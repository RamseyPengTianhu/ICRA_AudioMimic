# Research-draft revision, 2026-09-08

## Repository synchronization

- Ran `git fetch origin` before editing. Fetch succeeded.
- No remote-only commits were found. Local `main` at `484b142` already contained
  six commits ahead of `origin/main`; all six were preserved.
- The initial revision was a working-tree update. The subsequent requested
  publication adds the T01--T12 checklist and visible manuscript TODOs; use
  the repository commit history for the published revision identity.
- Retained the existing IEEE conference class and bibliography. Conversion to
  the final journal submission format is a separate task.

## Manuscript changes

- Reframed title, abstract, motivation, and contributions around causal
  generation, effective music timing, and measured execution.
- Preserved the existing D+C/FK formulation, Commit-Forcing mechanism, figures,
  and two-training-seed representation table. The underlying historical numeric
  table was not regenerated in this revision.
- Clarified that Commit Forcing closes the reference-history/state process,
  not the physical robot dynamics. SONIC is an external state-feedback tracker.
- Added audio-cutoff/deadline age and effective-lead definitions; distinguished
  cached predictions from actual-future oracle audio.
- Added the current FiLM/Hybrid/RMS-FMS model taxonomy and startup protocol.
- Replaced the superseded M3-only pilot narrative with the formal generator
  cohort, evaluator calibration status, A-D condition replay, and fixed-reference
  SONIC measurements.
- Added three diagnostic tables and explicit limitations. Timing discrepancies
  are not aesthetic errors or additive causal shares.

## Evidence map

Paths below are relative to the parent AudioMimic workspace. They are internal
research provenance, not bibliography entries or public supplementary material.

| Manuscript material | Source |
|---|---|
| Historical motivation and route | `docs/experiments/EXP-20260617-music2dance-progress-report.md`; `ROADMAP_REALTIME_MUSIC_TO_G1.md` |
| Model architecture/ownership | `docs/evaluation/C0_C1_INJECTION_OWNERSHIP_AUDIT_20260828.md` |
| Learned startup candidate | `docs/evaluation/FILM_VISIBLE_SONIC_START_20260908.md`; completed u6250 training receipt/log |
| Formal 18-song generator matrix | `eval/results/benchmark_v1/formal/all_generator_routes_comparison/REPORT_ZH.md` |
| Film-AM/C0 song-bootstrap result | `eval/results/benchmark_v1/formal/song_bootstrap_gt_calibration_v1/REPORT_ZH.md` |
| Fixed-q0 residual counterfactual | `eval/results/benchmark_v1/formal/dc_generator_ablation_3seed/REPORT_ZH.md` |
| Cross-dataset evaluator status | `eval/results/benchmark_v1/formal/g1_music_motion_evaluator_multidataset_v3/REPORT_ZH.md` |
| A-D generation | `eval/results/diagnostics/age_attribution_v1/film_am_098/generation/` |
| A-D tracking | `eval/results/diagnostics/age_attribution_v1/film_am_098/sonic_c4_r04/comparison_trim2s_mujoco_order/metrics.json` |
| Retention metric implementation | `eval/sonic/analyze_generation_execution_gap.py` |
| New timing trace | `eval/results/online_music/scheduler_budget_v1/film_am_098_budget140_snapshot100_sonic_r01/online_run.json` |
| Evaluation design | `docs/evaluation/EVALUATION_MAP_MUSIC_TO_G1.md`; `docs/evaluation/HUMAN_EVALUATION_PROTOCOL.md` |

The A-D conditions archive is
`eval/results/diagnostics/age_attribution_v1/film_am_098/conditions/live_vs_cache_snapshot100_fullrate.conditions.npz`,
SHA-256 `73a6e2ad1e85d5fa20701845a450172ff930b20ffe444c56c16ade0d24ac6787`.
Replays start at archive index 3, emitted music frame 145 (audio 5.8 s), with
empty motion history, Film-AM seed 1234, and 225 commits. The new age trace
SHA-256 is `f799cfbc6d9a1f9139b2543a7e5a142200eb0522fcd5d88d1ccebf7e04854db5`.
These are matched artificial segments, not full-song onset trials.

## Claim gates before submission

1. Complete matched Teacher-Forcing/Commit-Forcing and recursively generated
   discrete-only/independent continuous-only controls. Existing decoder
   counterfactuals cannot substitute for these studies.
2. Validate the learned startup checkpoint in generation and execution; report
   untrimmed startup and subsequent activity. Re-audit historical standing
   deltas after the feedback-order correction.
3. Repeat timing/content interventions over independent songs and seeds, and
   tracker trials over independent resets. Include all attempts in reliability
   statistics; successful retries alone do not estimate a success rate.
4. Check full/C4 preview access, initial state, and timestamp alignment before
   attributing delivery effects. Separate actual online execution from replay.
5. Complete blinded evaluations and reserve final songs not repeatedly used
   for tuning. Cross-dataset v3 is not yet an accepted cross-dataset ranking
   metric; the earlier performance-ID-based v2 numbers are superseded.
6. Validate any hardware claim with real hardware records. Current A-D results
   are MuJoCo measurements, not a safety guarantee or real-G1 result.
7. Re-audit existing literature entries and claims before final submission.
   This revision reused the bibliography, rather than independently verifying
   every historical reference.

## Build

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error \
  -outdir=/tmp/audiomimic-paper-20260908 main.tex
```

The initial expanded draft was 10 pages, including references; enabling the
collaborative TODO annotations adds review material. The draft still needs
editorial compression for submission. `TODO.md` records the open evidence gates,
and `\showpapertodostrue` makes linked TODOs visible in the compiled manuscript.
Set `\showpapertodosfalse` only when preparing an appropriately reviewed clean
version; hiding annotations does not close evidence gaps. Author information
remains commented out as in the existing draft and has not been invented.

## D+C and three-block evaluation revision

- Fetched again and fast-forwarded to `ba1b79f`, preserving the two remote
  Overleaf commits and their new `V1.tex`. This revision edits `main.tex`, not
  that preserved version. Overleaf must compile `main.tex` to display this draft.
- Recentered the abstract, motivation, contributions, and conclusion on
  music-appropriate, expressive robot dance. D+C is now a standalone core
  contribution alongside Commit Forcing and causal music-to-robot execution.
- Expanded the D+C rationale: native kinematic supervision, complementary
  structure/detail roles, shared decoding and atomic commitment. No claim of
  inventing all discrete+continuous representations or proven q0 genre semantics.
- Explained the 30-to-50-Hz C4 reference interface, fixed SONIC policy ownership,
  reference-derived generator state versus measured controller feedback, and
  why tracking accuracy alone cannot prove music-adaptive expression.
- Replaced the two-outcome table with three explicit evaluation blocks:
  MMR matching/retrieval; music adaptation; dance quality/aesthetics. Added
  reported/implemented-exploratory/planned status to prevent a protocol wishlist
  from being mistaken for a completed experiment matrix.
- Specified MMR-MS, MMDist and retrieval definitions; BAS direction and event
  caveats; onset/impact response; distribution/diversity/multimodality; dynamics,
  continuity and physical proxies; and separate human music-fit/aesthetic tests.
- Added matched cross-paired audio controls to test appropriate adaptation,
  not only changed trajectories. The protocol applies to both generation and
  execution; completion remains T04/T09/T10, not a reported result.
- Kept runtime/forecast-age/valid-horizon and fixed-tracker measurements as
  supporting diagnostics, without conflating them with the three quality blocks.
- Preserved existing numeric results; no new model run, metric computation,
  controller change, or performance gain was produced by this writing revision.

### Additional definition sources

| Definition or status | Audited source in parent workspace |
|---|---|
| Metric organization and limitations | `docs/evaluation/METRIC_TAXONOMY_MUSIC_DANCE_G1.md`; `docs/evaluation/EVALUATION_MAP_MUSIC_TO_G1.md` |
| MMR-MS, paired centroid distance, retrieval and multimodality | `eval/metrics/learned_music_motion.py` |
| Frozen G1 evaluator and training controls | `eval/metrics/music_motion_evaluator.py` |
| BAS, onset/impact, contact and skating proxies | `eval/sonic/analyze_motion_music_execution.py` |
| Formal metric availability and sample limitations | `eval/results/benchmark_v1/formal/all_generator_routes_comparison/REPORT_ZH.md` |

The MMR-MS attribution was checked against the primary SoulNet paper,
*Music-Aligned Holistic 3D Dance Generation via Hierarchical Motion Modeling*
(ICCV 2025; https://arxiv.org/abs/2507.14915), and added to `Reference.bib`.
Our G1 evaluator is not claimed to be the original human-motion checkpoint.
This manuscript organization does not modify the frozen internal metric taxonomy
or existing metric implementations. Remaining validation is tracked in `TODO.md`.

The expanded three-block draft compiles to 12 pages including references and
visible TODOs. `latexmk` and `git diff --check` pass; there are no overfull boxes
or undefined references/citations. The pre-existing missing-author warning,
underfull line warnings, and MRT2 bibliography type warning remain. The metric
table and adjacent formula pages were visually checked. Final venue-length
compression and authorship remain T12 rather than being silently resolved.
