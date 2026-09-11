"""Verify accepted MMR results from saved pair scores and reproduce paper rows."""
from pathlib import Path
import json,csv,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'evidence/foredance/mmr-accepted'
d=json.loads((P/'generator-aggregate.json').read_text());records=d['records']
assert len(records)==198 and d['seconds']==60 and d['windows_per_track']==56
seeds=[1234,2345,3456]
labels={'FD-DF-L-AM-FHC':'Startup-aware','FD-DF-L-AJ-FHC':'Direct'}
metrics=['score','wrong_track_score','margin','preference_accuracy']
csv_rows=list(csv.DictReader((P/'generator-per-track.csv').open()));assert len(csv_rows)==len(records)
for a,b in zip(csv_rows,records):
 for key in metrics:np.testing.assert_allclose(float(a[key]),b[key],rtol=0,atol=1e-14)
rows=[];verified=0
for route,label in labels.items():
 arrays={k:np.empty((3,3,11)) for k in metrics}
 for ti,train in enumerate(seeds):
  for si,sample in enumerate(seeds):
   rec=[r for r in records if (r['route'],r['training_seed'],r['sampling_seed'])==(route,train,sample)]
   assert len(rec)==11 and len({r['track'] for r in rec})==11
   scores=np.load(P/'pair-scores'/f'{route}_train{train}_sample{sample}_scores.npz')['pair_scores']
   assert scores.shape==(11,11,56) and np.isfinite(scores).all()
   for i,r in enumerate(rec):
    correct=scores[i,i];wrong=np.delete(scores[:,i],i,axis=0);delta=correct[None,:]-wrong
    calc=[correct.mean(),wrong.mean(),delta.mean(),100*np.where(delta>1e-7,1,np.where(delta< -1e-7,0,.5)).mean()]
    for key,value in zip(metrics,calc):
     np.testing.assert_allclose(value,r[key],rtol=0,atol=1e-12);arrays[key][ti,si,i]=value
    verified+=1
 for key,values in arrays.items():
  a=values.mean(axis=1);rng=np.random.default_rng(20260907)
  train=rng.integers(0,3,(10000,3));song=rng.integers(0,11,(10000,11))
  bs=a[train[:,:,None],song[:,None,:]].mean(axis=(1,2));ci=np.quantile(bs,[.025,.975])
  np.testing.assert_allclose(a.mean(),d['results'][route][key]['mean'],rtol=0,atol=1e-12)
  np.testing.assert_allclose(ci,d['results'][route][key]['ci95'],rtol=0,atol=1e-12)
  np.testing.assert_allclose(a.mean(axis=1),list(d['results'][route][key]['per_training_seed'].values()),rtol=0,atol=1e-12)
 v=d['results'][route];acc=v['preference_accuracy'];margin=v['margin']
 rows.append(f"{label} & {v['score']['mean']:.4f} & {v['wrong_track_score']['mean']:.4f} & +{margin['mean']:.4f} & [{margin['ci95'][0]:.4f}, {margin['ci95'][1]:.4f}] & {acc['mean']:.2f} [{acc['ci95'][0]:.2f}, {acc['ci95'][1]:.2f}] "+r'\\')
(ROOT/'evidence/foredance/mmr_correspondence_rows.tex').write_text('\n'.join(rows)+'\n')
# Keep both verified configurations in the archive; select a complete result
# for the compact paper presentation, never individual tracks or seed cells.
selected=max(labels,key=lambda route:d['results'][route]['preference_accuracy']['mean'])
v=d['results'][selected];acc=v['preference_accuracy'];margin=v['margin']
quality=json.loads((ROOT/'evidence/foredance/motion-quality.json').read_text())
bas_metric='G1FKRoboPerformBAS'
bas_selected=max(labels,key=lambda route:quality['routes'][route]['mean'][bas_metric])
bas=quality['routes'][bas_selected]['mean'][bas_metric]
for route in labels:
 seed_means=[r['mean'][bas_metric] for r in quality['routes'][route]['by_training_seed'].values()]
 np.testing.assert_allclose(np.mean(seed_means),quality['routes'][route]['mean'][bas_metric],rtol=0,atol=1e-12)
summary_rows=[
 f"Learned correspondence & 11 tracks, 60\\,s & {acc['mean']:.2f}\\% "+r'\\',
 f"Beat alignment (BAS) & 18 tracks, 23\\,s & {bas:.4f} "+r'\\',
]
(ROOT/'evidence/foredance/mmr_summary_rows.tex').write_text('\n'.join(summary_rows)+'\n')
(ROOT/'evidence/foredance/mmr_selected_rows.tex').write_text(
 f"ForeDance & {v['score']['mean']:.4f} & {v['wrong_track_score']['mean']:.4f} & +{margin['mean']:.4f} & [{margin['ci95'][0]:.4f}, {margin['ci95'][1]:.4f}] & {acc['mean']:.2f} [{acc['ci95'][0]:.2f}, {acc['ci95'][1]:.2f}] "+r'\\'+'\n')
(ROOT/'evidence/foredance/music-evaluation-selection.json').write_text(json.dumps({
 'date':'2026-09-11',
 'policy':'Author-requested metric-specific maximum across the two complete FHC initialization configurations, selected after evaluation. No source, window, training seed or sampling seed selection within a configuration.',
 'primary_evaluator':'R_cosine5; unchanged owner-accepted identity',
 'generator_correspondence':{'metric':'preference_accuracy','selected_route':selected,'mean':acc['mean'],'records':99,'tracks':11,'seconds':60,'source':'mmr-accepted/generator-aggregate.json','candidates':{r:d['results'][r]['preference_accuracy']['mean'] for r in labels},'companion_scores':'All score, wrong-score, margin and interval fields use the accuracy-selected configuration; they are not independently maximized.'},
 'beat_alignment':{'metric':bas_metric,'selected_route':bas_selected,'mean':bas,'records':162,'tracks':18,'seconds':23,'source':'motion-quality.json','candidates':{r:quality['routes'][r]['mean'][bas_metric] for r in labels}},
 'history_control_table':{'routes':['FD-DF-L-AM-HCLEAN','FD-DF-L-AM-HDROP','FD-DF-L-AM-FHC'],'reason':'Matched history-training controls at the initialization used for headline BAS; all displayed metrics use the same complete cohorts and configurations.'},
 'uncertainty':'Previously computed intervals are retained only as descriptive intervals conditional on the selected configuration, not selection-independent significance.',
 'complete_outcomes_retained':['mmr-accepted/generator-aggregate.json','mmr-accepted/pair-scores/','mmr_correspondence_rows.tex','motion-quality.json'],
},indent=2)+'\n')
(P/'verification.json').write_text(json.dumps({'verified_records':verified,'pair_matrices':18,'dimensions':[11,11,56],'bootstrap_draws':10000,'bootstrap_seed':20260907,'all_published_means_intervals_and_seed_means_reproduced':True,'hashes':{str(p.relative_to(P)):hashlib.sha256(p.read_bytes()).hexdigest() for p in P.rglob('*') if p.is_file() and p.name!='verification.json'}},indent=2)+'\n')
print('Verified 198 records, 18 pair matrices, all means and confidence intervals. Wrote accepted MMR rows.')
