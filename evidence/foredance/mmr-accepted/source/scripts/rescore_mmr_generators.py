"""Rescore archived decoded FHC-FiLM outputs; never pretend missing Hybrid is scored."""
import argparse
import csv
import json
from pathlib import Path
import pickle
import time

import numpy as np
import torch
from huggingface_hub import HfApi

from eval.evaluate_mmr_g1_plus import validate_checkpoint_binding
from eval.mmr_g1_plus_features import extract_features, FEATURE_VERSION
from eval.mmr_g1_plus_score import encode_windows, readout
from model.g1_torch_kinematics import G1TorchKinematics
from model.mmr_g1 import MMRG1

ROOT = Path('/home/tianhup/Desktop/Musics2Dance/runtime/EXP-20260907-mmr-g1-plus-correspondence')
OUT = ROOT / 'generator-rescore'
REPO = Path(__file__).resolve().parents[1]
BUCKET = 'wyksdsg/musics2dance-server-public'
PREFIX = '20260908/project/runtime/EXP-20260904-v6f-aq-tmmr-direct-condition/evaluation/leaves/dev60'
SEEDS = (1234, 2345, 3456)
ROUTES = ('FD-DF-L-AM-FHC', 'FD-DF-L-AJ-FHC')


def validate_motion(raw, row):
    if raw['motion_format'] != 'g1_abs_6d' or float(raw['fps']) != 30:
        raise ValueError('wrong archived motion contract')
    if raw['audio_path'] != row['source_path'] or raw['source_path'] != row['source_path']:
        raise ValueError('audio identity mismatch')
    for k, d in [('root_pos', 3), ('root_rot', 4), ('dof_pos', 29)]:
        a = np.asarray(raw[k])
        if a.shape != (1800, d) or not np.isfinite(a).all():
            raise ValueError(f'invalid 60-second decoded trajectory: {k}')
    # Source exporter emits XYZW via decode_streaming_g1_motion/g1_abs_6d.
    np.testing.assert_allclose(np.linalg.norm(raw['root_rot'], axis=-1), 1, atol=1e-4)


def summary(values):
    # Average sampling seeds inside each training-seed/song cell first.
    a = np.asarray(values).mean(axis=1)
    rng = np.random.default_rng(20260907)
    train = rng.integers(0, a.shape[0], (10000, a.shape[0]))
    song = rng.integers(0, a.shape[1], (10000, a.shape[1]))
    samples = a[train[:, :, None], song[:, None, :]].mean(axis=(1, 2))
    return {'mean': float(a.mean()), 'ci95': np.quantile(samples, [.025, .975]).tolist(),
            'per_training_seed': dict(zip(map(str, SEEDS), a.mean(axis=1).tolist())),
            'bootstrap_scope': 'training seeds and songs; sampling seeds averaged within cells; descriptive'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--family', choices=('R', 'H'), default='R')
    args = parser.parse_args()
    family = args.family
    OUT = ROOT / ('generator-rescore' if family == 'R' else 'generator-rescore-H-cosine5')
    source_dir = ROOT / 'generator-rescore/source'
    OUT.mkdir(exist_ok=True)
    if (OUT / 'aggregate.json').exists():
        raise ValueError('preserve existing rescore')
    cohort = json.loads((REPO / 'eval/mmr_g1_finedance_domain_cohort.json').read_text())['windows']
    api = HfApi()
    if family == 'H':
        original = json.loads((ROOT / 'generator-rescore/source-manifest.json').read_text())
        if original['bucket'] != BUCKET:
            raise ValueError('source bucket mismatch')
        local_sources = {x['remote']: x for x in original['files']}
    else:
        remote = {x.path: x for x in api.list_bucket_tree(BUCKET, prefix=PREFIX, recursive=True)
                  if hasattr(x, 'size')}
    files, source_records = [], []
    for route in ROUTES:
        for train in SEEDS:
            for sample in SEEDS:
                leaf = f'{route}/train{train}/sample{sample}/cfg1p0/correct/motions/generated'
                for i, row in enumerate(cohort):
                    name = f'{i:03d}_{row["sequence_id"]}_f{row["start_frame"]:06d}.pkl'
                    key = f'{PREFIX}/{leaf}/{name}'
                    if family == 'H':
                        item = local_sources[key]
                        dst = source_dir / leaf / name
                        if str(dst) != item['local'] or dst.stat().st_size != item['bytes']:
                            raise ValueError(f'baseline source mismatch: {dst}')
                        source_records.append(item)
                        continue
                    if key not in remote:
                        raise FileNotFoundError(key)
                    dst = OUT / 'source' / leaf / name
                    files.append((remote[key], dst))
                    source_records.append({'remote': key, 'local': str(dst), 'bytes': remote[key].size})
    (OUT / 'source-manifest.json').write_text(json.dumps({'bucket': BUCKET, 'files': source_records,
        'hybrid': 'missing from checked public/private buckets and local checkout'}, indent=2)+'\n')
    print(f'Downloading {len(files)} decoded motions, {sum(x.size for x,_ in files)} bytes', flush=True)
    if files:
        api.download_bucket_files(BUCKET, files, raise_on_missing_files=True)
    for item, path in files:
        if path.stat().st_size != item.size:
            raise ValueError(f'incomplete download {path}')
    free, _ = torch.cuda.mem_get_info()
    if free < 4 * 1024**3:
        raise RuntimeError('Need4GiB free; leave unrelated GPU jobs untouched')
    torch.cuda.set_per_process_memory_fraction(.16)
    start = time.time()
    norm = np.load(ROOT / 'data/normalizer.npz')
    if str(norm['feature_version']) != FEATURE_VERSION:
        raise ValueError('wrong normalizer feature identity')
    source = Path(json.loads((ROOT/'backup-manifest.json').read_text())['source'])/'data'
    models = []
    for seed in SEEDS:
        saved = torch.load(ROOT/f'runs/{family}_seed{seed}/final.pt', map_location='cpu', weights_only=False)
        validate_checkpoint_binding(saved, family, seed, ROOT/'data', source)
        model = MMRG1().cuda().eval()
        model.load_state_dict(saved['model'])
        models.append(model)
        del saved
    fk = G1TorchKinematics(REPO/'third_party/unitree_g1_description/g1_29dof_rev_1_0.xml', root_quat_order='xyzw').cuda().eval()
    windows = np.arange(56)
    music = []
    for row in cohort:
        full = np.load(ROOT/'data/music'/f'fd_{Path(row["source_path"]).stem}.npy')
        offset = row['start_frame']
        a = np.stack([full[offset+s*30:offset+s*30+150] for s in windows])
        if a.shape != (56, 150, 4800):
            raise ValueError('incomplete aligned music')
        music.append(a)
    records, results = [], {}
    for route in ROUTES:
        values = {k: [] for k in ('score', 'wrong_track_score', 'margin', 'preference_accuracy')}
        for train in SEEDS:
            train_values = {k: [] for k in values}
            for sample in SEEDS:
                embeddings = [[] for _ in models]
                for i, row in enumerate(cohort):
                    name = f'{i:03d}_{row["sequence_id"]}_f{row["start_frame"]:06d}.pkl'
                    path = source_dir/route/f'train{train}'/f'sample{sample}'/'cfg1p0/correct/motions/generated'/name
                    with path.open('rb') as f:
                        raw = pickle.load(f)
                    validate_motion(raw, row)
                    features = extract_features(raw, fk, source_fps=30, ground_height=raw.get('ground_height')).numpy()
                    if features.shape != (1200,357):
                        raise ValueError('unexpected resampled duration')
                    features = (features-norm['mean'])/norm['std']
                    x = np.stack([features[s*20:s*20+100] for s in windows])
                    for m, model in enumerate(models):
                        embeddings[m].append(encode_windows(model, music[i], x, seconds=5))
                # Same correct generated dance, ten wrong music donors, matched relative time.
                scores = np.mean([readout(np.stack([e[0] for e in z])[:,None],
                                           np.stack([e[1] for e in z])[None,:], 'cosine5')
                                  for z in embeddings], axis=0)
                np.savez(OUT/f'{route}_train{train}_sample{sample}_scores.npz', pair_scores=scores)
                leaf = {k: [] for k in values}
                for i, row in enumerate(cohort):
                    correct = scores[i,i]
                    wrong = np.delete(scores[:,i], i, axis=0)
                    delta = correct[None,:]-wrong
                    v = {'score':float(correct.mean()), 'wrong_track_score':float(wrong.mean()),
                         'margin':float(delta.mean()),
                         'preference_accuracy':float(100*np.where(delta>1e-7,1,np.where(delta< -1e-7,0,.5)).mean())}
                    records.append({'route':route,'training_seed':train,'sampling_seed':sample,
                                    'sequence_id':row['sequence_id'], 'track':row['source_group'], **v})
                    for k in values:leaf[k].append(v[k])
                for k in values:train_values[k].append(leaf[k])
                print(json.dumps({'route':route,'train':train,'sample':sample,'score':np.mean(leaf['score'])}),flush=True)
            for k in values:values[k].append(train_values[k])
        results[route] = {k:summary(v) for k,v in values.items()}
    report = {'evaluator':f'{family}_cosine5 score ensemble seeds1234/2345/3456', 'results':results,
              'records':records,'cohort':str(REPO/'eval/mmr_g1_finedance_domain_cohort.json'),
              'seconds':60,'windows_per_track':56,'feature_version':FEATURE_VERSION,
              'status':'FiLM rescoring complete; Hybrid input missing; no FiLM/Hybrid winner',
              'scope':'archived correct-motion rescoring; not regenerated or new common-randomness proof',
              'generator_source':PREFIX,'normalizer':str(ROOT/'data/normalizer.npz'),
              'gpu_seconds':time.time()-start,'peak_allocated_bytes':torch.cuda.max_memory_allocated()}
    (OUT/'aggregate.json').write_text(json.dumps(report,indent=2)+'\n')
    with (OUT/'per_track.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    print(json.dumps(results),flush=True)


if __name__ == '__main__':
    main()
