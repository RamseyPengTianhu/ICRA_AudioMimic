# CF target semantics and supervision audit

This audit corrects the manuscript description; it does not change training,
inference, the SONIC bridge, or the official tracker. Paths below are relative
to the parent AudioMimic workspace and are internal reproducibility references.

## Ordinary music-conditioned Commit Forcing

Source root: `runtime/musics2dance_sources/listenahead-film-v1/`.

| Question | Implementation evidence | What follows |
|---|---|---|
| What does residual rebasing preserve? | `train_g1_paper_faithful_dc_streaming.py:1656`, `corrected_residual_target` | The full target latent is `e(q_target) + r_target`; subtraction of the sampled embedding preserves this sum. There is no boundary-state input to this operation. |
| Which boundary is used for the next plan? | Same file, `build_commit_forcing_context`, around lines 2415--2555 | The first committed generated native frames update history and the reference-derived boundary. The switch selects the complete history/residual/state context together. |
| Are the next targets changed? | Same helper and `train_g1_listenahead_mrt2.py`, around lines 400--535 | The next dataset q/residual targets are retained. The second residual target is rebased, not re-encoded under the generated boundary. |
| Is the first pass a full recursive batch rollout? | `train_g1_listenahead_mrt2.py`, same loss path | Supplied window transitions are sampled independently using AR structure and DDIM residual sampling. This matches a transition construction, not an entire long-horizon state distribution. |
| Does prefix-aware training alter this conclusion? | `train_g1_listenahead_prefix_start.py`, around lines 315--448 | Startup/preroll and history-dropout logic can change supplied contexts, but does not establish state-matched re-encoding of all next targets. |
| Can identical latent imply identical motion? | `model/g1_hybrid_streaming_codec.py:332`, `decode_components` | The decoder also uses boundary state, so the identity is not generally preserved across different boundaries. |
| Does state-matched target code exist elsewhere? | `model/g1_state_matched_commit_forcing.py:287`, `state_matched_full_latent` | Yes, a separate variant encodes target motion with the generated state. Its existence must not be conflated with activation in the reported music-conditioned CF path. |

Consequently, state closure makes the next context consistent with its committed
reference. It does not guarantee that the unchanged GT continuation is
continuous or dynamically compatible with that state. Pose/velocity boundary
jumps and target reconstruction under both boundaries are open measurements.
Likewise, rebasing adds a correction `e(q_target) - e(q_sampled)` to the residual;
codec separation alone cannot prove the same separation in generated samples.

### Focused CPU verification

Three existing tests passed with GPUs hidden and writable Numba/Matplotlib caches:

- `tests.test_g1_paper_faithful_dc_training.G1PaperFaithfulDCTrainingTest.test_corrected_residual_preserves_complete_latent_for_replaced_q0`
- `tests.test_g1_paper_faithful_dc_training.G1PaperFaithfulDCTrainingTest.test_oracle_q0_keeps_original_residual_target`
- `tests.test_g1_commit_forcing.G1CommitForcingTest.test_commit_context_switches_whole_causal_state`

These tests verify latent algebra and context switching only. They do not prove
decoded-motion invariance, long-rollout continuity, or improved music fit.

## Overlapping versus proposed supervision

The frozen clean-representation experiment documentation is
`docs/experiments/EXP-20260807-v6f-z-clean-representation.md` under the same source
root. The Z0 legacy route delegates to `train_g1_hybrid_streaming_codec.py`;
the clean routes are defined by `train_g1_clean_streaming_codec.py`.

- Legacy structure-channel weights cover all 34 channels, including arms:
  root 2, legs 1.5, waist 1.25, remaining channels 0.5.
- Legacy full reconstruction, contact/physical and boundary terms coexist
  with weighted q-only reconstruction, q endpoint/invariance, and residual-rate
  penalties. The contact head and gradient routes also differ.
- Proposed supervision uses normalized full and designated structure views and
  a residual-robust branch; the detailed coefficients and corruption rules are
  written in `supervision_details.tex`.
- The full-state rows compare a supervision bundle, not removal of all loss
  terms or a single scalar-weight change. Historical table values are preserved;
  binding each value to original checkpoint receipts remains an explicit TODO.

## Outcome evidence and scope

The new primary table transcribes correct-condition means from
`eval/results/benchmark_v1/formal/all_generator_routes_comparison/all_routes_metrics.csv`
for `C0_FMS_ONLY_FILM`, `FILM_AM`, and `RMS_FMS_EQ`: 18 songs, three sampling seeds.
These are generator-only results, not live SONIC measurements. Same-cohort
execution metrics and per-song uncertainty remain missing. A--D replay results
are separate diagnostics and cannot fill those rows.

Old DC-FILM-F and Film-AJ are aliases with identical audited model tensors, not
independent trained baselines. This release detail is kept here rather than
in the main architecture description. Original bitmap figures and `V1.tex`
are retained; `main.tex` uses the new native TikZ diagrams.
