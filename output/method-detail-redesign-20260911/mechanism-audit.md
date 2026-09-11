# Method-detail redesign: source and scope

Manuscript baseline: `8d4e61b8e6b8a9cd7940a8bbcf3fff2069c230d2`.
Method implementation inspected at `lbtwyk/Musics2Dance`, immutable commit
`24f4f75aa17c3622071e4fa6b1491ca5f2eabcb2`; fetched source copies remain under
`tmp/method-detail-redesign-20260911/source/` and the prior typography audit.

## Accepted scope

Redesign conditioning, reconstruction/training, and Commit Forcing details.
Keep the accepted main overview and teammate SONIC diagram untouched.
Keep the original 60-second result frames and reduce their layout overhead.
Preserve all evaluator validation, BAS, MMR, quantitative tables and pending
ablation statements in the baseline. No experiment or numerical result changes.

The first candidates were rejected for excessive explanatory text and monotonous
visual style. Fresh candidates use sparse labels and visual mechanisms. Long
explanations and exact settings belong in prose/captions/appendix. The accepted conditioning vector is retained. The v6 comparison and representation
rasters were inspected and reconstructed under the user instruction to finish
generation and unified vectorization.

## Conditioning

`model/g1_listenahead_direct_conditioning.py`, `DirectConditionInterface`,
`align_physical_frames`, and `FrameFiLM` establish projection after LayerNorm,
physical-time embedding, linear interpolation, coverage masking, and the
residual gated modulation. The skip activation remains unchanged outside valid
coverage. Separate modules are installed after structural blocks and residual
diffusion heads. This is not cross-attention or a replacement of the activation.

`model/g1_listenahead_conditioning.py:motion_lead_seconds` starts motion queries
at 1/15 second. `dataset/g1_listenahead_mrt2_dataset.py:_condition_from_rows`
computes forecast leads as `(j+1)/25 - snapshot_age`, with positive-time validity.
The schematic fresh-forecast timeline illustrates zero snapshot age. Actual
conditioning uses each forecast's retained timestamps.

## Reconstruction

`model/g1_hybrid_streaming_codec.py:encode_clean_components` constructs
`r=z-stopgrad(e(q))`, full input `stopgrad(e(q))+r`, and structure-only input
`z+stopgrad(e(q)-z)`. The former sends the encoder gradient through r; the latter
uses straight-through gradients. Both decode with the same parameters and b.
The separate VQ objective trains the quantized representation.

`train_g1_clean_streaming_codec.py` and
`model/g1_clean_representation_losses.py` establish four standardized kinematic
blocks with equal block weights, full-coordinate versus selected structural
supervision, residual-corrupted auxiliary reconstruction, and boundary losses.
The diagram retains two principal reconstruction branches. Auxiliary settings
remain in the appendix; no third main diagram branch is introduced.

## Commit Forcing

`train_g1_listenahead_mrt2.py`, `build_commit_forcing_context` in its parent
trainer, and manuscript `METHOD_AUDIT_20260908.md` establish matched selection
of generated history and its corresponding reference boundary. Each supplied
training window constructs a local sampled transition without gradients.

The next recorded q and full latent remain fixed. The sampled next structure
conditions residual prediction; the residual target is `z_target-e(q_sampled)`.
Recorded target IDs supervise structural cross-entropy directly. They must not
be drawn as an input into predicted logits. The latent identity does not imply
identical decoded motion under a different boundary. No generated boundary
enters target re-encoding in the reported method.

## Figure and text integration plan

The new main CoF detail replaces duplicate explanations in the current main and
appendix diagrams. The old diagram source remains available. Exact settings,
native state definitions and loss partitions remain in the appendix. The three native figures and matching prose are now integrated in the actual
manuscript. Its 12-page proof was rebuilt and the figure pages were inspected.
