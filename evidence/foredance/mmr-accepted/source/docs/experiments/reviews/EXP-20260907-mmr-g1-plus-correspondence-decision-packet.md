# MMR decision packet — 2026-09-10

## Supported result

The new evaluator assigns archived FHC-FiLM motions higher scores for their
correct music than for wrong music in the fixed eleven-track gallery.
The decisive comparison holds motion fixed and substitutes ten music donors.

| Generator startup | Actual historical MMR, matched percentage | New MMR percentage | Descriptive 95% interval |
|---|---:|---:|---|
| FHC-FiLM AM: prefix-aware startup | unavailable | 74.20% | [63.77%, 84.15%] |
| FHC-FiLM AJ: direct causal-prefix startup | unavailable | 75.01% | [65.17%, 84.13%] |
| Hybrid AM | unavailable | unavailable | — |
| Hybrid AJ | unavailable | unavailable | — |

New evaluator is R_cosine5: standard-sampling training, five-second cosine,
three-checkpoint score ensemble. AM/AJ are startup variants, not architectures.
Accuracy counts correct-score wins over wrong-score, with half credit for ties;
it is not a ratio of score magnitudes, eleven-way retrieval accuracy, or a
percentage of overall motion quality. Random pairwise ordering is 50%.

FiLM evidence: 198 decoded sixty-second motions, three training seeds crossed
with three sampling seeds and eleven songs per variant; 56 five-second windows.
Intervals bootstrap training seeds and query songs with the gallery fixed.
Saved results are described in the companion `generator-rescore.md` report;
this packet records no additional model execution or new independent test.

## Decision status

Owner decision, 2026-09-10: **accepted; adopt R_cosine5 as the primary MMR
evaluator for subsequent generator experiments**. This supersedes the pending
adoption decision, not the missing comparisons below. Keep one frozen evaluator
across generators. Old-checkpoint superiority remains unresolved, while its
recovery is no longer a prerequisite for adopting the new mainline.

- Current new-evaluator recommendation remains R_cosine5. Its confusing held-out
  accuracy is 64.08%, versus 60.22% for confusing-sampling multiscale H_ms.
  This was descriptive selection after opening the lockbox, not a fresh test.
- The historical-checkpoint replacement decision and FiLM/Hybrid comparison
  remain unresolved. R_ms belongs to the new training experiment and must not
  be substituted for the actual historical evaluator.
- AJ's observed +0.81 percentage points over AM is not evidence of a reliable
  winner; a paired difference interval has not been reported here.
- The percentages can be reported as fixed-gallery wrong-track pairwise
  correspondence evidence. They do not establish overall generator quality,
  superiority to historical MMR, or paper acceptance.

## Recovery audit and exact missing inputs

Checked local workspace/cache, recursively listed both HF server backup
buckets, scanned available HF model/dataset repositories, and inspected GitHub
release asset metadata. The following inputs were not found as directly
accessible artifacts:

1. Historical evaluator checkpoint plus matching normalizer/configuration.
   Relevant historical identities are
   `EXP-20260902-mmr-g1-evaluator-selection/evaluator/fd/final.pt` and the
   abs-6D evaluator used by later runs,
   `EXP-20260903-mmr-g1-abs-6d-evaluator/evaluator/fd/final.pt`.
   Restore the identity that actually scored the chosen generator outputs;
   do not silently interchange the two evaluators.
2. Hybrid decoded motions with song/start-frame/training-seed/sampling-seed
   bindings. Historical candidates were recorded under
   `EXP-20260902-mmr-g1-evaluator-selection/generation/FD-Hybrid-{AM,AJ}/seed*`.
   Cohort compatibility must be established before filling the comparison.

HF migration index
`hf://buckets/wyksdsg/musics2dance-server-private/20260908/migration-index.json`
explicitly has `complete: false`; its inventory note says the inventory is
not proof that all listed files were uploaded. An inventory path alone is
therefore not an available checkpoint.

The GitHub `lbtwyk/Musics2Dance` release `listenahead-hybrid-v1` contains
inference weights and supporting assets, but no matching decoded motion pack
or historical MMR evaluator. Weights alone do not close this rescore.
The private backup release
`lbtwyk/musics2dance-server-backup`, tag `project-context-20260908`, contains
split context archives and a compressed capture inventory. Their binary
contents were not inspectable through the available authenticated GitHub read
interface. Absence inside those archives has **not** been established.

Continuation requires an accessible source directory/HF object for the two
input classes, or access to the original source server. Then restore the exact
bindings, compute historical and new scores on the same compatible motions,
report paired percentage differences and intervals, and present the completed
decision table. Scientific adoption is owner-accepted; operational completion
stays blocked by the missing inputs and other undeclared-complete stages.
