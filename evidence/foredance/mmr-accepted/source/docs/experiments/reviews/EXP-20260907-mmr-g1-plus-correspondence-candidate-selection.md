# MMR-G1+ candidate selection — 2026-09-10

## Recommendation

Use **R_cosine5**, the ensemble of three standard-trained final checkpoints with
five-second posterior-mean cosine scoring, as the current correspondence
evaluator recommendation. It has the highest confusing wrong-music accuracy in
the complete measured matrix: 64.08%. H_ms (confusing training plus historical
MS) reaches 60.22%, so its development-set lead does not carry over here.

This is a practical recommendation requested by the owner, not scientific
acceptance or a claim of statistically established universal superiority.
The original R_cosine5 versus R_ms confirmation remains unchanged. All additional
comparisons are descriptive on the already-opened lockbox, not a fresh test.

## Scope and identifiers

R: common repaired frontend and standard content-group-uniform training.
H: same model/loss/population with 64 uniform anchors and64 distinct-group
confusing-music neighbors per batch. MS: historical one-second segment feature
and dynamics distance, negated for higher-is-better comparisons. cosine5 and
l2_5 encode a complete five-second window; cosine1 and l2_1 encode its five
one-second segments. L2 readouts use negative squared Euclidean distance.

All six checkpoints are final update14500, seeds1234/2345/3456. Scores, not
embeddings or accuracies, are averaged across seeds before ranking. Frozen
lockbox:30 content groups,3661 windows,15 disjoint song pairs per task. No new
training, cohorts, feature versions, loss, readout math or generated motions.

Ranking rule recorded before supplemental evaluation: confusing accuracy
descending, ordinary accuracy for exact ties. Retrieval remains reported but
does not choose the correspondence evaluator. This does not erase the original
confirmation's retrieval guardrails or their outcome.

## Complete selection table

Percentages; higher is better. Development has9 groups and4 song pairs per
task; the opened lockbox has30 groups and15 pairs. Do not treat all windows as
independent or compare different gallery sizes as matched retrieval tests.

| Rank | Candidate | Development ordinary | Development confusing | Lockbox ordinary | Lockbox confusing |
|---|---|---:|---:|---:|---:|
| 1 | R_cosine5 | 71.61 | 67.47 | 68.41 | 64.08 |
| 2 | R_l2_5 | 71.72 | 67.71 | 68.36 | 63.74 |
| 3 | R_l2_1 | 68.68 | 63.61 | 66.56 | 62.36 |
| 4 | R_cosine1 | 70.41 | 63.63 | 66.71 | 62.36 |
| 5 | R_ms | 69.46 | 63.29 | 66.40 | 61.96 |
| 6 | H_cosine5 | 71.07 | 68.11 | 69.90 | 61.23 |
| 7 | H_l2_5 | 70.40 | 68.78 | 69.97 | 60.63 |
| 8 | H_ms | 74.62 | 69.73 | 66.05 | 60.22 |
| 9 | H_l2_1 | 74.76 | 69.83 | 66.15 | 60.12 |
| 10 | H_cosine1 | 74.73 | 68.78 | 65.04 | 59.88 |

R_l2_1 and R_cosine1 differ by less than0.001pp on confusing accuracy; their
ordering is numerical, not a meaningful established separation. R_cosine5
exceeds R_l2_5 by0.338pp, paired95%CI[-0.522,1.135]pp: a near-tie, not proof
that cosine itself is superior to five-second squared distance.

## Retrieval appendix

| Candidate | Music to motion R@1 | R@5 | Motion to music R@1 | R@5 |
|---|---:|---:|---:|---:|
| R_cosine5 | 12.22 | 38.89 | 11.11 | 42.22 |
| R_l2_5 | 13.33 | 38.89 | 12.22 | 40.00 |
| R_l2_1 | 13.33 | 35.56 | 14.44 | 37.78 |
| R_cosine1 | 15.56 | 37.78 | 12.22 | 36.67 |
| R_ms | 13.33 | 34.44 | 13.33 | 36.67 |
| H_cosine5 | 5.56 | 35.56 | 10.00 | 41.11 |
| H_l2_5 | 7.78 | 38.89 | 10.00 | 41.11 |
| H_ms | 8.89 | 41.11 | 8.89 | 37.78 |
| H_l2_1 | 8.89 | 40.00 | 10.00 | 37.78 |
| H_cosine1 | 10.00 | 42.22 | 10.00 | 38.89 |

## Decisive comparisons and original confirmation

- H_ms minus R_ms: ordinary -0.350pp, CI[-3.525,2.544]; confusing -1.735pp,
  CI[-5.078,1.541]. The development lead is not reproduced in point estimates.
- R_cosine5 minus H_ms: ordinary +2.361pp, CI[-1.779,6.891]; confusing +3.860pp,
  CI[-1.842,9.320]. These are descriptive unadjusted paired intervals, not
  selection-adjusted evidence that the chosen winner is superior.
- Original frozen R_cosine5 minus R_ms: confusing +2.124pp,
  CI[-2.878,6.419]; ordinary +2.011pp, CI[-1.267,4.826]. The +5pp and positive
  lower-CI gates remain unmet; motion-to-music R@1 declines2.222pp, beyond the
  original2pp guardrail. Recommendation does not retroactively pass these gates.

## Experiment integrity audit

Overall: **WARN**, for interpretation and remaining scope, not corrupted results.

| Check | Status | Evidence and claim impact |
|---|---|---|
| Ground truth provenance | PASS | Inherited real-motion content groups; no model-generated GT; music similarity defines donors, not human judgments |
| Metric semantics | PASS | Reused frozen readout/ensemble/bootstrap; all ten candidates' pair units recomputed through per-seed margins |
| Artifact identity | PASS | Three H files match original HF manifest sizes; family/seed/source binding and archived calibration parity pass; R confirmation metrics reproduce exactly |
| Evaluation scope | WARN | Complete10-cell comparison, but extra cells inspected after original lockbox opened; descriptive selection, not independent confirmation |
| Stage closure | WARN | Candidate comparison exit0; controlled generation and historical generated/no-music audit remain absent |
| Dead/divergent paths | PASS | New driver imports actual shared evaluator; original frozen evaluation_plan and confirmation files unchanged |

29 focused tests pass (27 existing model/metric/binding plus2 candidate tests).
H calibration checks retain rtol=atol=1e-4; metric tie tolerance is unchanged.
H encoding and full matrix analysis completed in19.94s excluding downloads;
peak allocated GPU348.35MiB, allocator capped16% with at least4GiB free before
start. No unrelated GPU processes were stopped. Native HF sync downloaded only
three final checkpoints,621608711 bytes. Durable session:
`mmr-candidate-comparison`; final `run.exit` is0.

## Candidate result-to-claim judgment

- Experiment: EXP-20260907-mmr-g1-plus-correspondence.
- Leading claim: Standard-trained five-second cosine scoring achieves the
  highest observed confusing wrong-music accuracy in the measured candidate matrix.
- Battlefield: real-motion wrong-music discrimination, frozen30-group cohort,
  three-seed score ensembles, all five readouts for R/H.
- Decisive evidence: R_cosine5 64.08%, R_l2_5 63.74%, H_ms 60.22%.
- Material bounds: point-estimate selection, near-tie with R_l2_5, original
  confirmation gates unmet; no direct historical-checkpoint matched comparison.
- Missing decisive evidence for universal old-MMR replacement: matched legacy
  checkpoint evaluation and intended generated-motion validation. R_ms is the
  repaired/retrained baseline, not the old checkpoint. The old checkpoint also
  cannot be assumed unseen on groups carved from its historical training set.
- Suggested wording: "Five-second cosine scoring of the standard-trained
  ensemble attains64.08% confusing wrong-music discrimination accuracy, the
  highest observed value among the ten evaluated configurations."
- Decision owner: user; recommendation recorded, acceptance not assigned.

## Reproducible artifacts and usable identity

Runtime root: `/home/tianhup/Desktop/Musics2Dance/runtime/EXP-20260907-mmr-g1-plus-correspondence`.

- `selection-comparison/aggregate.json`: all metrics, per-seed results, pair units,
  pairwise differences, checkpoint bindings and H calibration parity.
- `selection-comparison/comparison.csv`: complete sortable table including retrieval.
- `selection-comparison/H_seed*_embeddings.npz`: additional saved embeddings.
- `selection-comparison/run.log`, `run.exit`: download/execution and exit status.
- `lockbox/aggregate.json`: untouched original confirmation.
- `calibration/aggregate.json`: original development matrix.

Recommended identity: `runs/R_seed1234/final.pt`, `runs/R_seed2345/final.pt`,
`runs/R_seed3456/final.pt`; feature version
`mmr_g1_plus_so3_continuous_357_v1`; `data/normalizer.npz`; shared readout
`cosine5` from `eval/mmr_g1_plus_score.py`. Score is higher-is-better and
averaged over the three models and five-second windows at one-second stride.
Do not feed historical yaw-only caches or substitute a single best seed.
