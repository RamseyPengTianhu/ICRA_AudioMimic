# Paper Decisions and Iteration Log

This file is the canonical record for paper-level narrative decisions. It
separates author decisions from available evidence and prevents unfinished
experiments from silently entering the manuscript.

Last reconciled: 2026-09-09

## Active decision override — ForeDance revision

The author-approved 2026-09-09 plan in ../PAPER_AUDIT_AND_REVISION_PLAN_20260909.md supersedes conflicting historical decisions below. The active narrative is anticipatory music conditioning for streaming dance, supported by kinematics-guided D+C representation and paired training, and Commit Forcing. Use ForeDance provisionally, a venue-neutral format, FineDance only, heard-versus-predicted music as the anticipation comparison, and CoF versus TF as the continuation comparison. FHC and MMR are supporting material. Do not add wrong-time tests, human blind evaluation, runtime tables, or new training launches. Keep evidence gaps explicit. D+C figures show full and structure-only reconstruction; corrupted-detail training stays in text.

## Historical decisions (preserved; overridden where conflicting)

## Current paper direction

### D-001 — Central contribution

- **Decision:** Commit Forcing remains the central method contribution.
- **Owner:** Author.
- **Paper consequence:** The abstract, introduction, method, experiments, and
  conclusion must describe one consistent deployment-closure story rather than
  presenting several equal contributions.
- **Status:** Approved in grill.

### D-002 — Main experimental battlefield

- **Decision:** The headline comparison is Commit Forcing versus Teacher
  Forcing. The paper tests whether training on committed generated history
  reduces the mismatch between training and deployment.
- **Owner:** Author.
- **Evidence boundary:** The existing final Commit-Forcing model and the
  existing Teacher-Forcing control are not yet a fully matched final
  comparison. No headline numerical claim is allowed until a matched control
  uses the same representation, parents, data, budget, seeds, and evaluation
  protocol.
- **Status:** Narrative approved; final result pending matched evidence.

### D-003 — Treatment of Two-Forward

- **Decision:** Do not print Two-Forward numbers in the paper's headline
  results. Cite Two-Forward as closely related work and explain the method-level
  difference that motivates Commit Forcing.
- **Scientific guardrails:**
  - Do not select only unfavorable Two-Forward runs or metrics.
  - Do not claim that Commit Forcing outperforms Two-Forward.
  - Do not imply that Two-Forward was unavailable or irrelevant.
  - Because the completed matched comparison shows a mixed trade-off, any broad
    superiority claim must be narrowed. The underlying evidence remains in the
    research repository even when its numbers are outside the paper's headline
    comparison.
- **Owner:** Author chose the battlefield; evidence guardrails are mandatory.
- **Approved wording boundary:** Keep the criticism out of the introduction.
  State it concisely in Related Work: Two-Forward constructs a hybrid context
  from teacher-conditioned first-pass predictions rather than training on a
  coherent trajectory produced by the deployment sampler. Contrast this with
  Commit Forcing's complete sample--commit--decode--state-update transition.
- **Status:** Direction and Related Work wording approved.

### D-004 — Music conditioning

- **Decision:** Music conditioning may enter the paper as a method only after
  its implementation description is stable. It must not enter the results,
  abstract evidence, or conclusion until evaluation is complete and supports a
  final interpretable finding.
- **Current evidence:** Training is substantially complete, but the evaluation
  pipeline has unresolved missing outputs and no accepted aggregate verdict.
- **Status:** Method-only candidate; result claims blocked.

### D-005 — Model and table selection

- **Decision:** The paper may report the strongest accepted Commit-Forcing
  mainline selected by a declared rule over completed candidates.
- **Fair-comparison boundary:** A comparison method must be represented by its
  canonical or fairly selected configuration under the declared protocol. A
  deliberately weak variation may appear only when it is clearly labeled as
  an ablation or failure analysis; it cannot stand in for the method as a
  whole.
- **Status:** Mainline-best direction approved; exact table awaits matched
  Teacher-Forcing evidence.

### D-006 — Post-revision experiment request

- **Decision:** After the manuscript has been fully reconciled, open one GitHub
  issue that lists every missing experiment and ablation as formal requests
  from the paper-writing side to the experiment side.
- **Timing:** Do not open the issue piecemeal. Build the request list during
  revision and publish it after all paper sections have been audited.
- **Status:** Completed after the full manuscript audit; published as
  [Musics2Dance issue #35](https://github.com/lbtwyk/Musics2Dance/issues/35).

### D-007 — Title timing

- **Decision:** Keep the current title during section-by-section revision. Make
  the final title decision only after the method, results, music scope, and
  supported claim have been reconciled.
- **Status:** Deferred by author.

### D-008 — Commit-Forcing novelty definition

- **Decision:** Define Commit Forcing through three coupled closures:
  deployment-sampler rollout, atomic structure--detail commitment, and decoded
  robot-state reconstruction.
- **Paper consequence:** The method must state that the final route reaches a
  fully generated history with no target-history floor, and that removing any
  closure restores a training context that differs from deployment.
- **Status:** Approved and drafted.

### D-009 — Motion-representation name and contribution

- **Decision:** Replace generic "factorized codec" language with
  "kinematics-guided coarse-to-fine motion decoupling." Describe the discrete
  branch as coarse motion structure and the continuous branch as finer motion
  detail.
- **Two-level scope:** The decoupling occurs in both the representation and its
  training. The latent explicitly separates discrete structure from continuous
  detail; forward-kinematics objectives and separate structure-classification
  and conditional-detail-generation objectives preserve those roles during
  learning. The two outputs are reunited for decoding and atomic commitment.
- **Terminology:** Use "kinematics-guided," not "dynamics-guided," because the
  supervision comes from forward kinematics rather than forces or torques. Do
  not introduce an extra branded acronym.
- **Paper consequence:** Treat this representation as the paper's second formal
  contribution, supported by the completed intervention audit.
- **Status:** Approved and drafted. The deferred title still keeps its old
  wording until the final title grill.

### D-010 — Placement of decoupling evidence

- **Decision:** Keep every completed numerical result from the matched
  coarse--fine decoupling audit in the main paper, rather than moving the
  detailed table to supplementary material.
- **Paper consequence:** The main text contains the full three-route,
  two-seed audit with reader-facing route names and a scoped interpretation of
  what the comparison establishes. The former summary chart is omitted because
  it duplicated the full table and added a page without adding evidence.
- **Status:** Superseded by D-011 after the author requested a concise,
  conference-style ablation table rather than a complete audit dump.

### D-011 — Representation-ablation table

- **Decision:** Replace the full audit table with a compact ablation table that
  tests the proof obligations of the method: whether the continuous branch is
  necessary and whether the proposed clean kinematics-guided objective
  strengthens the intended separation relative to the legacy overlapping
  objective.
- **Evidence admitted now:** D-only decoding of the selected codec, matched
  full-state codecs using the legacy and proposed objectives, and the selected
  compact-state representation. The legacy objective contains sparse-FK terms,
  so it must not be described as having no kinematic supervision.
- **Evidence boundary:** D-only decoding sets the continuous code to zero; it
  is not a separately trained pure-discrete model. No matched separately
  trained pure-discrete, pure-continuous, or direct motion-space generator has
  completed, so no numbers for those baselines enter the paper.
- **Status:** Approved in principle by author and drafted with the evidence
  boundary stated explicitly.

### D-012 — Long-horizon numbers before the matched baseline

- **Decision:** Remove the integrated-system long-horizon numbers until the
  matched Commit-Forcing versus Teacher-Forcing comparison is complete.
- **Paper consequence:** The method remains described, but the abstract,
  introduction, experiments, discussion, and conclusion make no numerical
  long-horizon claim for Commit Forcing.
- **Status:** Approved by author and drafted.

### D-013 — D-only evidence admitted before retrained baselines

- **Decision:** Keep the completed D-only decoding intervention in the main
  representation-ablation table. Label it explicitly as setting the continuous
  code to zero in the selected trained codec.
- **Claim boundary:** It shows that the continuous branch carries necessary
  complementary information within the selected D+C representation. It does
  not establish superiority over a separately trained pure-discrete model.
- **Required follow-up:** Request matched, separately trained pure-discrete,
  pure-continuous, and direct motion-space generators in the final experiment
  issue.
- **Status:** Approved by author.

### D-014 — Standard metrics for the matched main comparison

- **Decision:** The main Commit-Forcing versus Teacher-Forcing result will use
  established motion-generation metrics rather than project-specific
  diagnostics. The unconditional comparison will report kinetic and geometric
  motion FID together with the corresponding diversity measures, all computed
  with one declared extractor and one matched free-running protocol.
- **Music boundary:** Beat Alignment Score belongs only to the separately
  matched music-conditioned experiment. It is not applicable to an
  unconditional Commit-Forcing comparison.
- **Exclusions from the paper table:** Contact, grounding, root, endpoint,
  boundary-jerk, state-drift, and related project-specific diagnostics will not
  appear as manuscript metrics. They may remain internal acceptance checks and
  experiment-record evidence, but they cannot be renamed or substituted for
  standard paper metrics.
- **Evidence boundary:** The current repository implements kinetic/geometric
  diversity and beat-alignment evaluation, but it does not yet provide the
  complete standard kinetic/geometric FID protocol required for the final main
  table. No values enter the manuscript until that matched evaluation is
  implemented and completed.
- **Status:** Approved by author; experiment request and manuscript TODO
  updated.

### D-015 — Mechanism metrics retained with formal proof roles

- **Decision:** Choose option B. Keep the representation mechanism table while
  reserving standard FID, diversity, and Beat Alignment for final generated-
  motion quality. A mechanism-specific measure is admissible only when its
  intervention, normalization, direction, and supported claim are explicit.
- **Metric roles:** Structure NRMSE measures reconstruction fidelity in the
  frozen coarse-structure view; detail NRMSE measures fidelity in its exact
  complement; the D/C structure-effect ratio measures whether a discrete-code
  swap changes the structure view more than a continuous-code swap.
- **Degeneracy guard:** The effect ratio cannot stand alone. The D-only gap and
  the continuous-code effective rank must show that the ratio was not obtained
  by suppressing or collapsing the continuous branch. Confidence intervals
  must support the ratio being greater than one.
- **Claim boundary:** These measures establish representation roles and the
  effect of the kinematics-guided objective. They are not overall motion-
  quality metrics and cannot replace standard FID/diversity results.
- **Presentation change:** Replace the development-style labels `Struct.
  error`, `Detail error`, and `SD` with `Structure NRMSE`, `Detail NRMSE`, and
  the descriptive D/C structure-effect ratio $R_{D/C}$; define every quantity
  and its frozen evaluation view in the method and protocol.
- **Status:** Approved by author and drafted.

### D-016 — Keep the mechanism table compact

- **Decision:** Choose option A. Keep the representation table at three
  columns: structure NRMSE, detail NRMSE, and the D/C structure-effect ratio.
- **Non-collapse presentation:** Report the continuous-code effective rank in
  the immediately following text rather than adding a fourth table column.
  The D-only reconstruction gap remains the primary tabulated non-collapse
  evidence; effective rank is a supporting check.
- **Paper consequence:** The table stays readable in one conference column
  without weakening the degeneracy guard or duplicating evidence.
- **Status:** Approved by author; the current manuscript already follows this
  layout.

### D-017 — Standard metrics over the complete free-running horizon

- **Decision:** Choose option A. Both Commit Forcing and Teacher Forcing must
  generate matched 60-second free-running rollouts. Each rollout is divided
  into three non-overlapping 20-second windows, and all windows enter the same
  kinetic/geometric FID and diversity evaluation.
- **Why this remains standard:** The reported quantities remain standard
  fixed-window motion metrics. The long-horizon claim comes from covering every
  window of a deployment-length free-running rollout, not from introducing a
  project-specific stability score.
- **Fairness contract:** Sources, training seeds, sampling seeds, window
  boundaries, feature extractor, sample count, and aggregation must be matched
  between the two training methods. No method may contribute only its early or
  successfully completed windows.
- **Paper consequence:** The main table represents the full 60-second rollout
  distribution while retaining a standard 20-second evaluation unit.
- **Status:** Approved by author; manuscript TODO and experiment request
  updated.

### D-018 — Conventional diversity presentation without a real-data row

- **Decision:** Choose option B. The final main table will use the conventional
  kinetic-diversity and geometric-diversity upward arrows without adding a
  held-out real-motion reference row.
- **Interpretation guard:** Diversity cannot support a positive claim by
  itself. It is interpreted jointly with kinetic/geometric FID: higher
  diversity is favorable only when distributional quality is preserved rather
  than replaced by noise or implausible variation.
- **Claim boundary:** The paper may describe richer generated motion when the
  matched result improves diversity without a material FID regression. It may
  not describe the method as better merely because a diversity number is
  larger.
- **Status:** Approved by author; no manuscript layout change is required until
  the final result table is inserted.

### D-019 — Established features with a frozen G1 joint mapping

- **Decision:** Choose option A. Compute kinetic/geometric FID and diversity
  with the established canonical-skeleton feature definitions, using one
  frozen, documented mapping from native G1 forward-kinematic joints to the
  canonical joint roles.
- **Matched application:** Real held-out G1 motion, Commit-Forcing motion, and
  Teacher-Forcing motion must use the identical mapping, units, coordinate
  convention, temporal sampling, and extractor implementation.
- **No learned evaluator:** Do not train a new G1-specific feature encoder and
  do not tune the mapping against the compared results. Freeze the mapping and
  extractor provenance before evaluating either method.
- **Reproducibility requirement:** The final experiment artifact must record
  every joint correspondence, preprocessing transform, extractor source and
  version, and code/checksum provenance. A small equivalence test must verify
  that real and generated files follow the same conversion path.
- **Evidence boundary:** The current repository contains legacy canonical-
  skeleton feature code but not a fully validated native-G1-to-canonical
  mapping for this final protocol. No FID/diversity value enters the paper
  until that mapping and its validation are complete.
- **Status:** Approved by author; manuscript TODO and experiment request
  updated.

### D-020 — Compact uncertainty reporting

- **Decision:** Choose option A, with a minimal main-paper footprint. Pool all
  matched windows for the displayed FID/diversity point estimate. Compute a
  paired-bootstrap 95% interval for the Commit-Forcing minus Teacher-Forcing
  difference, resampling complete matched 60-second rollouts so their three
  windows remain one block.
- **Main-table notation:** Show no numeric interval in the main table. Add a
  dagger only to a Commit-Forcing value whose paired interval excludes zero;
  explain the dagger in one short caption note. Put full interval endpoints in
  supplementary material and the experiment artifact.
- **Claim rule:** A metric whose interval crosses zero receives no dagger and
  cannot be described as a stable improvement. The point estimate may still be
  reported without inflated language.
- **Status:** Approved by author; manuscript TODO and experiment request
  updated.

### D-021 — Separate headline comparison from mechanism ablations

- **Decision:** Choose option A. Keep the headline result table to two method
  rows: matched Teacher Forcing and full Commit Forcing. Place component-
  removal variants in a separate compact ablation table.
- **Proof roles:** The headline table establishes the complete method against
  its direct training baseline. The ablation table attributes any supported
  difference to deployment sampling, atomic structure--detail commitment,
  residual rebasing, and reconstructed-state closure.
- **Presentation rule:** Do not duplicate every ablation row in the headline
  table. Use the same standard metric definitions and uncertainty notation
  across both tables so the separation changes presentation, not the evidence
  contract.
- **Status:** Approved by author; manuscript TODO and experiment request
  updated.

### D-022 — Retrain every training-mechanism ablation

- **Decision:** Choose option A. Each component-removal variant must be trained
  as a separate matched model; evaluation-time switches on the full model do
  not count as paper ablations.
- **Frozen contract:** Start from the same eligible parents and hold data/cache
  identity, representation, initialization policy, optimization budget,
  training seeds, checkpoint selection rule, sampling seeds, and evaluation
  protocol fixed. The only intended intervention is the named removed
  mechanism.
- **Required variants:** Remove deployment-form sampling, atomic structure--
  detail commitment, residual rebasing, and reconstructed-state closure one at
  a time. Full Commit Forcing remains the shared control row.
- **Evidence boundary:** Evaluation-time toggles may remain diagnostic checks,
  but their numbers cannot enter the manuscript or support mechanism
  attribution.
- **Status:** Approved by author; manuscript TODO and experiment request
  updated.

### D-023 — Use the full standard metric set in the component table

- **Decision:** Choose option A. The compact component-ablation table will use
  the same four columns as the headline comparison: kinetic FID, geometric
  FID, kinetic diversity, and geometric diversity.
- **Reason:** Reporting both established feature families prevents selective
  presentation of only the kinetic or geometric view that favors a particular
  component. Five method rows by four metric columns remains compact enough for
  a conference table.
- **Exclusions:** Do not add contact, transition, state-drift, or other project-
  specific diagnostics to this paper table.
- **Status:** Approved by author; manuscript TODO and experiment request
  updated.

### D-024 — Evidence-gated component-table admission

- **Decision:** Choose option A for the dagger analysis, but decide whether to
  insert the component table only after the complete predeclared ablation set
  is finished. A dagger marks a paired degradation relative to full Commit
  Forcing when the rollout-block interval excludes zero.
- **All-or-none reporting:** If the completed rows form a coherent mechanism
  result that supports the paper's main line, insert the entire compact table
  and mark the supported cells. If they do not, omit the whole table from the
  main manuscript rather than selecting only favorable removals or metrics.
- **Claim consequence:** Omitting an unsupported table also requires removing
  or narrowing any statement that the individual components have been
  empirically proven necessary. Method description may remain, but mechanism
  attribution cannot outrun the evidence.
- **Evidence preservation:** All planned rows, point estimates, intervals, and
  contrary outcomes remain in the experiment artifact and final GitHub issue.
  Material counterevidence that changes the central claim must still be
  disclosed or reflected in the narrowed wording.
- **Status:** Approved by author; manuscript TODO and experiment request
  updated.

### D-025 — Guard music alignment with standard motion-quality metrics

- **Decision:** Choose option A. If the music-condition experiment closes, its
  table will report Beat Alignment Score together with kinetic FID, geometric
  FID, kinetic diversity, and geometric diversity.
- **Reason:** Beat alignment alone can reward repetitive or low-quality motion.
  The two standard FID views and two standard diversity views ensure that any
  claimed rhythm benefit is interpreted together with motion distribution and
  variety.
- **Scope:** These five columns are reserved for the matched music-conditioned
  study. Project-specific contact, drift, boundary, and transition diagnostics
  remain internal acceptance evidence rather than paper-table metrics.
- **Status:** Approved by author; manuscript TODO and experiment request
  updated.

### D-026 — Use one complete five-condition music table

- **Decision:** Choose option A. If the matched music experiment supports the
  paper's main line, the main manuscript will use one compact five-row table:
  exact-null music, observed music only, observed plus causal future
  prediction, time-shifted future prediction, and shuffled future prediction.
- **Proof roles:** Exact null shows the motion-parent reference; observed-only
  isolates reactive conditioning; observed plus causal future prediction is
  the proposed route; shifted and shuffled prediction test whether any gain
  depends on correctly timed future information rather than merely adding a
  second condition.
- **Admission:** Complete all five rows. Insert the full table only when the
  combined result forms a coherent, evidence-supported music claim. Otherwise
  retain the music interface as method only, omit the result table, and narrow
  or remove its effect claim.
- **Status:** Approved by author; manuscript TODO and experiment request
  updated.

### D-027 — Require a closed music-effect result, not universal metric wins

- **Decision:** Choose option A. Admit an empirical music contribution only if
  observed plus causal future prediction improves paired Beat Alignment over
  observed-only conditioning, does not incur a predeclared material
  degradation in kinetic/geometric FID or diversity, and the time-shifted and
  shuffled controls do not reproduce the alignment gain.
- **Claim boundary:** The four motion-quality metrics are guardrails, not four
  additional objectives that must all improve. A supported claim is that
  correctly timed causal future prediction improves music responsiveness
  without a material motion-quality cost, not that it dominates every metric.
- **Failure action:** If any part of this chain fails, do not select favorable
  cells. Keep the causal music interface as method only, omit the result table,
  narrow or remove its effect claim, and preserve the complete evidence in the
  experiment artifact and issue.
- **Status:** Approved by author; D-029 fixes the quality-guardrail test and its
  permitted wording.

### D-028 — Treat manuscript length as a soft drafting constraint

- **Decision:** Do not optimize the current draft around an exact page count.
  Preserve the complete scientific logic and evidence contract first, while
  avoiding unreasonable repetition or expansion. Final compression happens
  after the result set and title are settled.
- **Status:** Approved by author.

### D-029 — Use paired difference tests, not non-inferiority margins

- **Decision:** Choose option B. For each kinetic/geometric FID and diversity
  metric, compare causal-future conditioning with observed-only conditioning
  using the same paired complete-rollout block bootstrap. Treat a quality
  guardrail as failed when the paired 95% interval shows a significant
  deterioration in that metric.
- **Wording boundary:** Passing this test supports only “we observed no
  statistically significant degradation under the matched evaluation.” It
  does not establish equivalence, non-inferiority, or absence of a smaller
  quality cost.
- **Admission consequence:** A significant deterioration in any declared
  quality guardrail breaks the approved no-observed-quality-loss story; do not
  hide that metric or replace the complete table with favorable cells.
- **Status:** Approved by author; manuscript TODO and experiment request
  updated.

### D-030 — Use the same frozen music model within each seed

- **Decision:** Choose option B. Within every retained training seed, freeze one
  full observed-plus-causal-future music model and evaluate all five rows
  through matched inference-time interventions on that same model. Training-
  seed selection or aggregation is a separate reporting decision.
- **Interventions:** The proposed row receives correctly timed observed and
  predicted-future states. The observed-only row disables only the future
  state; shifted and shuffled rows replace only the future state; exact null
  disables both music states. Every row shares motion history, sampling seed,
  checkpoint, and rollout protocol.
- **Claim boundary:** This design tests whether the trained model uses correctly
  timed causal future information. It does not compare against a separately
  optimized observed-only model and therefore cannot support a claim that
  future-prediction training is universally better than observed-only
  training. Label the row “Observed only (future off),” not “Observed-only
  model.”
- **Status:** Approved by author; manuscript TODO and experiment request
  updated.

### D-031 — Keep the contract-fixed 100k music checkpoint

- **Decision:** Choose option B for checkpoint selection. Preserve the current
  music experiment contract: the final checkpoint is fixed at 100k updates;
  25k, 50k, and 75k remain learning-curve diagnostics and cannot be selected
  for the paper result.
- **Reason:** The author's “select the best” intent concerns seed selection,
  not retrospective checkpoint selection. Keeping 100k preserves the current
  experiment contract and separates that question cleanly from seed reporting.
- **Status:** Approved by author; seed type and reporting remain to be grilled.

### D-032 — Report one validation-selected training seed for music

- **Decision:** Choose option A. Select one best independently trained music
  seed on a separate validation split at the contract-fixed 100k checkpoint,
  then use that frozen seed for the five-condition main-paper table. Do not
  select a generation/sampling seed; aggregate every predeclared sampling seed
  within the selected model.
- **Main-paper presentation:** Keep the table to the selected training seed and
  do not discuss the other seed results in the main narrative. Include only the
  minimum provenance phrase “validation-selected training seed” in the
  protocol or caption.
- **Evidence preservation:** Preserve every trained seed, selection score, and
  final result in the supplementary artifact and GitHub issue. The paper may
  claim capability of the selected model, but not robustness across training
  seeds.
- **Status:** Approved by author; the validation selection score remains to be
  fixed before seed-level results are inspected.

### D-033 — Select the music seed with a quality gate, then Beat Alignment

- **Decision:** Choose option A. On the independent validation split, reject
  any 100k training seed for which the correct causal-future condition has a
  statistically significant deterioration in any declared kinetic/geometric
  FID or diversity metric relative to future-off. Rank only the remaining
  seeds by the predeclared Beat Alignment criterion.
- **No weighted score:** Do not combine the five paper metrics into a subjective
  weighted scalar. Motion metrics act as eligibility guardrails; Beat Alignment
  owns selection because the music experiment's proof role is rhythm response.
- **Failure action:** If no training seed passes every quality guardrail, no
  seed is eligible and the music result table remains out of the paper.
- **Status:** Approved by author; D-034 fixes the Beat Alignment quantity.

### D-034 — Select by paired future-condition gain

- **Decision:** Choose option A. For every quality-eligible 100k training seed,
  compute the paired Beat Alignment gain of the correctly timed causal-future
  condition over “Observed only (future off)” on the validation split. Require
  the correctly timed condition also to beat both time-shifted and shuffled
  future controls. Select the eligible seed with the largest paired future-off
  gain.
- **Reason:** The selection quantity now matches the music experiment's proof
  role: value attributable to correctly timed future information. Absolute Beat
  Alignment alone could select a model that is rhythmic but insensitive to the
  future condition.
- **Failure action:** If no seed has a positive supported future-off gain and
  separates from both timing controls while passing the four quality
  guardrails, no seed is eligible and no music result table enters the paper.
- **Status:** Approved by author; multiplicity handling for the three Beat
  Alignment contrasts remains to be fixed.

### D-035 — Use separate uncorrected Beat Alignment intervals

- **Decision:** Choose option B. Evaluate correct future timing separately
  against future-off, shifted, and shuffled conditions using three ordinary
  paired 95% complete-rollout block-bootstrap intervals. Do not apply Holm or
  another familywise correction.
- **Admission:** Each declared contrast must independently have its complete
  interval above zero for the seed to pass the timing gate.
- **Wording boundary:** Describe these as three nominal 5% paired tests. Do not
  claim that the joint familywise false-positive rate is controlled at 5%.
  Preserve all interval endpoints in supplementary evidence.
- **Status:** Approved by author; main-table significance notation remains to be
  fixed.

### D-036 — Use one compact music-timing significance marker

- **Decision:** Choose option A. Put one marker beside the admitted deployable
  route's Beat Alignment point estimate only when all three declared timing
  contrasts pass their separate paired intervals. Do not scatter per-cell
  significance symbols across the five-metric table.
- **Evidence detail:** Define the marker in the table note and place all three
  interval endpoints in supplementary evidence. The marker is determined on
  the final held-out test, not inherited from validation-based seed selection.
- **Status:** Approved by author; the exact row receiving the marker depends on
  the final route-table decision.

### D-037 — Latest-GitHub music audit supersedes the older simplified model

- **Observed source:** Refreshed GitHub on 2026-08-18: `prior-dev` is
  `ada0b03d451957c619ab0b5fc9831a0946e63933`; the live music branch
  `codex/v6f-ad-listenahead-mrt2` is
  `5d405c1d2f6ecd021c0c994515f32a55533e9e36`.
- **Observed method:** The current contract is ListenAhead-MRT2 with routes
  B0--B8. B1 supplies recent observed states as a separately trained past-only
  control. B5 supplies measured-age predicted native H14 states to the TAC
  route; B8 supplies the same predicted states through temporal concatenation.
  The current accepted contract does not feed a separate observed-state stream
  and predicted-future stream together as the manuscript presently says.
- **Observed evidence state:** All 21 B1--B7 seed trajectories reached 100k,
  but Wave C has only 736/771 durable receipts. B8 stopped around 72--73k and is
  non-promotable until exact resume to 100k. No music route is scientifically
  accepted, so no music number may enter the manuscript.
- **Consequence:** Decisions D-025--D-036 remain proposed paper-admission and
  presentation rules, not descriptions of a completed current experiment. The
  earlier same-model five-row simplification must be reconciled with the actual
  B0--B8 route matrix before it becomes an experiment request or paper table.
- **Status:** Evidence audit complete; manuscript method alignment is the next
  author decision.

### D-038 — Align the music method with predicted H14 conditioning

- **Decision:** Choose option A. Describe the deployable ListenAhead route as
  conditioning the frozen motion parent on 14 native 25-Hz MRT2 future states
  predicted from arrived audio, with physical timestamps and measured-age
  asynchronous snapshots. Do not describe separate observed and predicted
  streams as simultaneous inputs.
- **Baseline role:** Recent observed MRT2 states remain the separately trained
  past-only control. Static-now, oracle-future, injection-mechanism, and timing
  interventions retain their distinct proof roles in the live B0--B8 matrix.
- **Evidence boundary:** The method may be written now, but its effect remains
  unclaimed until B8 reaches 100k and the complete Wave C evidence is accepted.
- **Status:** Approved by author; abstract, formulation, architecture caption,
  method, discussion, conclusion, and music TODO updated.

### D-039 — Use a five-route headline music table from the frozen matrix

- **Decision:** Choose option A. If complete Wave C evidence admits a music
  result, the headline table will contain five reader-facing rows: no music,
  recent observed history, static current state repeated into the future,
  selected deployable predicted future, and oracle future.
- **Proof roles:** The rows show the unconditional reference, the value of
  prediction over past-only conditioning, the value of temporal evolution over
  a static state, the selected deployable system, and the upper bound imposed by
  forecast error.
- **Other routes:** Legacy interpolation, ideal-age snapshots, structure-only
  consumption, B5-versus-B8 injection, and detailed timing interventions move
  to one evidence-gated compact ablation or supplementary evidence. The single
  timing marker from D-036 may summarize the complete held-out intervention
  gate in the headline table.
- **Admission:** If no deployable route clears the complete evidence gate, omit
  the entire music result table and retain the predicted-future interface as
  method only.
- **Status:** Approved by author; the rule for selecting B5 TAC versus B8
  temporal-prefix injection remains to be fixed.

### D-040 — Select the deployable injection route from complete evidence

- **Decision:** Choose option A. Do not pre-fix timestamp-aware conditioning
  (B5) as the paper method. After B8 reaches 100k and both routes complete the
  identical Wave C protocol, select the deployable route under one predeclared
  validation rule.
- **Disclosure:** If a music result is admitted, report the complete matched
  B5-versus-B8 comparison in the injection-mechanism ablation even though only
  the selected route appears in the five-row headline table. Do not hide the
  unselected route or select different routes for different metrics.
- **Narrative consequence:** Keep the main method name injection-neutral until
  selection closes. If B8 is selected, rewrite the method around temporal-
  prefix injection; if B5 is selected, retain timestamp-aware conditioning.
- **Status:** Approved by author; the route-ranking and efficiency tie-break
  rule remains to be fixed.

### D-041 — Rank injection routes by rhythm value, then deployment cost

- **Decision:** Choose option A. B5 and B8 must first pass the same Beat
  Alignment, FID/diversity, timing-intervention, stability, and latency gates.
  Among eligible routes, prefer the one with the larger paired Beat Alignment
  gain over the observed-history control.
- **Efficiency tie-break:** If the paired B5-versus-B8 rhythm evidence does not
  clearly separate them, prefer the route with fewer trainable parameters and
  no worse measured deployment latency. The frozen contract records 2,020,352
  trainable parameters for B8 and 20,674,432 for B5.
- **No point-estimate shortcut:** A small point-estimate difference alone does
  not override an efficiency advantage. If one route fails an admission gate,
  it is ineligible regardless of its Beat Alignment point estimate.
- **Status:** Approved by author; whether route selection aggregates all
  training seeds or compares each route's selected best seed remains to be
  fixed.

### D-042 — Choose the injection mechanism across all training seeds

- **Decision:** Choose option A. Use the complete three-training-seed B5/B8
  evidence to select the injection mechanism. Do not compare only the best B5
  seed against the best B8 seed.
- **Sequence:** First apply the route gates and rhythm/efficiency rule to the
  full seed matrix. After one injection route is selected, apply the approved
  validation rule within that winning route to choose the single training seed
  shown in the headline table.
- **Reporting:** The injection-mechanism ablation preserves all three seeds for
  both routes. The main-table seed cannot retroactively change the selected
  injection mechanism.
- **Status:** Approved by author; the across-seed aggregation statistic remains
  to be fixed.

### D-043 — Aggregate B5/B8 at the training-seed level

- **Decision:** Choose option A. Within each training seed, compute each route's
  paired Beat Alignment gain over the observed-history control and the direct
  paired B5-versus-B8 difference. Rank routes by the median gain across the
  three training seeds and require at least two of three seeds to favor the
  same route.
- **No rollout pooling:** Do not treat all rollout windows from different
  training seeds as one flat sample. Sampling seeds and windows improve the
  estimate within a trained model but do not create additional independent
  training replications.
- **Tie handling:** If the seed-level evidence does not satisfy the agreed clear-
  winner rule, treat B5 and B8 as rhythm-tied and apply the approved parameter/
  latency tie-break rather than choosing from a pooled point estimate.
- **Status:** Approved by author; the seed-level clear-winner rule remains to be
  fixed.

### D-044 — Require seed-level intervals for a clear injection winner

- **Decision:** Choose option A. A B5/B8 rhythm winner is clear only when at
  least two of the three seed-specific paired complete-rollout bootstrap 95%
  intervals favor the same route and no seed-specific interval significantly
  favors the opposite route.
- **Tie:** Majority point estimates without the interval condition do not count
  as a mechanism win. Any 1--1 conflict, one significant seed with the other
  two unresolved, or two same-direction point estimates with intervals crossing
  zero is treated as a rhythm tie.
- **Consequence:** A clear rhythm winner advances if it passes every other
  admission gate. A rhythm tie invokes the parameter/latency rule from D-041.
- **Status:** Approved by author; the deployment-latency comparison remains to
  be defined.

### D-045 — Compare matched end-to-end per-commit p95 latency

- **Decision:** Choose option A. Measure B5 and B8 on the same hardware with the
  same parent, checkpoint update, sampling policy, motion history, forecast
  snapshot, warm-up, and commit count. Compare end-to-end per-commit p95 latency
  from snapshot lookup through condition assembly, structural generation, and
  continuous-detail generation.
- **Async boundary:** The background MRT2 rollout is a shared asynchronous
  condition-source cost and is not charged differently to B5 or B8. Preserve
  its measured snapshot-age evidence separately. The route comparison measures
  the synchronous planning path affected by the injection mechanism.
- **No average-only decision:** Mean conditioner latency may be reported as a
  diagnostic but cannot select the deployable route or establish deadline
  compliance.
- **Status:** Approved by author; the required real-time safety margin remains
  to be fixed.

### D-046 — Use the full 266.7-ms commit interval as the latency gate

- **Decision:** Choose option B. A deployable music route passes the real-time
  gate when its matched end-to-end per-commit p95 is below the full 266.7-ms
  execution interval. Do not impose the proposed 213-ms headroom threshold.
- **Wording boundary:** Passing supports only “met the tested planning deadline
  on the declared hardware.” It does not establish a 20% scheduling margin or
  robustness to additional system load and hardware variation.
- **Failure:** A route at or above 266.7 ms is ineligible for the deployable
  headline row regardless of its Beat Alignment or parameter count.
- **Status:** Approved by author; the priority between parameter count and p95
  among routes that both pass remains to be fixed.

### D-047 — Let parameter count break a rhythm tie after the latency gate

- **Decision:** Choose option A. End-to-end p95 is a hard eligibility gate, not
  the first ranking metric among routes that pass. If B5 and B8 are rhythm-tied
  and both remain below 266.7 ms, select the route with fewer trainable
  parameters.
- **Consequences:** If only one route meets the deadline, select that route if
  it passes every other gate. If both pass and rhythm is tied, B8's 2,020,352
  trainable parameters beat B5's 20,674,432. Still report both p95 values and do
  not claim that the selected route is faster unless the measured evidence says
  so.
- **Status:** Approved by author; placement of parameter and latency evidence in
  the paper remains to be fixed.

### D-048 — Keep efficiency out of the headline music table

- **Decision:** Choose option A. The five-route headline music table retains
  only Beat Alignment, kinetic/geometric FID, and kinetic/geometric diversity.
  Do not add parameter-count or latency columns.
- **Placement:** Report B5/B8 trainable parameters and matched end-to-end p95 in
  the separate injection-mechanism ablation, where they directly explain the
  route-selection tie-break.
- **Reason:** The headline table answers whether causal predicted future music
  helps rhythm without an observed standard-quality loss. Efficiency is a
  mechanism-selection result and would make the five-row table unnecessarily
  wide.
- **Status:** Approved by author; the injection-ablation column set remains to
  be fixed.

### D-049 — Use one complete two-row B5/B8 injection table

- **Decision:** Choose option A. If a music result is admitted, use one
  full-width two-row table comparing timestamp-aware conditioning and temporal-
  prefix injection.
- **Columns:** Beat Alignment, kinetic FID, geometric FID, kinetic diversity,
  geometric diversity, trainable parameters, and matched end-to-end per-commit
  p95 latency. Use standard up/down arrows and the same metric implementations
  as the headline music table.
- **Completeness:** Do not move B5/B8 FID or diversity to supplementary evidence
  while using the main paper to claim an injection winner. The table must expose
  the rhythm, quality, and efficiency evidence together.
- **Status:** Approved by author; whether table entries aggregate all training
  seeds or show selected seeds remains to be fixed.

### D-050 — Show each injection route's best selected training seed

- **Decision:** Choose option B. The two-row B5/B8 paper table reports each
  route's own validation-selected best 100k training seed rather than the
  across-seed median.
- **Separation from route choice:** D-042--D-044 still select the injection
  mechanism from the complete three-seed matrix. The best-seed table is a
  selected-system comparison and cannot replace that route-selection evidence.
- **Claim boundary:** The table may compare the two selected models but cannot
  establish cross-seed injection robustness. Preserve all seed-level values and
  intervals in supplementary evidence and the GitHub issue.
- **Status:** Approved by author; the seed policy for the other headline-table
  routes remains to be fixed.

### D-051 — Give every trained headline route its own best seed

- **Decision:** Choose option A. Recent observed history, static current state,
  the selected deployable predicted-future route, and oracle future each use
  their own validation-selected best 100k training seed under one common
  selection protocol. The unconditional frozen parent remains fixed.
- **Fairness:** Do not force independently trained route families to share one
  seed identifier, and do not give the proposed route a seed-selection option
  denied to its trained controls.
- **Claim boundary:** The headline table is a best-system comparison, not a
  mean-seed robustness table. Preserve every route/seed result outside the main
  narrative.
- **Status:** Approved by author; a common selection statistic that applies to
  observed, static, predicted, and oracle routes remains to be fixed.

### D-052 — Use aggressive proof-role-specific validation selection

- **Author intent:** Maximize the strongest defensible paper advantage rather
  than weakening every route into a mean-seed presentation.
- **Decision:** Each trained headline route may select its own best 100k seed on
  validation using the statistic that most directly matches that route's proof
  role. Recent observed history, static current state, and oracle future select
  for their strongest active-condition Beat Alignment after the common
  FID/diversity degradation gate. The deployable predicted-future route selects
  for its strongest paired advantage over the required causal controls after
  the timing and quality gates.
- **Aggressive presentation:** The main paper reports only these selected models
  and does not dilute the headline table with cross-seed means or variances.
  Full seed results and selectors remain in supplementary evidence and the
  GitHub issue.
- **Non-negotiable boundary:** Route-specific selectors must be frozen on
  validation before the final held-out table is opened. Do not retrospectively
  change a selector, metric, seed, route, or checkpoint after viewing final test
  outcomes. If the selected models do not support the bounded claim on final
  test, omit the result rather than reselecting.
- **Status:** Closest scientifically admissible implementation of the author's
  requested aggressive selection; the predicted-route control objective remains
  to be fixed.

### D-053 — Select the deployable seed by its strongest worst-control gain

- **Decision:** Choose option A. For every quality- and timing-eligible seed of
  the selected deployable route, compute paired Beat Alignment gains over both
  recent observed history and static current state. Rank seeds by the smaller
  of those two gains and select the seed that maximizes this minimum.
- **Admission:** The selected seed must retain positive supported gains against
  both controls on final held-out evaluation. A large advantage over only one
  control cannot carry the predicted-future claim.
- **Reason:** This is the most aggressive selector that still closes both
  required alternative explanations: benefit from prediction rather than past-
  only conditioning, and benefit from temporal evolution rather than added
  static conditioning capacity.
- **Status:** Approved by author; the oracle-future row's required relationship
  to the deployable route remains to be fixed.

### D-054 — Admit oracle future only as a genuine empirical ceiling

- **Decision:** Choose option A. The validation-selected oracle-future route may
  appear as “Oracle future upper bound” only when its held-out Beat Alignment
  point estimate matches or exceeds the selected deployable prediction route,
  its paired interval does not show it to be worse, and no declared FID or
  diversity metric significantly degrades.
- **Interpretation:** A passing oracle row quantifies remaining forecast-error
  headroom. An oracle condition that performs worse cannot be described as an
  upper bound or used to close the prediction-value mechanism.
- **No relabeling shortcut:** Do not retain a failed oracle row under upper-bound
  wording merely because it uses ground-truth future states.
- **Status:** Approved by author; whether an oracle failure removes the entire
  music result or only the oracle row remains to be fixed.

### D-055 — Narrow to a four-route result if oracle future fails

- **Decision:** Choose option B. If oracle future does not satisfy D-054, remove
  it from the headline table and retain a four-row result containing no music,
  recent observed history, static current state, and the selected deployable
  predicted-future route, provided that the deployable route still passes every
  approved rhythm, quality, timing, and latency gate.
- **Claim consequence:** Delete every claim that oracle future forms an upper
  bound, that forecast error explains the remaining gap, or that better future
  prediction necessarily offers additional headroom. The surviving claim is
  limited to the selected deployable route outperforming the two causal
  controls under the declared evaluation.
- **Evidence preservation:** Keep the complete failed oracle result in
  supplementary evidence and the GitHub issue. Do not delete or relabel it as a
  successful ceiling.
- **Status:** Approved by author; the minimum main-text disclosure of the oracle
  failure remains to be fixed.

### D-056 — Disclose an oracle failure once in Discussion

- **Decision:** Choose option A. If the four-row fallback is used, add one
  neutral Discussion sentence stating that ground-truth future conditioning did
  not form an empirical upper bound, so the supported claim is limited to the
  deployable prediction route versus observed-history and static-now controls.
  Point to complete supplementary results.
- **Placement:** Do not add this limitation to the abstract or introduction, and
  do not expand it into a general weakness of causal music prediction.
- **Status:** Approved by author; this sentence is inserted only if the failure
  condition actually occurs.

### D-057 — Bold the best point estimate in every headline metric

- **Decision:** Choose option B. In the admitted four- or five-row music table,
  bold the best point estimate in each of Beat Alignment, kinetic/geometric
  FID, and kinetic/geometric diversity according to the declared arrow
  direction.
- **Significance distinction:** The single timing marker remains separate and
  retains its D-036 meaning. Boldface denotes the best displayed point estimate
  only; it does not imply a statistically significant difference.
- **Status:** Approved by author; numeric precision remains to be fixed.

### D-058 — Use metric-appropriate compact numeric precision

- **Decision:** Choose option A. Display Beat Alignment to three decimal places;
  kinetic/geometric FID and diversity to two decimal places; trainable
  parameters in millions with two significant digits; and end-to-end p95 as
  integer milliseconds.
- **Evidence preservation:** Rounding applies only to paper display. Preserve
  full-precision values, differences, and interval endpoints in supplementary
  artifacts and never compute significance from rounded table entries.
- **Status:** Approved by author; headline rollout duration remains to be fixed.

### D-059 — Combine the declared 30- and 60-second music horizons

- **Decision:** Choose option B. The headline music estimate includes both
  matched 30-second and 60-second Wave C results rather than using 60 seconds
  alone.
- **Correlation handling:** Do not concatenate all frames or treat the two
  durations as independent samples. Compute every metric separately at each
  duration, keep the matched 30/60 pair from the same source, training seed, and
  sampling seed inside one bootstrap block, and combine the two horizon-level
  estimates only at aggregation.
- **Evidence detail:** Preserve the separate 30-second and 60-second values and
  intervals in supplementary evidence so a horizon-specific reversal remains
  visible.
- **Status:** Approved by author; relative weighting of the two horizons remains
  to be fixed.

### D-060 — Give 30- and 60-second music horizons equal weight

- **Decision:** Choose option A. Each displayed headline metric is the 50/50
  average of its separately computed 30-second and 60-second horizon-level
  estimate.
- **Bootstrap:** Keep both durations in the same source/seed block and recompute
  the equal-horizon average inside every resample. Do not average independently
  produced interval endpoints or weight by frame count.
- **Status:** Approved by author; treatment of a duration-specific reversal
  remains to be fixed.

### D-061 — Forbid a hidden Beat Alignment horizon reversal

- **Decision:** Choose option A. The selected deployable route's paired Beat
  Alignment gain over both observed-history and static-now controls must be
  positive separately at 30 seconds and 60 seconds, and the 50/50 combined
  paired test must pass.
- **Interpretation:** The individual horizon point estimates enforce consistent
  direction; significance is carried by the predeclared combined paired test.
  Do not use a positive average to hide a negative short- or long-horizon gain.
- **Failure:** A negative gain at either horizon blocks the combined headline
  music claim under this protocol.
- **Status:** Approved by author; horizon-specific handling of FID/diversity
  guardrails remains to be fixed.

### D-062 — Enforce quality guardrails at both horizons and combined

- **Decision:** Choose option A. For kinetic/geometric FID and diversity, the
  selected deployable route must show no statistically significant degradation
  relative to the required controls at 30 seconds, at 60 seconds, or in the
  50/50 combined estimate.
- **Failure:** A significant degradation in any declared metric at any of the
  three reporting levels blocks the no-observed-quality-loss music story. Do
  not use the combined average to mask it.
- **Wording boundary:** Passing still means only that no significant degradation
  was observed under these tests; it does not establish formal equivalence or
  non-inferiority.
- **Status:** Approved by author; final held-out source coverage remains to be
  fixed.

### D-063 — Reserve the eight Wave C windows for selection, not final reporting

- **Decision:** Choose option A. Use the current eight source-stratified Wave C
  windows only to complete route screening, mechanism selection, and each
  route's frozen validation selector. They are not the final paper test set.
- **Final-test rule:** After every displayed route and training seed is frozen,
  evaluate the selected four- or five-row headline comparison on a larger,
  separately fixed FineDance held-out test set. The final test set must be
  declared before its results are inspected, and it cannot be used to reselect
  a route, seed, checkpoint, or metric rule.
- **Evidence consequence:** Current Wave C completion alone cannot admit music
  numbers into the paper. The expanded held-out evaluation is a required
  missing experiment and will be included in the final GitHub issue.
- **Status:** Approved by author; the exact expanded-test-set coverage remains
  to be fixed.

### D-064 — Evaluate every eligible held-out FineDance track

- **Decision:** Choose option A. The expanded final music evaluation uses every
  eligible FineDance held-out track that supports the predeclared matched
  60-second generation protocol; it is not a smaller hand-picked subset.
- **Freeze rule:** Build and checksum the complete source manifest before any
  final paper metric or render is inspected. All selected systems use the same
  manifest and matched sampling conditions.
- **Interpretation:** This maximizes source coverage and prevents style or song
  selection from being used to strengthen the reported result after the fact.
- **Status:** Approved by author; mechanical track-eligibility and exclusion
  rules remain to be fixed.

### D-065 — Centralize favorable-result selection disclosure in Discussion

- **Author decision:** Main-paper quantitative tables may present post-hoc
  selected favorable completed runs or cases. Repeated selection labels do not
  appear beside each table; one unified scope note appears in the final
  Discussion instead.
- **Mandatory unified note:** The note must say plainly that the quantitative
  tables use post-hoc favorable selection rather than aggregate performance on
  the full held-out set. It must also state that the tables demonstrate
  attainable behavior under selected conditions and do not estimate average or
  overall FineDance performance.
- **Record boundary:** Preserve every evaluated outcome, exclusion, and exact
  selection rule in the experiment ledger and internal decision record. Main
  text may omit those details, but it may not call the selected tables full-set
  or dataset-level results.
- **Relationship to D-064:** All eligible held-out tracks are still evaluated
  and retained. D-065 changes which completed evidence is displayed in the
  compact main-paper tables, not which outcomes exist in the scientific record.
- **Status:** Approved by author under the unified-disclosure condition; the
  within-table selection unit remains to be fixed.

### D-066 — Allow each method to use its own favorable case set

- **Decision:** Choose option A. Within a quantitative table, each method may
  report its own post-hoc selected favorable completed cases. The repeated
  selection qualification appears only in the unified final Discussion note,
  not beside individual tables.
- **Statistical consequence:** Because rows no longer evaluate the same cases,
  their numerical differences cannot identify a method effect. These tables
  may show each method's selected attainable behavior, but cannot support
  cross-row superiority, significance, winner bolding, or causal attribution.
- **Required final note:** State that methods may use different favorable case
  sets, that the displayed values are not matched comparisons, and that no
  dataset-level or cross-method inference should be drawn from row differences.
- **Record boundary:** Retain the complete full-set outcomes and the exact case
  set behind every displayed cell or row in the experiment ledger.
- **Status:** Approved by author; existing comparative tables and prose now
  require a presentation decision consistent with this rule.

### D-067 — Use one shared favorable case set within each metric

- **Decision:** Choose option A, superseding D-066. Different metrics may use
  different post-hoc selected favorable case sets, but every method compared
  within one metric must use the identical cases and sampling conditions.
- **Presentation:** The main text may compare methods, bold winners, and analyze
  the displayed differences within that selected metric-specific case set. The
  repeated selection qualification remains centralized in the final Discussion
  note rather than appearing beside every table.
- **Claim boundary:** A displayed difference supports performance on the
  selected cases for that metric, not average or full-set performance. Formal
  significance additionally requires independent evaluation data after case
  selection or a selection-aware uncertainty procedure.
- **Existing evidence:** The completed representation ablation retains its
  current matched comparison, winner bolding, and mechanism interpretation.
- **Record boundary:** Keep full-set outcomes and each metric's exact shared
  selected manifest in the experiment ledger.
- **Status:** Approved by author; selection-versus-evaluation data reuse remains
  to be fixed.

### D-068 — Separate favorable-case selection from reported sampling evidence

- **Decision:** Choose option A. Dedicate one predeclared sampling seed to
  selecting each metric's favorable shared case set. After that set is frozen,
  compute the main-paper point estimates, paired intervals, significance marks,
  and qualitative verdicts only from the other two sampling seeds.
- **Matching rule:** The same case manifest selected for one metric is applied
  to every method in that metric. Selection outputs never enter the displayed
  estimate or its bootstrap blocks.
- **Claim boundary:** This supports comparative claims and ordinary paired
  uncertainty on the selected setting, not on average or full-set FineDance
  performance. The unified Discussion note carries that scope once.
- **Record boundary:** Preserve selection-seed scores, frozen manifests,
  evaluation-seed scores, and the aggregation code in the experiment ledger.
- **Status:** Approved by author; the fixed selection-seed identity remains to
  be chosen.

### D-069 — Select a different screening seed per metric on Wave C

- **Decision:** Choose option B. For each reported metric, inspect all three
  sampling seeds on the existing Wave C selection windows and choose the seed
  that best serves that metric's favorable-case screening objective.
- **Freeze boundary:** Freeze the metric-to-selection-seed assignment before
  opening the expanded FineDance final evaluation. On the expanded set, that
  seed may select the shared favorable cases but cannot enter displayed values
  or intervals; the other two seeds alone produce paper estimates.
- **Prohibition:** Do not choose or revise the selection-seed identity after
  viewing expanded-test outcomes. Doing so would reuse final evidence and
  invalidate the planned ordinary paired intervals.
- **Record boundary:** Store the complete Wave C seed comparison, frozen
  assignment, selected manifest, and two-seed final estimates.
- **Status:** Approved by author; the metric-specific screening objective
  remains to be fixed.

### D-070 — Select screening seeds by comparative margin

- **Decision:** Choose option A. For each metric on Wave C, select the sampling
  seed that maximizes the proposed method's paired advantage over the strongest
  required baseline, not the seed that merely gives the proposed method its
  best absolute score.
- **Direction:** For kinetic/geometric FID, maximize the baseline-minus-proposed
  reduction. For Beat Alignment and the declared diversity columns, maximize
  proposed-minus-baseline improvement.
- **Baseline rule:** The strongest required baseline is determined within the
  comparison's predeclared control set. Teacher Forcing is the required
  unconditional baseline; the deployable music route must clear both
  observed-history and static-now controls, so its screening margin is the
  smaller of those two paired gains.
- **Freeze boundary:** Compute this choice only on Wave C and freeze it before
  expanded testing. Final-test results cannot alter either the seed or the
  baseline used for selection.
- **Status:** Approved by author; the minimum favorable-case-set size remains to
  be fixed.

### D-071 — Retain the best quarter with at least eight source tracks

- **Decision:** Choose option A. For each metric, select the source tracks with
  the largest correctly oriented paired advantage until the best 25\% of the
  eligible expanded-test manifest is retained, with a hard minimum of eight
  distinct tracks.
- **Rounding:** Round the 25\% count upward, then apply the maximum of that count
  and eight. If fewer than eight tracks are eligible, the metric is not
  admissible as a paper-level quantitative result under this protocol.
- **Matching rule:** Use the identical selected source manifest for every method
  compared within that metric and retain complete 30- and 60-second blocks for
  each selected source.
- **Interpretation:** The main table remains deliberately focused on the most
  favorable quarter, while avoiding a single-song or single-window showcase
  masquerading as a distributional metric.
- **Status:** Approved by author; whether 30- and 60-second horizons share one
  selected manifest remains to be fixed.

### D-072 — Select separate favorable source sets by horizon

- **Decision:** Choose option B. For every metric, select the most favorable
  25\% source tracks independently at 30 seconds and 60 seconds, with at least
  eight distinct tracks in each horizon-specific set. The two manifests may
  differ.
- **Matching rule:** Within one metric and horizon, every compared method uses
  exactly the same selected sources and sampling conditions.
- **Aggregation:** Compute point estimates and paired method differences
  separately at each horizon. Bootstrap sources independently within the
  30-second and 60-second selected manifests, then average matched method-
  difference draws 50/50 to obtain the combined interval. Do not call the two
  source manifests matched duration pairs.
- **Claim boundary:** The combined result summarizes two separately selected
  favorable horizon settings; it does not estimate one shared source
  population across durations. The unified Discussion note states this once.
- **Status:** Approved by author; whether the selection-seed identity is shared
  across horizons remains to be fixed.

### D-073 — Share one metric-specific screening seed across horizons

- **Decision:** Choose option A. Each metric has one Wave-C-selected screening
  seed, and that same seed performs favorable-source selection independently at
  both 30 seconds and 60 seconds.
- **Evaluation split:** The other two sampling seeds remain evaluation-only at
  both horizons and alone produce all displayed values, horizon-specific
  intervals, and the equal-horizon aggregate.
- **Reason:** Do not let a seed act as selection evidence at one horizon and
  final evaluation evidence at the other, because the two rollouts are related
  and would weaken the claimed separation between screening and estimation.
- **Status:** Approved by author; the source-subset optimization procedure for
  distributional metrics remains to be fixed.

### D-074 — Use deterministic backward elimination for set-level metrics

- **Decision:** Choose option A. For FID and diversity, begin with every
  eligible source and use the metric's screening seed to remove one source at a
  time. At each step remove the source whose removal produces the largest
  correctly oriented set-level margin over the strongest required baseline.
- **Stop rule:** Stop at the D-071 target: the larger of the upward-rounded top
  25\% count and eight distinct sources.
- **Determinism:** Recompute the actual distributional metric after each
  candidate removal. Break exact objective ties by stable source identifier;
  do not use a per-track proxy, random restart, or manual override.
- **Record boundary:** Save the full elimination path, set-level score after
  every step, final manifest, extractor identity, and code revision.
- **Status:** Approved by author; component-table source reuse remains to be
  fixed.

### D-075 — Give the component table its own favorable manifests

- **Decision:** Choose option B. Do not reuse the headline Commit-Forcing-
  versus-Teacher-Forcing source manifests. For every component-table metric and
  horizon, independently select the favorable top-quarter manifest that
  maximizes full Commit Forcing's correctly oriented margin over the strongest
  displayed component removal.
- **Matching rule:** Apply that manifest to full Commit Forcing and every
  separately trained removal in the component table. Do not choose a different
  source set for each removal.
- **Selection split:** Use a validation-only screening seed and deterministic
  backward elimination for FID/diversity; reserve the other two sampling seeds
  for displayed values and intervals exactly as in the headline protocol.
- **Proof role:** The headline table selects evidence for overall value against
  Teacher Forcing. The independent component table selects evidence for
  mechanism attribution against the strongest removal.
- **Status:** Approved by author; the component-table admission threshold
  remains to be fixed.

### D-076 — Require a clean four-metric component-table win

- **Decision:** Choose option A. Admit the component-ablation table to the main
  paper only when full Commit Forcing ranks best against every displayed
  separately trained removal in kinetic FID, geometric FID, kinetic diversity,
  and geometric diversity.
- **All-or-none rule:** Keep the full predeclared removal set and all four
  columns together. If any removal matches or exceeds the full method in any
  column, omit the entire component table rather than dropping that row or
  metric.
- **Claim consequence:** After omission, retain only architectural descriptions
  whose evidence does not depend on the missing component comparison and move
  the unresolved mechanism tests to the final experiment issue.
- **Status:** Approved by author; the required significance pattern remains to
  be fixed.

### D-077 — Require one supported loss per removal and no reversal

- **Decision:** Choose option B. Full Commit Forcing must retain the best point
  estimate in all four standard columns against every removal. Each removal
  must additionally be significantly worse than the full method in at least
  one column, while no column may significantly favor that removal.
- **Interval rule:** Use the approved paired evaluation-seed bootstrap on the
  component table's selected shared manifest. A significant loss means the
  corresponding 95\% difference interval excludes zero in the declared adverse
  direction; a significant reversal excludes zero in the opposite direction.
- **Admission:** A removal with four non-significant differences fails the
  component-necessity requirement even if its point estimates are worse. Any
  significant reversal fails the entire all-or-none component table.
- **Claim boundary:** The table supports that every declared component has a
  measurable role on at least one standard outcome in the selected setting; it
  does not claim that every component improves every metric significantly.
- **Status:** Approved by author; compact significance-marker placement remains
  to be fixed.

### D-078 — Mark every significant component cell

- **Decision:** Choose option B. Place a dagger directly beside every component-
  table metric value whose paired 95\% interval significantly favors full
  Commit Forcing over that removal.
- **No row shortcut:** Do not replace cell-level markers with one dagger beside
  the row name. A reader should see which standard outcomes provide evidence
  for each component.
- **Supplement:** Preserve the exact intervals for every cell, including non-
  significant differences, outside the compact main table.
- **Status:** Approved by author; multiple-comparison handling remains to be
  fixed.

### D-079 — Use uncorrected cell-wise component intervals

- **Decision:** Choose option A. Determine every component-table dagger from
  its own ordinary paired 95\% interval. Do not adjust the four metric
  intervals for familywise error within a removal row.
- **Wording:** A dagger means only that the declared cell-wise interval excludes
  zero in the adverse direction for that removal. Do not claim that a removal
  row or the complete table is jointly significant.
- **Admission compatibility:** D-077 still requires at least one marked cell per
  removal and no cell-wise significant reversal. Full intervals for marked and
  unmarked cells remain in supplementary evidence.
- **Status:** Approved by author; main-table horizon presentation remains to be
  fixed.

### D-080 — Show only equal-horizon component aggregates in the main table

- **Decision:** Choose option A. The main component-ablation table retains four
  columns only: equal-weight 30-/60-second kinetic FID, geometric FID, kinetic
  diversity, and geometric diversity.
- **Supplement:** Report the separate 30-second and 60-second point estimates
  and paired intervals for every full-method/removal comparison outside the
  main table.
- **Marker:** A main-table dagger is determined from the approved combined
  horizon-level difference distribution, not from one favorable horizon alone.
- **Status:** Approved by author; horizon-specific reversal handling remains to
  be fixed.

### D-081 — Block component-table horizon reversals

- **Decision:** Choose option A. For every full-method/removal metric cell, full
  Commit Forcing must retain the correctly oriented point-estimate advantage
  separately at 30 seconds and 60 seconds.
- **Failure:** A wrong-direction point estimate at either horizon blocks the
  complete component table, even when the 50/50 aggregate favors the full
  method. Any significant reversal at either horizon also blocks admission.
- **Significance:** The D-077 requirement of at least one significant loss per
  removal is still judged from the compact combined columns; horizon-specific
  intervals act as reversal guards and remain in supplementary evidence.
- **Status:** Approved by author; the component-table protocol is closed.

### D-082 — Require real-G1 execution evidence before submission

- **Decision:** Choose option A. Add a completed real-G1 execution study to the
  submission requirements and to the final consolidated GitHub experiment
  issue.
- **Current boundary:** Until the study is run, evaluated, and scientifically
  accepted, keep every current claim scoped to robot-native reference-motion
  generation. Do not claim hardware execution, controller robustness, or
  closed-loop deployment from simulation or reference renders.
- **Admission:** Hardware text and results enter the paper only after matched
  controller conditions, safety review, quantitative evaluation, and
  representative videos are complete. A prepared or attempted run is not
  sufficient.
- **Status:** Approved by author; the minimum hardware comparison remains to be
  fixed.

### D-083 — Use qualitative real-G1 feasibility evidence only

- **Decision:** Choose option B. The required real-G1 study consists of selected
  representative execution videos without a matched quantitative hardware
  comparison against Teacher Forcing.
- **Proof role:** The videos may establish that selected robot-native reference
  sequences can be executed on the physical G1 under the frozen controller and
  safety protocol.
- **Claim boundary:** Do not claim improved hardware stability, tracking,
  success rate, controller robustness, or closed-loop superiority over Teacher
  Forcing. The quantitative Commit-Forcing claim remains supported by the
  reference-generation evaluation, not the qualitative hardware showcase.
- **Record:** Retain full uncut captures, controller/config identity, safety
  interventions, selected video list, and the selection rationale.
- **Status:** Approved by author; minimum video coverage remains to be fixed.

### D-084 — Use one strongest real-G1 hero execution

- **Decision:** Choose option B. Require one selected strongest representative
  real-G1 execution rather than three style-diverse videos.
- **Proof role:** The hero video demonstrates physical feasibility for that
  selected sequence only. It does not establish coverage across music styles,
  execution success rate, or representative hardware performance.
- **Selection record:** Preserve every candidate capture, failed or interrupted
  attempt, controller/config identity, and the rule used to choose the displayed
  hero video outside the main paper.
- **Status:** Approved by author; continuity and editing rules remain to be
  fixed.

### D-085 — Allow an edited real-G1 highlight

- **Decision:** Choose option B. The single real-G1 hero asset may be a shorter
  edit assembled from the strongest moments rather than one uncut continuous
  60-second execution.
- **Proof role:** The edit may demonstrate local physical plausibility of the
  selected motions on G1. It cannot establish uninterrupted 60-second
  execution, long-horizon hardware stability, recovery, or end-to-end success.
- **Record:** Preserve the complete unedited source captures, timestamps of
  every included segment, playback-rate operations, cuts, and interventions.
- **Status:** Approved by author; minimum shot length and playback integrity
  remain to be fixed.

### D-086 — Preserve real-time playback and visible continuous shots

- **Decision:** Choose option A. The edited G1 hero video uses real-time
  playback, visible cuts, and shots of at least five continuous seconds.
- **Integrity:** Do not use speed changes to strengthen apparent stability or
  motion quality. Preserve the original synchronized footage and exact edit
  list.
- **Delegation:** Routine video, table, symbol, ordering, and formatting details
  are now resolved by the writer under the already approved contribution-first,
  favorable-selection, centralized-disclosure, and complete-record rules. Grill
  the author only for decisions that materially change a claim, central table,
  or major experiment requirement.
- **Status:** Approved by author; hardware presentation details are closed.

### D-087 — Keep Commit Forcing on the 60-second battlefield

- **Decision:** Choose option A. The headline Commit-Forcing-versus-Teacher-
  Forcing table and its component-ablation table use 60-second free-running
  rollouts only, evaluated through all three non-overlapping 20-second windows.
  Do not add an independent 30-second Commit-Forcing experiment.
- **Scope correction:** The equal-weight 30-/60-second protocol and separately
  selected horizon manifests remain specific to the music study. D-072 and
  D-073 are scoped accordingly. D-080 and D-081 are superseded for the
  Commit-Forcing component table.
- **Component guard:** The four component columns summarize the 60-second
  protocol. Full Commit Forcing must keep the correct direction in each window
  position and no window-specific interval may significantly reverse.
- **Reason:** This directly tests the long-horizon deployment-history problem,
  keeps the strongest battlefield, and avoids adding a redundant shorter
  Commit-Forcing study.
- **Status:** Approved by author; horizon inconsistency resolved.

### D-088 — Use a concise provisional title

- **Decision:** Use “AudioMimic: Commit Forcing for Causal Streaming Humanoid
  Dance” as the current working title.
- **Scope:** The title leads with the central contribution and avoids promoting
  incomplete music evidence. Kinematics-guided coarse-to-fine decoupling
  remains the second contribution in the paper body.
- **Status:** Provisional by author; revisit once final matched results are
  available and before submission.

### D-089 — Publish the consolidated experiment request

- **Decision:** Publish one paper-facing request covering every missing matched
  comparison, ablation, music evaluation, and physical-feasibility artifact.
- **Relationship to active work:** The consolidated request does not replace
  music issue #33; that issue remains the execution ledger for the B0--B8
  ListenAhead-MRT2 study.
- **Status:** Published as
  [Musics2Dance issue #35](https://github.com/lbtwyk/Musics2Dance/issues/35).

### D-090 — Keep TODOs inside the manuscript draft

- **Decision:** Restore visible TODO blocks at the exact sections they affect.
  Use one draft switch so the same source can render either the annotated draft
  or a clean submission copy without maintaining two manuscripts.
- **Status:** Applied; the current default is the annotated draft.

## Evidence admission rules

A result enters the paper only when all of the following are true:

1. The compared systems follow a declared and fair comparison contract.
2. Training, evaluation, qualitative review, and aggregation are complete.
3. The result has one clear proof role in the paper's central story.
4. The wording matches the actual scope of the evidence.
5. Material limitations that change the claim are stated without turning local
   trade-offs into a global failure.

Incomplete work may support a method description, but not an empirical claim.

## Planned manuscript iterations

| Order | Proposed change | Evidence state | Grill state |
|---:|---|---|---|
| 1 | Rewrite the title-level claim, abstract, and introduction around deployment-closed Commit Forcing versus Teacher Forcing | Method is supported; final matched comparison is missing | Abstract and introduction drafted; concise working title selected provisionally |
| 2 | Update the Commit-Forcing method to match the final atomic generated-commit and reconstructed-state procedure | Implementation supported | Completed |
| 3 | Present kinematics-guided coarse-to-fine motion decoupling as the second formal contribution, using a concise necessity-and-training ablation | Completed component and objective evidence; separately trained pure D/C and motion-space controls are missing | Current table approved; stronger controls queued |
| 4 | Reframe Two-Forward as related work and explain its remaining method-level gap without numerical comparison or superiority language | Literature and implementation supported | Completed |
| 5 | Add the stable music-conditioning method, clearly separated from the unconditional Commit-Forcing result | Current B0--B8 implementation reconciled; final evaluation incomplete | Method completed; results withheld |
| 6 | Replace legacy result claims with the matched Commit-Forcing versus Teacher-Forcing evaluation | Fair final control missing | Blocked on evidence |
| 7 | Rewrite the discussion and conclusion to make only the final supported claim | Current evidence boundary known; final numerical update depends on item 6 | Draft completed; final result insertion blocked |
| 8 | Add one selected edited real-G1 feasibility video under the approved playback and claim boundaries | Physical capture not yet accepted | Queued for final experiment issue |

## Iteration history

| Date | Iteration | Decision or change | Result |
|---|---|---|---|
| 2026-08-18 | I-001 | Reconciled the paper with the latest code mainline and active music branch | Commit Forcing retained as the paper center; music results withheld |
| 2026-08-18 | I-002 | Applied contribution-first writing rules | Global metric dominance is not required; the claim must be bounded and evidence-backed |
| 2026-08-18 | I-003 | Chose Teacher Forcing as the headline comparison | A new matched final control is required before numerical rewriting |
| 2026-08-18 | I-004 | Chose not to print Two-Forward numbers in the paper | Selective unfavorable reporting is prohibited; no claim over Two-Forward is allowed |
| 2026-08-18 | I-005 | Rewrote the abstract and introduction around Commit Forcing versus Teacher Forcing | Removed premature comparative and music-effect claims; retained completed mainline feasibility as supporting evidence |
| 2026-08-18 | I-006 | Established the post-revision experiment-request workflow | One GitHub issue will collect all missing experiments after the full manuscript audit |
| 2026-08-18 | I-007 | Added the approved concise Two-Forward limitation to Related Work only | The introduction remains focused on the general deployment-history problem |
| 2026-08-18 | I-008 | Deferred the title decision | The current title remains unchanged until the full paper story is settled |
| 2026-08-18 | I-009 | Rewrote the Commit-Forcing method around three coupled closures | Deployment sampling, atomic commitment, and decoded state reconstruction are now the explicit novelty |
| 2026-08-18 | I-010 | Renamed and reframed the motion representation | Coarse structure comes from the discrete branch, finer detail from the continuous branch, and forward kinematics decouples their roles |
| 2026-08-18 | I-011 | Completed the two-level decoupling story | The paper now explains representation-level separation, training-level supervision and generators, and joint commitment |
| 2026-08-18 | I-012 | Added the complete decoupling audit to the main paper | All three matched representation routes and every completed metric are reported with reader-facing names and scoped interpretation |
| 2026-08-18 | I-013 | Removed the redundant decoupling summary chart | The complete table retains every value while avoiding an extra page of duplicate evidence |
| 2026-08-18 | I-014 | Replaced the audit dump with a compact representation ablation | The paper now reports four direct rows and three proof-relevant metrics with rounded values |
| 2026-08-18 | I-015 | Withheld unmatched long-horizon and music-system numbers | Commit Forcing and music remain method claims until their final matched controls are complete |
| 2026-08-18 | I-016 | Retained the completed D-only decoding ablation | Its claim is limited to branch necessity within the selected codec; retrained representation baselines remain required |
| 2026-08-18 | I-017 | Fixed the main comparison to standard conference metrics | The future unconditional Commit-Forcing versus Teacher-Forcing table will use kinetic/geometric FID and diversity; Beat Alignment is reserved for the music study, while contact and internal diagnostics stay out of paper tables |
| 2026-08-18 | I-018 | Retained and formalized the representation mechanism table | Each column now has one proof role, a complete definition, a fixed normalization and intervention contract, a non-collapse guard, and an explicit boundary from standard task-quality metrics |
| 2026-08-18 | I-019 | Kept effective rank outside the compact table | The three-column table carries the primary reconstruction and intervention evidence; continuous-code rank remains an adjacent non-collapse check |
| 2026-08-18 | I-020 | Fixed the long-horizon standard-metric protocol | Both methods must free-run for 60 seconds; all three non-overlapping 20-second windows enter the matched FID and diversity evaluation |
| 2026-08-18 | I-021 | Chose conventional diversity arrows without a real-data row | Diversity remains a standard main-table metric but can support a positive claim only when interpreted jointly with FID |
| 2026-08-18 | I-022 | Fixed the standard feature space and G1 conversion rule | Standard kinetic/geometric features will use one frozen documented G1 FK-to-canonical mapping for real and generated motion; no learned project-specific evaluator is allowed |
| 2026-08-18 | I-023 | Added compact paired uncertainty reporting | The main table keeps one number per metric and uses only a dagger for intervals excluding zero; full block-bootstrap intervals move to supplementary evidence |
| 2026-08-18 | I-024 | Split headline results from component ablations | The main table contains only matched Teacher Forcing and full Commit Forcing; mechanism removals receive a separate compact table |
| 2026-08-18 | I-025 | Required separately trained component ablations | Each removal must use the same parents, data, budget, seeds, selection, sampling, and evaluation as full Commit Forcing; inference-only toggles are diagnostic only |
| 2026-08-18 | I-026 | Fixed four standard columns for the component table | Every component row will report kinetic/geometric FID and diversity, preventing selective use of only one feature family |
| 2026-08-18 | I-027 | Made the component table evidence-gated and all-or-none | The full predeclared table enters the paper only if it supports a coherent mechanism claim; otherwise it is omitted and component-level claims are narrowed, while all results remain recorded |
| 2026-08-18 | I-028 | Added motion-quality guardrails to the music evaluation | Beat Alignment will be reported together with kinetic/geometric FID and diversity, preventing a rhythm-only result from carrying the music claim |
| 2026-08-18 | I-029 | Fixed one complete five-condition music table | Null, observed-only, causal future, shifted-future, and shuffled-future rows will appear together only if the completed table supports a coherent music claim |
| 2026-08-18 | I-030 | Fixed the music-effect admission logic | Beat Alignment is the primary improvement; standard motion metrics are quality guardrails, and shifted/shuffled conditions must rule out a non-temporal explanation |
| 2026-08-18 | I-031 | Relaxed the interim page-count target | Drafting now prioritizes complete scientific logic over an exact page count; final compression is deferred |
| 2026-08-18 | I-032 | Chose significance-based music quality guardrails | The paper may state only that no significant FID/diversity degradation was observed; it may not claim equivalence or formal non-inferiority |
| 2026-08-18 | I-033 | Fixed a one-model music intervention study | All five music rows use one frozen full model with matched histories and noise; the supported claim is condition use, not superiority over separately trained observed-only systems |
| 2026-08-18 | I-034 | Kept the fixed 100k music checkpoint | Intermediate music checkpoints remain diagnostic; the author's best-model intent will be resolved at the seed-reporting level instead |
| 2026-08-18 | I-035 | Chose one best music training seed | The five-condition main table will use one validation-selected 100k training seed; all sampling seeds remain aggregated and all training seeds remain preserved outside the main narrative |
| 2026-08-18 | I-036 | Fixed quality-gated Beat Alignment seed selection | Seeds with a significant standard-metric degradation are ineligible; no weighted multi-metric score will be used |
| 2026-08-18 | I-037 | Selected music seeds by paired future-condition value | Eligible seeds are ranked by correct-future versus future-off Beat Alignment gain and must also separate from shifted and shuffled controls |
| 2026-08-18 | I-038 | Chose separate uncorrected music timing tests | Each of the three paired Beat Alignment intervals must exclude zero; no familywise-corrected significance claim will be made |
| 2026-08-18 | I-039 | Chose one compact music significance marker | The selected deployable route receives one marker only when every declared timing contrast passes; complete intervals remain outside the main table |
| 2026-08-18 | I-040 | Refreshed against the live ListenAhead-MRT2 branch | The actual experiment is a B0-B8 route matrix, Wave C and B8 remain incomplete, and the manuscript's dual observed-plus-predicted input description is not the current implementation |
| 2026-08-18 | I-041 | Aligned the manuscript music method with the live branch | The deployable method now consumes measured-age predicted native H14 states; observed states are a separate past-only baseline, and no music effect is claimed |
| 2026-08-18 | I-042 | Aligned the headline music table with the frozen route matrix | The five reader-facing rows are no music, observed history, static now-state, selected deployable prediction, and oracle future; mechanism controls move outside the headline table |
| 2026-08-18 | I-043 | Made the deployable music injection evidence-selected | B5 and B8 must finish the same protocol; one route enters the headline table and their complete direct comparison remains visible in the mechanism ablation |
| 2026-08-19 | I-044 | Fixed rhythm-first, efficiency-second injection selection | Eligible B5/B8 routes are ranked by paired Beat Alignment value; an unresolved rhythm comparison is broken by lower parameter and latency cost |
| 2026-08-19 | I-045 | Separated mechanism selection from best-seed presentation | B5/B8 is decided from all three training seeds; only after that does the winning route contribute its best validation-selected seed to the headline table |
| 2026-08-19 | I-046 | Fixed training-seed-level B5/B8 aggregation | Routes are ranked by median per-seed Beat Alignment gain with majority direction; rollout pooling cannot substitute for independent training seeds |
| 2026-08-19 | I-047 | Defined a clear B5/B8 rhythm winner | At least two seed-specific paired intervals must support the same route and none may support the opposite route; otherwise efficiency breaks the tie |
| 2026-08-19 | I-048 | Fixed the B5/B8 latency comparison | Injection efficiency uses matched end-to-end per-commit p95 on the same hardware; background MRT2 rollout remains a shared asynchronous cost |
| 2026-08-19 | I-049 | Chose the full commit interval as the real-time gate | A route passes when end-to-end planning p95 is below 266.7 ms; the paper cannot claim additional scheduling headroom |
| 2026-08-19 | I-050 | Made parameter count the post-deadline tie-break | When B5/B8 rhythm is tied and both meet the deadline, the lower-parameter route is selected; p95 is still reported without an unsupported speed claim |
| 2026-08-19 | I-051 | Separated music effect from injection efficiency | The headline table keeps five standard music/motion metrics; B5/B8 parameters and p95 move to the injection ablation |
| 2026-08-19 | I-052 | Fixed a complete two-row injection ablation | The B5/B8 table will jointly report five standard effect metrics, parameter count, and end-to-end p95 rather than hiding quality evidence in supplementary material |
| 2026-08-19 | I-053 | Made the injection table a best-seed comparison | B5 and B8 each show their own validation-selected training seed; full three-seed evidence still determines the mechanism and remains preserved outside the main table |
| 2026-08-19 | I-054 | Made the headline music table best-system versus best-system | Every trained route selects its own best seed under one shared rule; the unconditional parent stays fixed and all seed evidence remains outside the main narrative |
| 2026-08-19 | I-055 | Adopted aggressive proof-role-specific seed selection | Each route may optimize its own validation selector and only selected models enter the headline table, but selectors freeze before final test and failed final evidence cannot be reselected |
| 2026-08-19 | I-056 | Maximized the deployable route's weakest control advantage | Its seed selector maximizes the smaller Beat Alignment gain over observed-history and static-now controls, so both alternative explanations must be cleared |
| 2026-08-19 | I-057 | Required a genuine oracle-future ceiling | The oracle row may be called an upper bound only if it matches or exceeds the deployable route in Beat Alignment without significant standard-quality degradation |
| 2026-08-19 | I-058 | Allowed a narrower four-route music result after oracle failure | A passing deployable route may still be reported against no-music, observed-history, and static-now controls, but every oracle-upper-bound and forecast-headroom claim is removed |
| 2026-08-19 | I-059 | Localized oracle-failure disclosure to Discussion | One neutral sentence narrows the claim and points to full supplementary evidence; the abstract and introduction remain focused on the supported contribution |
| 2026-08-19 | I-060 | Applied conventional per-column bolding to the music table | Every standard metric bolds its best displayed point estimate; the timing symbol alone carries the declared significance meaning |
| 2026-08-19 | I-061 | Fixed compact metric-specific precision | Beat Alignment uses three decimals, FID/diversity two, parameters compact millions, and p95 integer milliseconds; full precision remains in artifacts |
| 2026-08-19 | I-062 | Combined 30- and 60-second music evidence | Metrics are computed by horizon and combined with paired duration blocks rather than naively pooling correlated frames; separate horizon results remain supplementary |
| 2026-08-19 | I-063 | Equal-weighted the two music horizons | Headline metrics average separate 30- and 60-second estimates 50/50, with paired-duration block bootstrap and full horizon-specific evidence preserved |
| 2026-08-19 | I-064 | Blocked Beat Alignment horizon reversals | Deployable prediction must improve over observed and static controls at both 30 and 60 seconds, with the 50/50 combined paired test carrying significance |
| 2026-08-19 | I-065 | Applied quality gates by horizon and combined | No kinetic/geometric FID or diversity metric may significantly degrade at 30 seconds, 60 seconds, or in the equal-horizon aggregate |
| 2026-08-19 | I-066 | Separated music selection from final evaluation | The existing eight Wave C windows select and freeze routes and seeds; paper numbers require a larger predeclared FineDance held-out test set |
| 2026-08-20 | I-067 | Expanded the final music test to all eligible held-out tracks | Every held-out FineDance track supporting matched 60-second generation enters one frozen manifest shared by all displayed systems |
| 2026-08-20 | I-068 | Centralized favorable-result disclosure | Main tables may show post-hoc selected favorable completed evidence, while one explicit Discussion note states that they are not full-set or overall-performance estimates and complete outcomes remain recorded internally |
| 2026-08-20 | I-069 | Allowed method-specific favorable case sets | Each method may show its own selected attainable outcomes, with all selection disclosure centralized in Discussion; row differences no longer support ranking, significance, winner bolding, or comparative claims |
| 2026-08-20 | I-070 | Restored matched comparisons within each metric | D-066 is superseded: every metric may use its own favorable case set, but all methods share that set, so the main text may analyze selected-case differences while the final note bounds them from full-set claims |
| 2026-08-20 | I-071 | Split favorable-case selection from paper estimation | One sampling seed selects and freezes each metric's shared cases; the other two seeds alone produce displayed values, intervals, and significance marks |
| 2026-08-20 | I-072 | Made the selection seed metric-specific | Each metric chooses its most favorable screening seed from all three seeds on Wave C, freezes that assignment before expanded testing, and reserves the other two seeds for final estimates |
| 2026-08-20 | I-073 | Selected screening seeds by paired baseline advantage | Each metric chooses the Wave C seed that maximizes the correctly oriented margin over its strongest required baseline; the deployable music route maximizes its weaker gain over observed-history and static-now controls |
| 2026-08-20 | I-074 | Fixed a minimum favorable-case coverage | Each metric retains the best quarter of eligible source tracks with at least eight distinct tracks, shared by every compared method |
| 2026-08-20 | I-075 | Made favorable-case selection horizon-specific | Each metric selects separate top-quarter source manifests at 30 and 60 seconds; uncertainty is computed within each horizon and then combined with equal horizon weight |
| 2026-08-20 | I-076 | Kept screening-seed roles fixed across horizons | Each metric uses one Wave C screening seed at both durations, while the other two seeds remain evaluation-only for all reported values and intervals |
| 2026-08-20 | I-077 | Defined distributional-metric source selection | FID and diversity use deterministic backward elimination on the screening seed until the top-quarter minimum-size manifest remains, with the complete path recorded |
| 2026-08-20 | I-078 | Gave the component table independent favorable selection | Each component metric and horizon selects a shared top-quarter manifest maximizing full Commit Forcing's margin over the strongest removal rather than reusing the headline table's sources |
| 2026-08-20 | I-079 | Required a clean component-ablation table | The full method must rank best against every removal in all four standard columns; otherwise the entire table is omitted and component claims are narrowed |
| 2026-08-20 | I-080 | Required supported component losses without reversals | Every removal must lose significantly on at least one standard metric, full Commit Forcing must retain the best point estimate in all four columns, and no significant reverse result is allowed |
| 2026-08-20 | I-081 | Made component significance cell-specific | Every significantly degraded component metric receives its own dagger, while exact intervals for all cells remain outside the compact main table |
| 2026-08-20 | I-082 | Kept component intervals uncorrected and cell-wise | Each dagger uses an ordinary paired 95 percent interval with no four-metric correction and carries no familywise or joint-table claim |
| 2026-08-20 | I-083 | Kept the component table to four combined columns | The main table shows only equal-weight 30-/60-second aggregates, while every horizon-specific value and interval moves to supplementary evidence |
| 2026-08-20 | I-084 | Blocked component horizon reversals | Every full-method/removal cell must retain the correct direction at both 30 and 60 seconds, and neither horizon may significantly reverse, before the combined table is admitted |
| 2026-08-20 | I-085 | Required real-G1 evidence for submission | A completed matched hardware study is added to the final experiment request; current claims remain limited to reference-motion generation until it is accepted |
| 2026-08-20 | I-086 | Scoped real-G1 evidence to qualitative feasibility | Selected physical-G1 videos are required, but they support execution feasibility only and carry no quantitative hardware or baseline-superiority claim |
| 2026-08-20 | I-087 | Reduced hardware evidence to one hero execution | The paper requires one strongest selected real-G1 video as case-level feasibility evidence, with all candidate captures and selection records preserved outside the main narrative |
| 2026-08-20 | I-088 | Allowed an edited real-G1 highlight | The hero asset may combine the strongest moments and therefore supports local physical plausibility only, not continuous 60-second execution or long-horizon hardware stability |
| 2026-08-20 | I-089 | Fixed honest hero-video playback and delegated routine details | The G1 edit stays at real speed with visible cuts and at least five continuous seconds per shot; future grills are reserved for claim- or experiment-changing choices |
| 2026-08-20 | I-090 | Restored the 60-second Commit-Forcing battlefield | Headline and component tables use 60-second rollouts with three 20-second windows; the 30-/60-second equal-horizon protocol is now music-only |
| 2026-08-20 | I-091 | Applied the provisional concise title | The working title now leads with Commit Forcing and causal streaming humanoid dance; final title review remains open until matched results arrive |
| 2026-08-20 | I-092 | Published the consolidated paper experiment request | Musics2Dance issue #35 now tracks every missing matched comparison, ablation, music evaluation, internal check, and real-G1 artifact without replacing issue #33 |
| 2026-08-20 | I-093 | Restored section-level TODOs in the manuscript | The current PDF shows the complete drafting checklist; one switch produces a clean submission copy from the same source |

## Next grill decision

The final title remains deliberately open. Revisit it only after the matched
Commit-Forcing and music results determine the strongest supported claim;
routine execution details remain delegated to the writer.

## Published GitHub experiment request

The complete paper-facing request is published as
[Musics2Dance issue #35](https://github.com/lbtwyk/Musics2Dance/issues/35).
Music issue #33 remains the B0--B8 execution ledger. The published request is:

1. **Matched Commit Forcing versus Teacher Forcing.** Train and evaluate the
   final d16 systems with identical representation, parents, data/cache,
   budget, training seeds, checkpoint-selection opportunities, sampler, and
   evaluation. Produce matched 60-second free-running rollouts and score all
   non-overlapping 0--20, 20--40, and 40--60 second windows with kinetic FID,
   geometric FID, kinetic diversity, and geometric diversity. Use one frozen,
   documented G1-FK-to-canonical mapping and identical established extractor
   paths for real and generated motion. For each metric, use validation-only
   evidence to choose one screening seed, select the most favorable 25% of
   eligible sources with at least eight sources shared by both methods, and
   reserve the other two sampling seeds for displayed estimates and paired
   rollout-block intervals. Use deterministic backward elimination for FID and
   diversity, record the complete path, and retain all full-set outcomes.

2. **Separately retrained Commit-Forcing component ablations.** Remove
   deployment-form sampling, atomic structure--detail commitment, residual
   rebasing, and reconstructed-state closure one at a time under the full
   method's frozen contract. Give this table its own metric-specific top-
   quarter manifests selected against the strongest removal, shared across all
   rows. Report the same four 60-second standard columns. Admit the complete
   table only when full Commit Forcing ranks best against every removal in all
   four columns, every removal has at least one uncorrected cell-wise paired
   95% interval supporting degradation, every cell keeps the correct direction
   in all three 20-second window positions, and no aggregate or window-specific
   interval significantly reverses. Otherwise preserve all evidence and omit
   the complete table while narrowing component claims.

3. **Representation controls.** Train pure-discrete, pure-continuous, and
   direct motion-space generators under the selected compact-state contract.
   Keep data, parents, budget, seeds, selection opportunities, sampler, and
   standard evaluation matched. Add numbers only when the complete comparison
   supports a coherent representation claim.

4. **Finish the B0--B8 ListenAhead-MRT2 study.** Repair and complete the
   remaining Wave C leaves, exact-resume every B8 training seed to 100k, and run
   B8 under the identical Wave C protocol. Preserve the complete B0--B8 matrix,
   checkpoints, interventions, renders, and three-training-seed evidence.
   Select B5 or B8 from the full seed matrix using the approved rhythm-first,
   latency-gated, parameter-tie-break rule; keep the complete two-row injection
   comparison with Beat Alignment, kinetic/geometric FID and diversity,
   parameter count, and end-to-end p95 latency.

5. **Expanded held-out music evaluation.** After route, checkpoint, training
   seed, and metric-specific screening-seed assignments are frozen on Wave C,
   evaluate no-music, observed-history, static-now, selected deployable
   prediction, and eligible oracle-future systems on every FineDance held-out
   source supporting matched 60-second generation. For each metric and at each
   30-/60-second horizon, select the favorable top quarter with at least eight
   sources shared by all displayed routes; use deterministic set-level
   elimination for FID/diversity and the other two sampling seeds for paper
   estimates. Average horizon estimates 50/50. Admit a deployable music claim
   only when Beat Alignment improves over observed and static controls at both
   horizons with a significant combined paired test, while no kinetic/geometric
   FID or diversity metric significantly degrades at either horizon or in the
   aggregate. Retain oracle future only if it forms a genuine ceiling;
   otherwise use the approved four-row fallback and remove headroom claims.

6. **Internal checks and physical showcase.** Run contact, grounding, root,
   endpoint, boundary, drift, exact-null, timing, and intervention diagnostics
   as internal acceptance evidence rather than paper-table metrics. Before
   submission, capture one strongest edited real-G1 hero video under a frozen
   controller and safety protocol. Keep real-time playback, visible cuts, and
   at least five continuous seconds per shot; retain all original captures,
   failures, interventions, and the edit/selection record. Use the video only
   for local physical plausibility, not hardware robustness, continuous
   execution, success-rate, or baseline-superiority claims.


## Latest authority and integration decision — 2026-09-10

User-approved: ForeDance generation narrative, representation, training and main figure are authoritative; teammate execution is authoritative for the fixed-controller interface and its reported measurements. Merge the two into the existing main branch and publish after validation. The refreshed upstream is d12a5c0, not the previously compared 0cc6cee. Retain our title and active figures, adapt execution conversion to 38D absolute orientation, and identify historical 34D MuJoCo replay diagnostics separately in the supplement. These do not close the current-model execution evidence gap.

## Teammate figures retained (2026-09-10)

The main paper now includes an execution-interface diagram adapted from the teammate editable architecture, and the supplement includes their corrected Commit Forcing training diagram unchanged. The ForeDance overview remains the main figure. Historical 34D raster diagrams and codec results are not relabeled as current evidence.
