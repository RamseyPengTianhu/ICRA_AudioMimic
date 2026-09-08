# Open evidence gates and experiments

Updated 2026-09-08. This is a collaborative research checklist, not a statement
that the listed experiments have been completed. IDs match the red TODOs in
`main.tex`. Evidence already available is mapped in `REVISION_NOTES_20260908.md`.

Close a gate only with a frozen protocol, reproducible result artifacts, and a
manuscript claim consistent with the result. A negative result can close an
experiment while requiring a weaker claim. Optional research directions must
not become implicit prerequisites or completed contributions.

## P0: Trustworthy measurements

### T01. Interface, reconstruction, and provenance

- [ ] Check absolute named target/measured fields versus raw fallback ordering
  and default offsets, as well as radians, root axes, quaternion order, and fps.
- [ ] Audit timestamp alignment among audio cutoff, publish, fetch, deadline,
  sent reference, consumed target, feedback, and simulated state.
- [ ] Verify reconstructed video against original simulation observations and
  known poses; rerun affected anatomical groups and startup statistics.
- [ ] Preserve source receipts, checkpoint/codec hashes, code versions, audio
  offsets, initial states, and packet/preview/safety settings for every table.
- [ ] Link historical representation-table numbers to their original artifacts;
  these values were preserved, not regenerated during the manuscript update.

**Blocked claims:** historical standing deltas as pure training error; visual
execution conclusions based on the incorrect joint conversion.

## P1: Method evidence

### T02. Commit Forcing versus Teacher Forcing

- [x] Audit ordinary music-conditioned CF: rebasing preserves the target latent,
  not decoded motion across changed boundary states. Next dataset targets are
  unchanged; first-pass window transitions are sampled independently. See
  `METHOD_AUDIT_20260908.md` for source paths and focused CPU tests.
- [ ] Measure target decoding under dataset versus generated boundaries and
  reference pose/velocity jumps after generated commits. Compare ordinary
  latent rebasing with the separate state-matched target objective under matched
  training; do not assume target re-encoding is active in the reported music path.
- [ ] Compare TF/CF using matched representation, parents, data, update budget,
  training seeds, inference NFE, sampling seeds, and startup.
- [ ] Remove sampler, commit, and state closure separately under matched training.
- [ ] Evaluate 60-s free-running motion, boundary continuity, and degradation
  over time; aggregate uncertainty by song rather than by frame.

**Blocked claim:** CF improves long-horizon deployment. Existing stable runs and
the two-seed codec study do not demonstrate a CF training benefit.

### T03. D+C and structural interpretation

- [x] Rename the legacy comparator overlapping supervision and document its
  channels, weights, auxiliary head, and differences from the proposed objective
  in `supervision_details.tex`. Historical checkpoint-to-table binding remains T01.
- [ ] Audit planner residual norms/tails, discrete mismatch, and rebasing
  correction-to-original residual magnitude. Repeat branch interventions in
  recursive generation, not only in codec reconstruction, to test whether
  residuals primarily compensate structural sampling errors.
- [ ] Link the standalone D+C contribution to native kinematic supervision,
  complementary structure/detail views, shared decoding/commitment, and branch
  intervention evidence; distinguish this from prior discrete+continuous methods.
- [ ] Complete recursive discrete-only rollout, updating history and state from
  its actual zero-residual output.
- [ ] Train independent continuous-only and direct motion-space controls with
  matched data, compute, boundary state, and generation duration.
- [ ] Compare reconstruction and generated quality, not only fixed-q0 decoding.
- [ ] Evaluate D+C controls across MMR, music adaptation, and dance quality;
  verify that detail improvements survive SONIC without assuming that less jerk
  or larger diversity implies better aesthetics.
- [ ] Audit cross-song q0 semantics only if a genre/style-token claim is retained.

**Available:** codec mechanism study and fixed-q0 residual counterfactual.
**Blocked claims:** complete architectural superiority; proven genre semantics.

### T04. Music content and injection architecture

- [ ] Complete matched unconditional, static-now, past-only, predicted-future,
  and calibrated oracle controls. An OOD oracle substitution is not an upper bound.
- [ ] Match startup and account for capacity when comparing FiLM and LCA; obtain
  and audit the original joint-project aggregate results where needed.
- [ ] Separate RMS/FMS content changes from AJ/AM startup-training changes.
- [ ] Check correct/null, wrong-song, and wrong-time responses for *appropriate*
  adaptation rather than merely changed motion or changed q0 tokens.
- [ ] Generate matched-history/noise D_A and D_B, score each with both songs,
  and test correct-pair fit margins using same-style/similar-tempo and cross-style
  negatives. Repeat for measured execution with the original audio clock fixed.

**Blocked claims:** FiLM is universally best; predicted future outperforms causal
history controls; changed conditions guarantee correct musical adaptation.

### T05. Learned standing startup

- [ ] Verify deployed initialization and the first public C4 agree with the
  trained visible-start contract; do not silently substitute private preroll.
- [ ] Test the u6250 candidate against matched old-model/initialization controls
  over songs, sampling seeds, and measured standing variations.
- [ ] Measure untrimmed first-pose delta, early joint speed, foot contact, root
  drift, recovery time, and failures; separate reference from execution metrics.
- [ ] Validate the transition-duration choice in generated and executed motion,
  not only interpolated targets and codec reconstructions.
- [ ] Check later activity, diversity, musicality, and freezing to rule out
  learning to stand still as the apparent solution.

**Available:** training completion and target/codec feasibility checks.
**Blocked claim:** startup instability has been solved.

### T06. Consumption age and effective future horizon

- [ ] Repeat matched cache/live experiments over independent songs and seeds.
- [ ] Complete the content x age matrix (cache/live at ideal/old/new ages),
  keeping audio cutoffs, initialization, and random sampling fixed.
- [ ] Pair replay diagnostics with actual online S/B configurations and record
  age/valid-frame distributions, plan-time tails, misses, and holds.
- [ ] Evaluate H14 versus longer candidate horizons using per-lead prediction
  quality and full-pipeline load, not future-rollout timing alone.
- [ ] Measure musical/perceptual outcomes separately from trajectory RMSE.

**Available:** A-D one-song/one-seed pilot; lower-age trajectory discrepancy
0.2281 to 0.2064 rad (about 9.5%).
**Blocked claims:** quality improved 9.5%; online equals offline; additive
percentages of the quality gap attributable to MRT2, timing, or tracking.

## P2: Execution and generalization

### T07. Tracking and reference delivery

- [ ] Compare native references and retargeted GT with generated trajectories
  under the same frozen SONIC protocol and independent initial-state resets.
- [ ] Control full/C4 preview and future-reference access, playback rate, root
  alignment, and timestamps; compare against actual online execution separately.
- [ ] Repeat arm/leg spectral, amplitude, dynamic, and event-retention analysis;
  report startup separately rather than only trimming it away.
- [ ] Determine whether attenuated high-frequency content is meaningful dance
  detail or jitter using GT controls and blinded viewing.

**Available:** A-D MuJoCo fixed-reference tracking, not four online inference runs.
**Blocked claims:** universal 40-ms tracker latency; all attenuation is harmful;
median joint velocity-power ratio is total physical energy.
**Optional, not implemented:** tracker-aware adaptation. If pursued, compare
with raw references and simple smoothing/clipping under a fixed controller;
do not relabel official SONIC as our new policy.

### T08. Cohort, reliability, and statistical protocol

- [x] Put existing three-model generator means into a primary-outcome matrix;
  leave matched execution outcomes explicitly missing rather than replacing
  them with the A--D one-song tracking diagnostics.
- [ ] PRIORITY: complete the same-cohort generated/executed MMR, beat/dynamic
  response, dance quality, and cross-paired music-fit results; add song-cluster
  uncertainty and independent blinded judgments. This is the central outcome
  evidence, ahead of expanding the diagnostic metric catalogue.
- [ ] Audit the per-model/per-song recording inventory and failed/incomplete
  runs before declaring a complete multi-model comparison.
- [ ] Freeze final songs not repeatedly used for tuning; verify style labels
  rather than infer cross-style diversity from song IDs.
- [ ] Distinguish training seeds, sampling seeds, windows, and tracker resets;
  report song-cluster uncertainty with repeats nested appropriately.
- [ ] Include aborted attempts and resource contention in reliability reports.
  Successful retries alone do not estimate deployment success probability.
- [ ] Keep formal 18-song matrices, smaller pilots, and codec experiments separate.

### T09. Metric calibration

- [ ] Complete and publish the three-block coverage matrix (MMR, music
  adaptation, dance quality/aesthetics) per cohort and gen/exec layer; mark
  unavailable or unvalidated endpoints N/A, not zero or silently omitted.
- [ ] Freeze MMR evaluator hash, feature/normalization versions, candidate pools,
  multiple-positive rules, crop length, and aligned one-second temporal segments.
  Do not label a global-only fallback as full MMR-MS; preserve the implemented
  square root of 0.7 global squared distance plus 0.3 temporal norm sum.
- [ ] Declare BAS direction, event extraction, smoothing, sigma, and any
  precision/recall matching tolerance. Do not impose one motion accent per beat
  or promote undefined Beat-F1 to a mandatory choreography score.
- [ ] Validate tempo/phase handling (including half/double tempo) and contact
  proxies before ranking models. Genre, phrase, and affect endpoints are optional;
  validate them if retained, otherwise narrow the associated claims.
- [ ] Keep learned FID/diversity and same-song multimodality in the dance-quality
  block, distinct from music--motion matching; report GT and sample counts.
- [ ] Close per-dataset gates for the multi-dataset evaluator, including the
  AIST++ song-level controls whose confidence intervals still cross zero.
- [ ] Keep music identity distinct from performance identity and avoid same-song
  false negatives; do not reintroduce superseded v2 numbers.
- [ ] Validate independent frozen metrics on GT and controlled corruptions;
  disclose contact proxies, feature-space differences, and FID sample limitations.
- [ ] Do not use generated-to-GT joint RMSE as a one-to-many choreography score.

### T10. Human evaluation and videos

- [ ] Separate silent-video naturalness/smoothness/expressiveness/aesthetics
  from soundtrack-on rhythm/dynamics/overall music fit; include cross-paired
  soundtrack controls and paired generated-versus-executed clips.
- [ ] Conduct blinded dance-quality, matched-audio musicality, and
  reference-versus-execution retention studies with randomized presentation.
- [ ] Match camera, rig, fps, duration, and audio time; preserve real playback speed.
- [ ] Treat songs and participants as repeated-measure units and predefine analysis.
- [ ] Separate labelled debugging grids and selected showcases from blinded evidence.

**Blocked claims:** better aesthetics or preserved expressive accents based
solely on low jerk, high BAS, or power retention.

### T11. Hardware and live-input scope (conditional)

- [ ] If retaining real-G1 claims, obtain actual hardware trials with a frozen
  protocol, full original recordings, failures, and interventions.
- [ ] If retaining unknown-live-audio claims, test microphone or causal stream
  changes, pauses, and music transitions rather than only paced WAV files.
- [ ] Otherwise explicitly limit claims to the tested paced-file MuJoCo setting.

Hardware is a claim-dependent gate, not a blanket requirement to train a new tracker.

## P3: Manuscript readiness

### T12. References, contributions, and final packaging

- [ ] Verify historical references and comparative technical claims against
  primary sources; confirm shared work attribution with Yukun.
- [ ] Align title, abstract, and contributions with completed evidence. Do not
  claim novelty or superiority merely because components are integrated.
- [x] Replace framework figures with editable native diagrams: both-branch FiLM,
  discrete-to-continuous conditioning, reference-derived state, separate fixed
  SONIC physical feedback, and latent-only CF target rebasing.
- [ ] Finalize authorship, venue-specific template, page budget, and reference format.
- [ ] Compress the expanded draft; visible review TODOs are not final paper content.
- [ ] Prepare reproducible public artifacts without assuming parent-workspace
  internal paths are accessible to readers.
- [ ] Review every T01--T12 gate; either attach evidence or narrow/remove its claim
  before switching `\showpapertodostrue` to `\showpapertodosfalse`.
