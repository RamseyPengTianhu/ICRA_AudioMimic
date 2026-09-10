# Accepted MMR evidence integrated on 2026-09-11

## Authority

The owner adopted standard-training `R_cosine5` on 2026-09-10: [acceptance record](https://github.com/lbtwyk/Musics2Dance/issues/50#issuecomment-5618385423), preserved in `owner-acceptance.md`. The method checkout was verified at commit `911336680765c0c09fa62e4a0ffb3196671abbc5` on `codex/mmr-local-4090`. The user explicitly requested adopting this accepted result as the paper mainline, removing old MMR from the manuscript, and pushing the updated paper.

The frozen evaluator uses standard content-group sampling, five-second posterior-mean cosine, and score-level averaging of final update-14500 checkpoints for evaluator seeds 1234, 2345, and 3456. Inference is FP32 with the frozen training-only normalizer and continuous full-SO3 357-dimensional motion frontend. Archived source documents and scoring code are in `source/`.

## Data and result mapping

`generator-aggregate.json` and `generator-per-track.csv` were copied from the accepted experiment runtime on 4090-ts, under `/home/tianhup/Desktop/Musics2Dance/runtime/EXP-20260907-mmr-g1-plus-correspondence`. The eighteen arrays in `pair-scores/` retain all underlying pair scores. The cohort and evaluator-selection evidence are retained alongside them.

The 198 trajectories comprise two startup settings, three generator training seeds, three sampling seeds, and eleven eligible tracks. Every trajectory is 60 seconds. All eleven eligible gallery tracks and all repeats are retained. Each score matrix contains eleven music donors by eleven motion queries by 56 overlapping five-second windows. Donor audio offsets follow the archived source records.

| Paper name | Archived generator route | Correct cosine | Wrong cosine | Margin | Pairwise accuracy |
|---|---|---:|---:|---:|---:|
| Prefix-aware startup | FD-DF-L-AM-FHC | 0.21048145 | 0.03190388 | 0.17857757 | 74.20274170% |
| Direct-prefix startup | FD-DF-L-AJ-FHC | 0.20571008 | 0.02740084 | 0.17830924 | 75.01262626% |

These rows populate the primary correspondence table. Abstract, introduction, experiments, and conclusion use these same values. The separate 18-track motion-quality study retains its distribution/contact results but no old MMR column. Old MMR formulas, scores, and condition-use result tables are absent from the compiled manuscript; immutable historical evidence remains outside it.

## Reproduction

Run `python scripts/build_mmr_tables.py` with NumPy installed, then `python scripts/build_evidence_tables.py`. The first script independently reconstructs all 198 records from the eighteen score matrices, checks the CSV, reproduces every published mean and interval, and writes the paper rows. It applies half credit for differences within 1e-7. Bootstrap draws resample generator training seeds and query tracks while keeping the donor gallery fixed; sampling repeats are averaged within each training-seed/query-track cell. The 10,000 draws use seed 20260907. `verification.json` records reproduction status and SHA-256 hashes of the archived evidence.

## Claim boundary

The result measures intended-versus-alternative soundtrack ordering for fixed generated motion. It is not overall motion quality, eleven-way retrieval, a controlled music-input intervention, a causal forecast benefit, or a hardware/human-preference result. No startup superiority is claimed. The evaluator calibration configuration was selected after inspection; calibration and fixed-gallery intervals remain descriptive. The archived decision documents retain failed original confirmation gates and the complete candidate-selection history. The main paper gives the relevant selection disclosure once in Discussion. Historical-checkpoint comparison and missing controlled-generation/human studies remain future work outside the accepted claim.
