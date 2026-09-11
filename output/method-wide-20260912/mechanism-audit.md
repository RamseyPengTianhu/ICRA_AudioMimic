# Scientific and visual checks — 12 September 2026

Authoritative implementation: `lbtwyk/Musics2Dance` at immutable commit
`24f4f75aa17c3622071e4fa6b1491ca5f2eabcb2`. Retrieval paths and hashes are
in `source-manifest.json`.

## Representation

`g1_hybrid_streaming_codec.py:307–345` gives a full latent and a structural
embedding to the same state-conditioned decoder. Both reconstruct complete
motions. The figure retains two routes, one decoder and neutral complete poses.

`g1_motion_projectors.py:27–75,451–474` selects coordinates in four blocks:
native motion, native velocity, Cartesian positions and Cartesian velocities.
Native selection and Cartesian landmark selection differ: arm joint variables
are not interchangeable with wrist positions. Therefore one whole-limb color
cannot represent both losses. Full supervision fills every mask cell; structural
supervision selects coordinates in every row. Both rows reuse exactly the same
neutral pose artwork. Counts and positions in the masks are schematic, not a
coordinate inventory. Exact selections remain in the manuscript.

`g1_motion_tokenizer.py:88–95` uses Euclidean nearest-prototype assignment.
The selected point is closer to the encoded point than every other visible
prototype. The offset arrow follows their displacement. Codebook and point
markers are exact circles; encoder and decoder have symmetric trapezoid sides.

## TF, self-rollout context and rebasing

`train_g1_listenahead_mrt2.py:397–540` samples a first plan without gradients
from recorded seed context. It constructs the next context, then trains the
next-segment models with recorded supervision. This is one training transition;
the figure does not claim recursively accumulated training rollouts.

`train_g1_paper_faithful_dc_streaming.py:2258–2415` decodes the sampled plan,
derives the new state from its committed motion prefix, and appends the same
discrete/residual prefix to the history. History and state are replaced together.
The discarded tail supplies neither history nor state. In the drawing, recent
TF tiles match the recorded source and recent CoF tiles match the generated
commit in both discrete symbols and residual traces. Both contexts retain the
same illustrated earlier history. The arrows enter the matched context groups
only from the selected source. Aligned music remains implicit in this focused
comparison and is still explained by the overview and method text.

`train_g1_listenahead_mrt2.py:500–540` conditions the residual loss on a sampled
next structure and rebases the residual target as fixed latent minus the sampled
embedding. Both geometric arrows reach exactly the same target. The recorded
prototype is closer than the alternative sampled origin; offsets are collinear
with the corresponding point pair and clipped to leave arrowheads visible.
Rebasing does not mean re-encoding the target under the generated boundary state.

## Visual evidence and protected material

The fresh imagegen comparison was inspected. Its repeated Commit labels, extra
return arrowhead, mismatched history contents and unequal comparison groups were
corrected in the native vector revision. The original long representation was
preserved apart from regular geometry, state input indication and supervision.
Both method SVG/PDF files contain native shapes and editable text, with no images.

Checks cover stroke/text, small filled glyph/text and text/text intersections,
as well as figure bounds and scientific geometry. Page 5 of the rebuilt paper
was visually inspected. The overview wordmark is the sole overview change;
the SONIC figure, numeric evidence and result frames retain their original hashes.
User-pulled changes from `c7fa384` are preserved. The title's Unicode dash is
written as equivalent TeX `--` to render with the existing font setup.

The conditioning subfigure and every reference to it were removed. Its methods
and original standalone assets remain. The author explicitly kept the appendix
disabled, so inherited appendix references are unresolved in the PDF. There are
no new unresolved figure references, missing glyphs or overfull boxes.
