# Standard versus confusing sampling: five-second cosine — 2026-09-10

Final owner decision after this comparison: retain standard R_cosine5 as the
primary evaluator, resume GitHub synchronization, and leave actual old-MMR
comparison as follow-up. The pause described below is historical.

H_cosine5 gives higher observed wrong-track pairwise accuracy on both archived
FHC-FiLM startup variants than R_cosine5. R is standard content-group sampling;
H is confusing-song sampling. Both use five-second cosine and three-seed
score-level ensembles. AM/AJ are prefix-aware/direct-prefix FiLM startup,
not FiLM/Hybrid architecture labels.

| Generator | Evaluator | Correct cosine | Wrong cosine | Margin | Pairwise accuracy |
|---|---|---:|---:|---:|---:|
| FiLM AM | R_cosine5 | 0.21048 | 0.03190 | 0.17858 | 74.20% |
| FiLM AM | H_cosine5 | 0.20572 | 0.02870 | 0.17703 | 75.69% |
| FiLM AJ | R_cosine5 | 0.20571 | 0.02740 | 0.17831 | 75.01% |
| FiLM AJ | H_cosine5 | 0.20005 | 0.02319 | 0.17686 | 76.79% |

Matched H-minus-R accuracy: AM +1.48449pp, descriptive95%CI[-0.96320,4.55997];
AJ +1.77850pp, CI[-1.62703,5.96505]. Neither interval excludes zero.
R gives slightly higher raw cosine and mean margin. Different win frequency
and mean margin rankings are compatible: one counts signs, the other retains
magnitudes. A larger raw cosine across learned evaluators does not establish
a better evaluator. This generated-output comparison is not evaluator selection.

Existing GT held-out evidence remains ordinary R68.41% versus H69.90%, confusing
R64.08% versus H61.23%. The observed generated-motion percentage advantage
does not establish universal H dominance or supersede the owner's R adoption.
User requested this supplementary comparison while pausing remaining GitHub
synchronization; no new acceptance, push or GitHub comment was made for it.

## Execution and integrity audit

Command: `bash scripts/run_mmr_generator_rescore.sh H`.
Completed tmux `mmr-h-cosine5-rescore`, run.exit0; scoring72.58s,
peak allocated584380928 bytes. No training or new generation.
Runtime: `/home/tianhup/Desktop/Musics2Dance/runtime/EXP-20260907-mmr-g1-plus-correspondence/generator-rescore-H-cosine5`.
Evidence: `aggregate.json`, `per_track.csv`,18 pair-score matrices,
`source-manifest.json`, `comparison.json`, `run.log`, `run.exit`.
Analysis: `PYTHONPATH=. python -m scripts.compare_mmr_generator_readouts`.

Overall WARN: matched FiLM comparison complete; historical generator provenance
and missing Hybrid scope inherited from the original rescore report.

| Check | Status | Evidence and impact |
|---|---|---|
| Ground truth/proxy | PASS | Archived generated PKLs remain labeled generated; frozen music identities |
| Metric semantics | PASS | Same shared feature extraction, cosine readout, ties1e-7; three evaluator scores averaged before wins |
| Artifact identity | PASS/WARN | Source manifests exactly equal; checkpoint family/seed/data binding verified; original generation receipts remain incomplete |
| Evaluation scope | PASS | Same198 motions,3 training x3 sampling seeds x11 songs x2 variants; 56 windows and10 donors; no Hybrid claim |
| Stage closure | PASS/WARN | H scoring and analysis exit0; other experiment stages remain open |
| Executed paths | PASS | 396 R/H records independently recomputed from36 matrices; means and bootstrap intervals reproduce |

29 focused tests pass; Python compile and launcher shell syntax pass. Both
families retain final update14500, shared train-only normalizer and full-SO3
continuous357D frontend. Bootstrap samples training seeds and query songs with
the gallery fixed, averaging sampling seeds within cells; use the same draws
for paired differences. Overlapping windows are not independent samples.

Candidate claim: confusing-sampling cosine gives higher observed fixed-gallery
pairwise accuracy for both FiLM starts. Material bound: difference intervals
include zero; this does not prove improved evaluator validity. Decision owner:
user. No recommendation to reselect an evaluator from generator scores.
