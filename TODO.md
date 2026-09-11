# Evidence required for the ForeDance draft

These are manuscript evidence gaps, not new experiment-launch authorization. Keep them within the research repository's existing experiment specifications and ledger.

| ID | Needed evidence | Paper role |
|---|---|---|
| M1 | Matched heard-music versus predicted-music generators, common sources, fixed training and sampling conditions, matching and motion-quality metrics | Isolate the value of anticipation. Predicted versus no-music cannot replace this. |
| D1 | Current full-orientation codec reconstruction, structural/detail interventions, non-collapse checks and paired-supervision evidence | Explain the intended division of labor. Use the current representation-specific masks. |
| D2 | Separately trained pure-discrete and pure-continuous generators with matched settings | Establish the generation benefit of D+C and training. Decoder branch removal is not a trained baseline. |
| C1 | Current conditioned generator with matched Teacher Forcing and Commit Forcing, 60-second rollouts and each 20-second position | Test continuation quality and commit-boundary behavior. |
| V1 | Matched qualitative long sequences for the displayed comparison | The current 60-second case is genuine generation, but no matched TF result is supplied. |
| V2 | Current generated reference and corresponding fixed-controller recording, explicitly simulation or hardware | Short execution case; kinematic rendering does not establish execution. |

## Unfinished ablations — explicit draft TODOs

The manuscript now contains a visible **Pending Ablation Studies** subsection. Its four TODO paragraphs map directly to M1, D1, D2 and C1 above. None has a result yet; the author will supply these later. Add results only after matching the current representation, sources, training and sampling conditions, and archived evaluation identity. The completed clean-history/dropout/corruption comparison is a supporting history-training study, not a substitute for these core ablations.

- [ ] M1 — Forecast versus heard-music conditioning: learned correspondence, BAS and motion quality on matched generated motions.
- [ ] D1 — Paired structure/detail training: reconstruction, interventions and non-collapse evidence on the current representation.
- [ ] D2 — Independently trained discrete-only, continuous-only and combined generators.
- [ ] C1 — Commit Forcing versus Teacher Forcing: 60-second rollouts, all three non-overlapping 20-second positions, boundary behavior and matched qualitative sequences.
- [ ] V1/V2 — Add matched long renders and current-model execution evidence when available; retain their separate scope.

## Populated tables and source boundaries

The evaluator-validation table reports reference-motion discrimination (30 content groups, 3,661 windows); it does not score ForeDance. The generator music table reports the higher complete initialization result for each metric: learned correspondence uses 99 generated 60-second motions from all 11 tracks; BAS uses 162 outputs from all 18 tracks and the common 23-second crop. All three training and three sampling seeds remain included. The three-row history-training table holds initialization fixed and compares clean history, dropout and corruption using that same 18-track cohort. The complete two-initialization scores remain archived in `evidence/foredance/music-evaluation-selection.json` and its source records. Post-hoc reporting choices are disclosed once in Discussion; no initialization-superiority claim is made.

Do not pool the distinct cohorts, relabel the 23-second scores as 60-second results, or treat these tables as completion of M1, D1, D2 or C1.

## Existing outputs awaiting later results — 2026-09-11

The author will add missing results later. The GitHub/HF audit located reusable outputs under the existing `EXP-20260904-v6f-aq-tmmr-direct-condition` experiment; this is not a new experiment or a launch request.

- **Expand matched 60-second correspondence:** the public HF bucket `wyksdsg/musics2dance-server-public`, under `20260908/project/runtime/EXP-20260904-v6f-aq-tmmr-direct-condition/evaluation/leaves/dev60/`, contains 99 correct-condition generated motions for each of five routes: startup-aware/direct FHC, startup-aware/direct clean history, and startup-aware history dropout. The five route inventories share exactly the same 11 source identifiers and three-by-three training/sampling bindings. The archive already contains accepted correspondence scores for the two FHC routes (198 motions); the other three provide 297 potential additional scores. The compact paper displays one complete FHC configuration for correspondence. Recover generation identity and native audio offsets, then use the accepted frozen standard-training evaluator and unchanged full-cohort aggregation. File presence and sample inspection do not establish a completed score or restore missing generation receipts.
- **Keep motion-quality horizons explicit:** if the archived 60-second controls are scored for motion quality, use matching reference motions and one common feature protocol, with the three 20-second positions separately inspected. Until this is complete, retain the existing 18-track, 23-second results as a separate study.
- **Longer qualitative examples:** the same experiment's `evaluation/survival/` contains one 120-second music program and three 60-second switch programs for five history/startup routes and three training seeds, totaling 60 saved motions. One 120-second file and two added 60-second controls were downloaded and inspected in the audit. Complete recording/audio checks and qualitative review are still needed before adding a display or aggregate claim. These are generated references, not robot execution.
- **Do not reuse obsolete scores:** older HF conditioning comparisons and GitHub representation/CoF/simulation results belong to different model or evaluation identities. Preserve them as provenance rather than inserting their numbers into current-model result cells. In particular, the old no-music distances do not become results from the newly adopted evaluator.

The paper lists missing core comparisons explicitly as TODO paragraphs. Do not create filled or zero-valued result cells for pending outcomes.

Do not add wrong-time tests, human blind evaluation, runtime tables, an OMG result section, or additional mandatory CoF component training. The D+C image contains only the two principal reconstruction paths; corrupted-detail training is described in the text.

## Execution integration status

The fixed-controller interface follows teammate revision d12a5c0, adapted to the current 38D representation. Appendix replay values are transcribed from the separate 34D study in 0cc6cee; they do not close V2. The exact source table and recorded metrics path are in evidence/foredance/team-execution/. Before admitting a current-model execution result, reconcile reference/checkpoint identity, the existing T01 joint-order/offset/timestamp audit, and recording coverage. No new training, human study, timing study, or hardware launch is authorized by this manuscript integration.
