Source: https://github.com/lbtwyk/Musics2Dance/issues/50#issuecomment-5618385423
Recorded: 2026-09-10T12:04:35Z

## Final owner decision: standard-training MMR mainline

After reviewing the additional matched R/H five-second cosine comparison, the owner confirmed on 2026-09-10: “那就标准训练为主线，完成更新，留后续和旧mmr对比”.

**Accepted primary evaluator: R_cosine5** — standard content-group sampling, 5-second posterior-mean cosine, score-level ensemble of final update14500 checkpoints for seeds1234/2345/3456, FP32 inference, frozen train-only normalizer and full-SO3 continuous357D frontend. Use the same frozen identity for subsequent generator comparisons. H_cosine5 (confusing sampling) remains supplementary, not the mainline.

| Archived generator | R correct cosine | H correct cosine | R pairwise accuracy | H pairwise accuracy |
|---|---:|---:|---:|---:|
| FHC-FiLM AM, prefix-aware startup | 0.21048 | 0.20572 | 74.20% | 75.69% |
| FHC-FiLM AJ, direct-prefix startup | 0.20571 | 0.20005 | 75.01% | 76.79% |

H-minus-R paired accuracy differences: AM +1.48pp, descriptive95%CI[-0.96,4.56]; AJ +1.78pp, CI[-1.63,5.97]. H has higher observed generated-motion win rates, R slightly higher cosine/margins; neither accuracy-difference interval excludes zero. Existing GT confusing accuracy remains R64.08% versus H61.23%. The owner retains R; no generator-driven automatic reselection occurred.

Both rescoring runs exited0. The same198 motions, music donors, windows and aggregation were used; 396 R/H records independently reproduce from36 saved pair-score matrices. 29 focused tests pass. These percentages measure correct-versus-wrong music ordering, not overall motion quality or controlled condition use.

**Follow-up:** restore the actual old MMR checkpoint/normalizer and perform a matched old/new comparison. This is deferred and does not block adoption. Missing Hybrid decoded outputs, common-randomness controlled generation and human-validation work remain explicitly incomplete. Original failed confirmation gates and post-lockbox selection disclosure are preserved. No claim of measured historical-checkpoint superiority.

Full results, acceptance, local reproduction code and tests are synchronized on `codex/mmr-local-4090`; no automatic merge or issue closure.
- [Canonical experiment](https://github.com/lbtwyk/Musics2Dance/blob/codex/mmr-local-4090/docs/experiments/EXP-20260907-mmr-g1-plus-correspondence.md)
- [R/H generator comparison](https://github.com/lbtwyk/Musics2Dance/blob/codex/mmr-local-4090/docs/experiments/reviews/EXP-20260907-mmr-g1-plus-correspondence-generator-R-H-cosine5.md)
- [Primary evaluator specification](https://github.com/lbtwyk/Musics2Dance/blob/codex/mmr-local-4090/docs/research/modules/MUSIC_MOTION_EVALUATION_SPEC.md)
