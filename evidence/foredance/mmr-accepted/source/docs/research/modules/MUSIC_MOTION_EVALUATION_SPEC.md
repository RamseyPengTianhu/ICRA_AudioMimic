# Music-Motion Evaluation Spec

Status: latest MMR primary evaluator accepted by the owner on 2026-09-10.

## Current Primary Evaluator — owner accepted 2026-09-10

Use **MMR-G1+ R_cosine5** for subsequent generator correspondence evaluation:
standard content-group sampling, five-second posterior-mean cosine, FP32
inference, score-level ensemble of seeds1234/2345/3456 final update14500,
frozen train-only normalizer and full-SO3 continuous357D frontend
`mmr_g1_plus_so3_continuous_357_v1`. Higher cosine is better. Report
wrong-track pairwise accuracy (%) and correct-minus-wrong margin using a common
cohort/window/donor protocol across generators. Do not call this percentage
R@1/R@5, overall motion quality or controlled condition-use accuracy.

Canonical identity, results and remaining stages:
[`EXP-20260907-mmr-g1-plus-correspondence`](../../experiments/EXP-20260907-mmr-g1-plus-correspondence.md).
The owner accepted available FHC-FiLM AM/AJ results of74.20%/75.01% and adopted
this evaluator as the mainline. Historical MMR/MS remains preserved for
comparison; matched historical-checkpoint and Hybrid rescoring are still
missing inputs. Adoption does not assert historical-checkpoint superiority,
successful original confirmation gates, or human/controlled-generation proof.

This decision supersedes earlier primary-evaluator choices below. The remaining
sections preserve the historical design and evidence, not current defaults.

After reviewing matched H_cosine5 rescoring (FiLM AM75.69%, AJ76.79%; paired
improvement intervals include zero), the owner explicitly reaffirmed standard
R_cosine5 as the mainline and deferred matched old-MMR comparison to follow-up.
[Final owner-decision handoff](https://github.com/lbtwyk/Musics2Dance/issues/50#issuecomment-5618385423).

## Decision Goal

Define a paper-facing music-motion evaluation protocol whose main metrics are
traceable to accepted top-conference work and whose diagnostics are clearly
separated from headline evidence.

This spec fixes the evaluation design. The project owner subsequently
authorized implementation, evaluator selection, and fast-path evaluation of
the six already-trained candidates listed in
`EXP-20260902-mmr-g1-evaluator-selection`. It does not authorize training the
missing OD-Hybrid route or selecting an evaluator from generated outputs.

## Settled Boundaries

- A learned metric may enter the main paper only through an identifiable
  published protocol, with any necessary embodiment adaptation disclosed.
- The current local learned-retrieval evaluator is a custom shallow dual tower.
  Its numbers are diagnostic and must not be presented as a published metric.
- The current transparent energy-motion cosine and its wrong-time subtraction
  have no verified accepted-top-conference precedent as the same metric. Keep
  them as an interpretable diagnostic, not a headline paper metric.
- Standard motion-quality metrics and Beat Alignment Score retain their normal
  literature-backed roles. Beat alignment alone is not evidence for fine
  within-track temporal correspondence.
- FD, OD, and OFD may be ranked only after the same frozen evaluator, cohort,
  seeds, and intervention protocol have been run across them.

## Evidence Review

### Closest same-domain protocol

SoulDance (ICCV 2025) defines Music-Motion Retrieval (MMR) with a music tower,
a temporal motion tower, a shared 256-dimensional latent, and symmetric
InfoNCE. Its paper-facing MMR Matching Score combines latent distance and
one-second temporal-difference distance. The published body evaluator is
trained on paired ground-truth motion from AIST++, FineDance, and PhantomDance,
with evaluator/generator split separation.

The paper and supplement specify the key protocol parameters: 263-dimensional
body motion input, batch size 128, temperature 0.1, and a false-negative
similarity threshold of 0.8. The public body-MMR training call does not pass a
semantic sentence embedding and therefore does not activate that optional
false-negative mask. The clean-room reproduction follows this executable
public-code behavior rather than inventing a semantic proxy from Jukebox.
Retrieval R@1/R@5 and median rank are evaluator validation outputs; MMR
Matching Score is the reported generation metric.

The official repository contains the metric code but not a usable public
pretrained MMR checkpoint or self-contained public data pipeline. It also uses
private absolute paths and a restrictive repository license. Adoption therefore
means a clean-room implementation of the paper-defined protocol, not copying or
claiming to use an official released evaluator.

### Rejected as direct replacements

- FineDance Genre Matching Score is genre-level compatibility; it cannot test
  whether a motion matches the correct moment of the same track.
- BeatDance is music-video retrieval, not 3D robot-motion retrieval.
- TANGO/AuMoCLIP is speech-gesture retrieval, not music-dance retrieval.
- MGSV and artistic-correspondence methods are music-video protocols. They are
  useful precedents for contrastive temporal alignment, but not drop-in robot
  motion evaluators.

## Candidate Paper Protocol

The leading candidate is a clean-room reproduction of SoulDance's body MMR
protocol:

1. Train the evaluator only on paired ground-truth train data. Exclude all test
   identities and all generated motion.
2. Reproduce the published encoder family, batch size, symmetric InfoNCE
   objective, latent width, temperature, the public body-training call's
   inactive optional semantic mask, one-second segmentation, and MMR Matching
   Score formula.
3. Report held-out ground-truth bidirectional R@1, R@5, and median rank as
   evaluator calibration, not as generator wins.
4. Report MMR Matching Score as the learned paper metric.
5. For the causal timing claim, apply the same published score to matched
   correct-time and same-track shifted conditions. The paired intervention is
   our experimental design; it must not be renamed as a published metric.
6. Keep the transparent score, full shift curve, and local shallow-retrieval
   results in diagnostics or appendix material.

## Promotion Gate

A reproduced learned evaluator is not main-paper evidence merely because its
training loss decreases. Before promotion, it must demonstrate on held-out
ground truth:

- non-trivial bidirectional retrieval above chance;
- correct-time preference over same-track temporal shifts and wrong tracks;
- degradation as temporal displacement increases; and
- a fixed, leakage-free evaluator identity shared by every compared generator
  and data stack.

Whether human-alignment validation is required for promotion remains open until
the protocol family is selected.

## Decision Tree

### Round 1: protocol family

- `A` — Adopt the SoulDance MMR protocol as the learned main-metric target.
  This is the closest accepted top-conference, same-domain method, but requires
  an explicit G1 representation bridge and a clean-room reproduction.
- `B` — Do not use a learned metric in the main paper. Keep learned retrieval
  and transparent alignment diagnostic-only; headline evaluation uses standard
  BAS and motion-quality metrics.
- `C` — Use FineDance Genre Matching Score. This is literature-backed but tests
  genre compatibility rather than within-track timing, so it does not cover the
  present ListenAhead claim.

Recommendation for Round 1: `A`. Later rounds must decide the representation
bridge and the calibration/promotion gate before any implementation is allowed.

Decision: `A` accepted by the project owner on 2026-09-02. Reproduce the
SoulDance MMR protocol as the learned main-metric target. This selects a
protocol family, not yet an implementation or a paper-valid evaluator.

### Round 2: motion representation bridge

Repository inspection found no existing G1-to-HumanML3D/Guo 263D conversion.
The published 263D input is tied to a 22-joint human topology rather than being
an arbitrary vector width:

- four root channels;
- local positions for 21 non-root joints;
- continuous 6D rotations for 21 non-root joints;
- local velocities for all 22 joints; and
- four left/right heel/toe contact channels.

G1 instead has a verified 29DoF, 30-body kinematic chain. It has explicit
pelvis, waist, limb, ankle, and wrist links, but no one-to-one canonical human
head, neck, heel, and toe topology. Producing exactly 263 channels would require
inventing or duplicating semantic joints. Matching the width would therefore
not constitute a faithful reproduction.

- `A2` — Use a G1-native structured Guo-feature analogue: the same root,
  body-local position, body rotation, velocity, and foot-contact factor types
  computed from verified G1 forward kinematics; change only the input projection
  width while preserving the published MMR encoder, objective, training
  protocol, and MMR-MS formula. Name it `MMR-G1` and disclose the embodiment
  adaptation.
- `B2` — Force G1 into a 22-joint 263D pseudo-human skeleton. This matches the
  tensor width but introduces custom virtual/duplicated head, neck, heel, and
  toe semantics that can dominate the learned score.
- `C2` — Require exact published 263D semantics and therefore decline a learned
  main metric for G1. Keep all learned alignment results diagnostic-only.

Recommendation for Round 2: `A2`. SoulDance itself varies motion
representations between body and whole-body evaluators while retaining the MMR
protocol. `MMR-G1` keeps the published learning and scoring method and makes the
unavoidable embodiment change explicit; `B2` creates a less defensible hidden
adapter merely to preserve the number 263.

Decision: `A2` accepted by the project owner on 2026-09-02. Use a G1-native
structured Guo-feature analogue and disclose it as `MMR-G1`. Do not claim input
compatibility with the published 263D body evaluator and do not construct a
pseudo-human 22-joint bridge merely to preserve its width.

### Round 3: main-paper promotion evidence

Selecting the published learning and scoring protocol does not automatically
validate its G1 embodiment adaptation. The promotion gate must determine
whether `MMR-G1` measures perceived music-motion correspondence rather than
dataset identity, locomotion magnitude, or a retargeting artifact.

- `A3` — Require both objective evaluator calibration and a frozen human
  agreement study before main-paper promotion. Objective calibration covers
  held-out bidirectional retrieval, correct-time versus same-track shifts and
  wrong tracks, displacement monotonicity, and nuisance checks. The human study
  uses blinded paired judgments on the same correct/shifted/wrong conditions and
  tests whether `MMR-G1` orders pairs in the same direction. Until both pass,
  report `MMR-G1` as diagnostic.
- `B3` — Require objective calibration only. This is cheaper and remains close
  to SoulDance's published evaluator validation, but it leaves the G1-specific
  representation adaptation without direct perceptual validation.
- `C3` — Treat protocol reproduction as sufficient and promote immediately.
  This confuses implementation fidelity with metric validity and is not
  acceptable for a headline claim.

Recommendation for Round 3: `A3`. The added human study validates the only
material deviation from the published protocol—the G1 representation—while the
learned architecture and scoring formula remain literature-defined.

Decision: `B3` accepted by the project owner on 2026-09-02. Require objective
calibration but not an independent human agreement study for main-paper
promotion. The paper must not claim demonstrated perceptual correlation; it may
claim a literature-derived, objectively calibrated music-motion metric.

### Round 4: evaluator training population

Verified route legend:

- `FD`: the legacy FineDance-native stack;
- `OD`: O-Dance motion from the six OMG dance families; and
- `OFD`: the OMG FineDance-only motion subset encoded in the OD codec/token
  space.

The generator comparison uses a common held-out FineDance target cohort, but
the evaluator's training population can still create affinity. A FineDance-only
evaluator may reward FD/OFD domain signatures; separate evaluators would make
cross-stack scores incomparable.

- `A4` — Train one frozen, source-balanced `MMR-G1` on all eligible paired
  ground-truth O-Dance training sources, with track/identity-disjoint validation
  and test sets. Prevent source identity from carrying retrieval by measuring
  retrieval within each source family, report per-family and macro calibration,
  and freeze the same evaluator for FD, OD, and OFD. No generated motion enters
  evaluator training or model selection.
- `B4` — Train one FineDance-only evaluator. This matches the common target
  cohort but creates an avoidable evaluator-affinity concern when comparing the
  FineDance-trained routes with OD.
- `C4` — Train one evaluator per data stack. This may optimize each domain but
  destroys the shared measurement scale and cannot support an FD/OD/OFD
  ranking.

Recommendation for Round 4: `A4`. It follows SoulDance's multi-dataset body-MMR
principle, reduces single-source style shortcuts, and preserves one common
frozen measurement scale. The final model comparison remains paired on the same
held-out FineDance cohort; multi-source GT is used to calibrate the evaluator,
not to change the generation task.

Decision: the project owner accepted the common-evaluator requirement on
2026-09-02 and refined `A4` into a two-candidate bake-off. Train both:

- `MMR-G1-FD`, using paired FineDance ground-truth training data; and
- `MMR-G1-OD`, using source-balanced paired O-Dance ground-truth training data.

Select exactly one evaluator before scoring any generated FD, OD, or OFD
outputs. Prefer `MMR-G1-OD` when it calibrates strongly on every declared
ground-truth domain; otherwise fall back to `MMR-G1-FD`. Once selected, the
winner is frozen and used for every data stack. This refinement replaces the
single-candidate part of `A4` but preserves its one-common-scale conclusion.

### Round 5: leakage-safe evaluator selector

Raw MMR-MS values from independently trained latent spaces are not a valid
cross-evaluator selector: their embedding scales may differ. The selector must
use scale-free held-out ground-truth tasks and must be frozen before any
generated model output is scored.

- `A5` — Use a per-domain non-inferiority selector. Compare the FD and OD
  candidates on held-out ground-truth within-domain bidirectional R@1/R@5,
  median rank, correct-versus-wrong/shift pair accuracy, and shift-ordering
  accuracy. Select OD only when it passes the absolute promotion gates in every
  declared domain and is non-inferior to FD on the primary FineDance domain;
  otherwise select FD if FD passes its absolute gates. If neither passes, no
  learned metric enters the main paper.
- `B5` — Select the candidate with the better macro-average calibration score.
  This is simpler but can hide failure on one data stack and makes metric
  weighting an additional custom design choice.
- `C5` — Select after inspecting generated FD/OD/OFD scores. This is circular
  metric selection and cannot support a credible comparison.

Recommendation for Round 5: `A5`. It is the leakage-safe interpretation of the
owner's rule, "use OD if it scores strongly on every data stack; otherwise use
FD," and gives an explicit diagnostic-only outcome when the fallback evaluator
is also uncalibrated.

Decision: `A5` accepted by the project owner on 2026-09-02. Candidate selection
uses only frozen held-out ground-truth calibration. Generated FD, OD, and OFD
outputs are embargoed until the evaluator winner and its identity are frozen.
OD wins only by passing every declared domain and remaining non-inferior to FD
on the primary FineDance domain; otherwise FD is the fallback if it independently
passes. If neither passes, learned alignment remains diagnostic-only.

### Round 6: numerical calibration and selection gates

Published retrieval percentages cannot be copied as absolute gates because
R@K and median rank depend on the held-out candidate-pool size. Keep the
published retrieval definitions, evaluate all eligible non-overlapping windows
within each frozen domain, and quantify uncertainty by track-clustered
bootstrap so multiple windows from one song are not treated as independent.

- `A6` — Use statistical absolute gates plus a bounded FineDance
  non-inferiority margin:
  - for every declared held-out domain and both retrieval directions, the 95%
    track-clustered lower confidence bounds of R@1 and R@5 must exceed their
    exact chance rates `1/N` and `min(5,N)/N`;
  - correct-versus-wrong-track and correct-versus-same-track-shift pair
    accuracies must each have a 95% lower confidence bound above `0.5`;
  - the correct-time score must be best and the score must worsen monotonically
    over the frozen displacement ladder, with the 95% confidence interval for
    the track-level trend excluding the wrong direction;
  - OD is non-inferior to FD on the primary FineDance domain when its paired
    deficit is no more than five percentage points for R@1, R@5, and both pair
    accuracies, and no more than one rank for median rank. These margins are an
    internal evaluator-selection rule, not a reported metric improvement;
  - FD fallback must independently pass all absolute gates on every domain on
    which it will be used. Otherwise learned alignment remains diagnostic.
- `B6` — Require strict point-estimate dominance with zero margin. This matches
  a literal "higher everywhere" rule but is unstable to sampling noise and
  will usually select FD because of tiny, scientifically irrelevant changes.
- `C6` — Copy SoulDance's reported R@1/R@5/MedR values as gates. This is not
  comparable unless the candidate set and data distribution are identical, so
  it creates false protocol fidelity.

Recommendation for Round 6: `A6`. It freezes a meaningful success criterion,
preserves the published metric definitions, treats songs rather than windows
as the independent unit, and prevents a weak fallback evaluator from entering
the main paper.

Decision: `A6` accepted by the project owner on 2026-09-02. Use the statistical
absolute gates and bounded FineDance non-inferiority selector above.

Implementation-level calibration details are resolved as follows without an
additional owner decision:

- the three declared calibration domains are held-out `FD`, source-balanced
  held-out `OD`, and held-out `OFD`, all containing paired ground-truth motion
  and audio only;
- OD source-family metrics are reported separately and OD's domain result is a
  source-macro result, so its largest source cannot determine the gate;
- split identity is song/track plus performer or logical motion source where
  available, and no identity may cross evaluator train, validation, or test;
- retrieval uses the complete frozen candidate pool within a domain and reports
  its `N`, making the associated chance rates explicit;
- the same-track temporal ladder is `1, 2, 4, 8` seconds in both feasible
  directions, with no wraparound; and
- all confidence intervals resample tracks/logical sources, not individual
  windows.

## Frozen Outcome

1. Reproduce SoulDance MMR as a clean-room, literature-traceable protocol.
2. Use the disclosed G1 structured motion adaptation `MMR-G1`; do not fabricate
   a pseudo-human 263D bridge.
3. Train exactly two candidate evaluators, `MMR-G1-FD` and `MMR-G1-OD`.
4. Select one with the frozen held-out-GT `A5/A6` gate before inspecting any
   generated result, then use that one evaluator for FD, OD, and OFD.
5. Promote the selected evaluator to a main-paper learned metric only after it
   passes the objective gates. Do not claim human-perceptual validation.
6. Keep transparent alignment and the existing shallow retrieval head as
   diagnostics. Use published MMR-MS, standard BAS, and standard motion/physical
   metrics for paper-facing evidence.
7. If neither candidate passes, learned alignment remains diagnostic-only; the
   main paper does not force a learned metric.

Future grill questions are limited to consequential choices that would change
the paper claim, the identity of the main metric, or the scientific route.
Implementation details that preserve this frozen design are decided directly
without presenting alternative menus to the owner.

## Resolved Placement

- The current custom learned evaluator is retained only as a historical
  diagnostic and must not be mixed with `MMR-G1` results.
- The transparent score remains an interpretable diagnostic/appendix result.
- The selected, passing `MMR-G1` evaluator is the only learned alignment metric
  eligible for main-paper tables.

## Final Paper Reporting and Authority Boundary

The main paper reports learned evidence in two panels. The capability panel
contains bidirectional R@1/R@5/MedR for correct-condition outputs. The
condition-use panel contains within-model MMR-MS effects for full-gallery
wrong-track, generation-time same-track 8--20 second offsets, and a
capacity-matched trained-no-music reference. Every effect includes a 95%
hierarchical-bootstrap interval and per-training-seed direction. PFC, root
jerk, and joint jerk accompany trained-no-music rows because their generation
quality can differ materially.

Learned retrieval and wrong-track margin share the same MMR-G1 embeddings and
are two views of one evaluator, not independent validation sources. Raw MMR-MS
values may describe outputs measured in one frozen space but never select a
conditioning architecture; architecture claims require a paired difference of
within-model correct-versus-control effects. Exact-null, one-donor wrong-track,
and +2.13 second wrong-time remain appendix diagnostics.

`MMR-G1-FD` passed the frozen objective gate on FineDance ground truth: held-out
bidirectional R@1 was `0.0843/0.0904` at chance `0.0030`, correct-versus-wrong
accuracy was `0.6657` `[0.5684,0.7619]`, correct-versus-shift accuracy was
`0.5708` `[0.5143,0.6365]`, and the `0/1/2/4/8` second distance ladder was
monotonic with positive trend `16.66` `[6.75,29.98]`. The selector consulted no
generated output.

This supports a literature-derived, objectively calibrated learned metric for
the G1 domain. It does not show capability or authority beyond SoulDance's
native human-motion evaluator: the motion representation is adapted from 263D
human features to 357D G1-native features, the retrieval populations are not
directly comparable, and no frozen human-agreement study was run. Paper wording
must call `MMR-G1` a G1-domain reproduction and validation of the SoulDance
protocol, not a superior evaluator.

## Sources

- SoulDance, ICCV 2025 paper and supplemental material.
- FineDance, ICCV 2023 paper.
- BeatDance, ICMR 2024 paper and official implementation.
- TANGO, ICLR 2025 paper.
- Music Grounding by Short Video, ICCV 2025 paper.
- It's Time for Artistic Correspondence in Music and Video, CVPR 2022 paper.
- EDGE, CVPR 2023 paper.
