# Figure terminology and supervision audit — 13 September 2026

Baseline: paper main `ec53c1892ca1fa31b349f1d19ff10c0b319ea03d`, pulled before editing.
Scope: all three figures included by the current manuscript: overview,
representation learning, and Commit Forcing. The separate conditioning and
teammate SONIC figures remain disabled; their source assets are unchanged.

## Reader-facing terminology

| Figure | Previous wording | Revised wording | Meaning |
| --- | --- | --- | --- |
| CoF | Recorded segment | Ground-truth motion | Motion supplied by the training data, from which TF context is obtained. |
| CoF | Recorded seed | Ground-truth context | Initial history and boundary state, not a random seed. |
| CoF | Context source / Generation context | Context construction / Conditioning context | Distinguishes the construction operation from its result. |
| CoF | Self-rollout | Model rollout | One sampled transition used to construct training context. |
| CoF | Append + derive state | Context update | Appends the committed latent prefix and derives state from its decoded motion, explained in the caption. |
| CoF | Generate next | Motion generator | Names the module that consumes the context. |
| CoF inset | Fixed latent target | Target latent | The ground-truth motion encoding stays fixed. |
| CoF inset | Sampled / Recorded structure | Sampled / Target embedding | Origins are continuous codebook embeddings, not discrete token IDs. |
| CoF inset | Rebased detail / Detail | Rebased residual / Target residual | Displacements to the same target latent. |
| Representation | Full code | Latent | The encoder output reconstructed by anchor plus residual. |
| Representation | Full / Structural supervision | Full-motion loss / Structural loss | Names the actual objectives. |
| Overview | Structure planner | Structural planner | The autoregressive structural-token model. |
| Overview | Commit segment | Committed prefix | The retained leading portion of the sampled plan. |
| Overview | Joint view / Geometry view | Joint motion / Body geometry | Distinguishes native joint variables from Cartesian landmarks. |
| Overview | Structural-view reconstruction | Structure-only reconstruction | Decoder input contains only the structural embedding; its output is still complete motion. |
| Overview | Learn continuation | Continuation training | Training on the subsequent motion under constructed context. |
| Overview | Next-segment targets | Future-motion targets | Ground-truth encodings that supervise continuation. |

Ground-truth context and self-generated output are established distinctions in
[Self Forcing](https://arxiv.org/abs/2506.08009). This source supports terminology,
not claims about MuRoDance's implementation. The implementation sources below
establish the actual operations. Standard operation labels such as Encode,
Sample, Commit, Discard, append, and compute remain concise and accurate.
Random seeds and temporal segments remain valid terms in experimental protocols;
this revision removes their ambiguous use as figure labels, not the terms globally.

## Supervision shown without duplicate anatomy

The accepted long encoder/codebook/decoder composition is preserved. The rejected
cell masks and proposed duplicate humanoid supervision views are replaced by two
simple, named coordinate bands on each side of a reconstruction comparison.
Blue represents the selected structural coordinates and orange their complement.
The full-motion loss compares both to ground truth. The structural loss compares
only blue; faint orange still belongs to the complete reconstruction. These are
kinematic coordinate subsets, not two independent anatomical decoders or an
independent detail-only objective. The caption includes velocity coordinates and
identifies band widths as schematic. Native joint and Cartesian selections are
specified in the method, rather than conflated into one limb-color pictogram.

## Source checks

The immutable implementation is `lbtwyk/Musics2Dance` at
`24f4f75aa17c3622071e4fa6b1491ca5f2eabcb2`; file URLs and hashes are in
`source-manifest.json`.

- `g1_hybrid_streaming_codec.py:307–345`: full latent and structural embedding
  use the same boundary-conditioned decoder; both return complete motion.
- `g1_motion_projectors.py:27–75,451–474`: structural subsets exist in native,
  native-velocity, Cartesian-position and Cartesian-velocity blocks. Wrist
  positions and arm joint variables must not be treated as the same selection.
- `g1_motion_tokenizer.py:88–95`: nearest-prototype assignment; the selected
  visible prototype remains nearest and the residual arrow is its displacement.
- `train_g1_listenahead_mrt2.py:397–540`: one no-gradient model transition
  constructs context, followed by training with ground-truth targets.
- `train_g1_paper_faithful_dc_streaming.py:2258–2415`: the committed prefix
  updates history and decoded boundary state together; the discarded tail does
  not enter the next context.
- `train_g1_listenahead_mrt2.py:500–540`: residual target is fixed motion latent
  minus the sampled codebook embedding. The target codebook embedding is nearer
  to the target latent than the alternative sampled embedding in the schematic.

## Complete active-figure audit

`figure-label-audit.json` inventories every text label in each included SVG.
The overview's other labels retain their source-faithful meanings: frozen music
prediction, FiLM conditioning, paired discrete/residual generation, shared decoding,
committed history, boundary state, and the reference/control interface. The method
figures retain one shared decoder, paired context updates, and a fixed rebasing
target. Proper names and module acronyms remain unchanged. Only eight text nodes
in the overview changed; its geometry, illustrations, and connections are intact.
