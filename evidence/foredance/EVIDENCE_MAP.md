# ForeDance evidence and figure provenance

Checked 2026-09-09 against the actual GitHub repositories and original Isambard outputs.

## Authoritative revisions

- Method default branch `prior-dev`: [24f4f75aa17c3622071e4fa6b1491ca5f2eabcb2](https://github.com/lbtwyk/Musics2Dance/tree/24f4f75aa17c3622071e4fa6b1491ca5f2eabcb2). The repository's branch literally named `main` was older; it was not substituted for the active default branch.
- Paper `main`: [0cc6cee55521bec0785ba2cf3d0e0d60a4f1c6ec](https://github.com/RamseyPengTianhu/ICRA_AudioMimic/tree/0cc6cee55521bec0785ba2cf3d0e0d60a4f1c6ec).
- Scientific acceptance: method repository `docs/experiments/reviews/EXP-20260904-v6f-aq-tmmr-direct-condition-acceptance.md` and `EXP-20260904-g1-yaw-anchor-abs-6d-acceptance.md` at the revision above.

## Original quantitative records

Remote evaluation root on `u6og-clash-isambard`:

`/lus/lfs1aip2/projects/u6og/yukunwang.u6og/runtime/EXP-20260904-v6f-aq-tmmr-direct-condition/evaluation/`

| Local immutable copy | Remote relative path | Use |
|---|---|---|
| condition-analysis.json | analysis/aggregate.json | Paired music-condition effects and intervals |
| motion-quality.json | paper_breadth/score/aggregate.json | Per-route and per-training-seed metric values |
| completion.json | completion.json | Pipeline status, separate from scientific acceptance |

The completion file says `complete_unreviewed`; that machine status is not promoted to scientific acceptance by itself. The separately dated GitHub owner acceptance is the scientific record used for admission. Preserve this distinction.

The condition-use table uses `conditioned_minus_trained_no_music` for `FD-DF-L-AM-FHC` and `FD-DF-L-AJ-FHC`, metric `mmr_ms`. The raw route names are internal provenance only. The positive improvement equals no-music distance minus conditioned distance. `build_evidence_tables.py` checks that identity against the independently saved route means. Each has 162 paired cells, three training seeds, and 10,000 bootstrap draws. Intervals are reproduced, not newly re-estimated or changed to favorable subsets.

All populated quantitative values belong to the frozen complete 18-track cohort and common 23-second source-supported segment beginning at frame 264. They do not fill the planned anticipation, current D+C-baseline, or TF/CoF comparisons. The trained no-music baseline is distinct from inference-time null conditioning.

## Method bindings

- `dataset/g1_streaming_state.py` and `dataset/motion_representation.py`: fixed yaw-anchor absolute pelvis orientation, 38D native motion, 71D boundary state.
- `model/g1_motion_projectors.py`: `structure_spec_for_motion_format` selects `G1_STRUCTURE_SPEC_NATIVE_SO3` for the yaw-anchor format. Structural native indices 0–23; velocity indices 0–20. Cartesian roles: torso, both wrist-yaw origins, both lowest-foot geometry points.
- `eval/g1_kinematics.py`: canonical joint order, twelve leg joints followed by three waist joints and fourteen arm joints.
- `model/g1_clean_representation_losses.py` and `train_g1_clean_streaming_codec.py`: full, structure-only and corrupted-detail objectives, plus full-orientation boundary-transition supervision. The corrupted-detail path stays in prose, per the author's figure decision.
- `model/g1_listenahead_direct_conditioning.py`: forecast-time alignment and FrameFiLM in both branches.
- `docs/research/modules/FULL_HISTORY_CORRUPTION_TRAINING_SPEC.md`: full-history training corruption, unchanged state/music, no inference corruption.

The body-part illustration depicts supervision views, not a hard anatomical constraint on the latent or decoder. Joint-view detail is fourteen arm joints; geometry-view detail is the remaining twenty-six points, including intermediate lower-body points. A wrist position can therefore be structural even though wrist-joint angles belong to the complementary native view.

## Actual motion illustration

`video-source.json` records the original remote file and verified SHA-256. `render-manifest.json` identifies the panels and motion files. Figure 5 crops the bottom-right FHC panel of the original 1280×960, 30 fps, 1800-frame video for source 098, training seed 1234, sampling seed 1234, guidance 1.0. Crop is x=640:1280, y=535:960, excluding the internal label band; sample times are 10, 30, 50 seconds. Only spatial cropping and frame extraction are applied. These evenly spaced snapshots are an illustrative selected case, not a matched TF comparison, measured controller execution, or quantitative superiority evidence.

## Generated method figures

The first four figures are explanatory imagegen illustrations; none supplies experimental measurements. Exact initial and revision prompts are archived beside this file. The user requested Image 2.5, but the built-in tool exposes no model parameter, so the model identity is not asserted. Architecture routing was checked for forecast-to-both-branches, sampled-structure-to-detail, separate structure/residual inputs to the shared decoder, and reference-derived history/state updates. The D+C figure must have only two principal reconstruction paths and code-matched body-part views.

## Teammate execution integration (2026-09-10)

The execution interface is taken from d12a5c0 and adapted to current absolute-orientation reconstruction. Supporting replay numbers come from the earlier 0cc6cee table, preserved verbatim in team-execution/teammate-main-20260908.tex and transcribed to tracking.json. These are one-track, one-sampling-seed, four single-run MuJoCo diagnostics of the earlier 34D generator; no live music inference occurs during replay. They are not current ForeDance results and are not pooled with the 18-track cohort. Numeric transcription is checked against the archived table; original controller traces were not independently reprocessed in this writing task. The latest Overleaf draft removes the experiment block; this merge keeps its streamlined interface and places the separately identified historical table in the supplement, not in the current-model main tables.
