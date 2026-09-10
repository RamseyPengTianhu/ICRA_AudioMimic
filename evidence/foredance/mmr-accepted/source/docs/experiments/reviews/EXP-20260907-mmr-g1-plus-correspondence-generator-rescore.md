# New MMR generator rescoring — 2026-09-10

## Result and scope

The frozen R_cosine5 evaluator gives archived FHC-FiLM generated motion higher
scores against its correct music than against the ten other gallery tracks.
Both AM (prefix-aware) and AJ (direct causal-prefix) startup variants have
positive mean margins in all three training seeds. These are two FiLM starts,
not a FiLM-versus-Hybrid comparison. Hybrid remains unscored: its decoded
outputs are absent from the checked local workspace and both HF backup buckets.
The user has been asked for their location. Do not mark the whole request done.

| Generator | Correct cosine | Wrong-track cosine | Paired margin | Descriptive95% margin interval | Preference accuracy |
|---|---:|---:|---:|---|---:|
| FHC-FiLM AM | 0.210481 | 0.031904 | +0.178578 | [0.093846,0.263340] | 74.20% |
| FHC-FiLM AJ | 0.205710 | 0.027401 | +0.178309 | [0.098332,0.260817] | 75.01% |
| Hybrid | missing input | — | — | — | — |

Do not select AM versus AJ or FiLM versus Hybrid from these absolute scores.
This tests scoring-time music correspondence of fixed generated motions, not
a newly controlled causal music-input intervention, temporal sensitivity,
physical motion quality or human preference. The frozen evaluator is not
reselected using these generated scores. Existing old-MMR results remain intact.

## Frozen identities and reproducibility

- Evaluator: R final checkpoints seeds1234/2345/3456, update14500; source-bound
  checkpoint identity checks pass, same train-only normalizer and full-SO3
  `mmr_g1_plus_so3_continuous_357_v1`, FP32 five-second cosine score ensemble.
- Source: public bucket `wyksdsg/musics2dance-server-public`, prefix
  `20260908/project/runtime/EXP-20260904-v6f-aq-tmmr-direct-condition/evaluation/leaves/dev60`.
- Routes: `FD-DF-L-AM-FHC`, `FD-DF-L-AJ-FHC`; correct condition, cfg1p0;
  three training seeds crossed with three sampling seeds,11 tracks each.
-198 decoded generated PKLs,1800 frames at30Hz each, have exported audio identity
  matched to `eval/mmr_g1_finedance_domain_cohort.json` and exact indexed filenames.
  Source records and HF file sizes are saved; native HF transfers verified size.
- Raw decoded root rotations are XYZW, traced to the main checkout's
  `eval/run_g1_abs_6d_wave_c_rollout.py:_save_waveform_motion` and
  `dataset/motion_representation.py:decode_g1_abs_6d_motion`. No re-decoding or
  inferred representation conversion is applied to the PKLs.
- Extract once per full trajectory to1200x357; apply frozen train normalizer;
 56 windows of5s at1s stride. Retain native audio starts960 and840 where specified.
- Average three evaluator scores before preference, then windows and ten wrong
  donors within track. Average sampling seeds inside training-seed/song cells.
  Bootstrap training seeds and query songs10000 draws, seed20260907; intervals
  are descriptive with the observed gallery held fixed, not independent donors.
- This is historical-artifact rescoring. Original generation source drift and
  missing runtime receipt coverage are not repaired by the new scorer.

## Integrity audit

Overall WARN: available FiLM rescoring is complete; requested Hybrid and new
controlled generation are not complete.

| Check | Status | Evidence / impact |
|---|---|---|
| Ground truth provenance | PASS | PKLs explicitly generated, not relabeled GT; correct audio and wrong donors come from frozen cohort |
| Metric semantics | PASS | Shared extract_features/encode_windows/readout; all198 score/margin records recomputed from saved11x11x56 pair matrices |
| Artifact identity | WARN | Exported file/audio/frame/model bindings verified; historical full generation receipts are not restored |
| Evaluation scope | WARN | Two FiLM startup variants only, no Hybrid; no architecture winner |
| Stage closure | WARN | FiLM rescore exit0; Hybrid missing input and formal common-randomness stage still open |
| Dead/divergent paths | PASS | Actual shared new-MMR functions called; no changes to old evaluator or original confirmation |

Focused validation:27 model/metric/binding tests pass, actual source PKL identity,
quaternion and1200x357 feature proof passes, constant aggregation proof passes;
shell syntax/Python compile pass. GPU stage72.28s, peak allocated584380928 bytes,
allocator cap16%, minimum4GiB free; unrelated jobs untouched.

## Artifacts and continuation

Runtime: `/home/tianhup/Desktop/Musics2Dance/runtime/EXP-20260907-mmr-g1-plus-correspondence/generator-rescore`.

`aggregate.json`, `per_track.csv`, `source-manifest.json`,18 saved pair-score
NPZs, `run.log`, `run.exit` (0). Command:
`bash scripts/run_mmr_generator_rescore.sh`; completed tmux `mmr-generator-rescore`.

Candidate claim: "The new evaluator assigns FHC-FiLM motions higher matching
scores for their correct tracks than for the other tracks in the fixed gallery."
Decisive comparison: per-motion correct music versus ten other gallery tracks.
Material bounds: fixed-gallery descriptive rescore, not new causal generator
validation or FiLM/Hybrid superiority. User owns acceptance.

Next required input: Hybrid decoded motions and their audio/start-frame/seed
bindings, preferably the historical matched `generation/FD-Hybrid-{AM,AJ}/seed*`
leaves. Checkpoints alone require a separate local generation adaptation and
resource decision; do not silently replace scoring with an unverified launch.
