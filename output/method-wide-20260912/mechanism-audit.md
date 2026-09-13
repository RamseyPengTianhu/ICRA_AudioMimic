# Scientific and visual checks — 13 September 2026

Authoritative implementation: `lbtwyk/Musics2Dance` at immutable commit
`24f4f75aa17c3622071e4fa6b1491ca5f2eabcb2`. Retrieval paths and hashes are
in `source-manifest.json`.

## Representation

`g1_hybrid_streaming_codec.py:307–345` gives a full latent and a structural
embedding to the same state-conditioned decoder. Both reconstruct complete
motions. The figure retains two routes and one decoder. Its two output comparisons
use named blue/orange coordinate bands rather than duplicate anatomical artwork.

`g1_motion_projectors.py:27–75,451–474` selects coordinates in four blocks:
native motion, native velocity, Cartesian positions and Cartesian velocities.
Native selection and Cartesian landmark selection differ: arm joint variables
are not interchangeable with wrist positions. The bands denote coordinate
subsets across these blocks, not body parts. Both subsets are compared with
ground truth through double-headed links for full-motion loss, while only the blue subset is compared for
structural loss. Faint orange coordinates still belong to the complete output.
There is no independent detail-only loss. Band widths are schematic.

`g1_motion_tokenizer.py:88–95` uses Euclidean nearest-prototype assignment.
The selected point is closer to the encoded point than every other visible
prototype. The offset arrow follows their displacement. Codebook and point
markers are exact circles; encoder and decoder have symmetric trapezoid sides.

## TF, self-rollout context and rebasing

`train_g1_listenahead_mrt2.py:397–540` samples a first plan without gradients
from ground-truth context. It constructs the next context, then trains the
next-segment models with ground-truth supervision. This is one training transition;
the figure does not claim recursively accumulated training rollouts.

`train_g1_paper_faithful_dc_streaming.py:2258–2415` decodes the sampled plan,
derives the new state from its committed motion prefix, and appends the same
discrete/residual prefix to the history. History and state are replaced together.
The discarded tail supplies neither history nor state. In the drawing, recent
TF tiles match the ground-truth source and recent CoF tiles match the generated
commit in both discrete symbols and residual traces. Both contexts retain the
same illustrated earlier history. The arrows enter the matched context groups
only from the selected source. Aligned music remains implicit in this focused
comparison and is still explained by the overview and method text.

`train_g1_listenahead_mrt2.py:500–540` conditions the residual loss on a sampled
next structure and rebases the residual target as fixed latent minus the sampled
embedding. Both geometric arrows reach exactly the same target. The target
prototype is closer than the alternative sampled origin; offsets are collinear
with the corresponding point pair and clipped to leave arrowheads visible.
Rebasing does not mean re-encoding the target under the generated boundary state.

## Visual evidence and protected material

The latest scoped revision replaces every boundary-state cue in the two
subfigures with the exact purple pose glyph already present in the overview.
The five copies share one master, contain no waveform, and are pictograms rather
than measured pose values. Contexts still contain the complete state defined in
the method; removing a waveform does not remove its velocity coordinates.

The committed prefix is grouped by one lower bracket; the update arrow starts
at its midpoint and enters the next context's left edge. Both next-generation
arrows align with the context and module centers and retain a shaft longer than
their arrowhead envelope. The initial context tiles have non-overlapping spacing.

The fresh imagegen comparison was inspected. Its repeated Commit labels, extra
return arrowhead, mismatched history contents and unequal comparison groups were
corrected in the native vector revision. The original long representation was
preserved apart from regular geometry, state input indication and supervision.
Both method SVG/PDF files contain native shapes and editable text, with no images.

Checks cover stroke/text, small filled glyph/text and text/text intersections,
as well as figure bounds and scientific geometry. Pages 2 and 5 of the rebuilt
paper are inspected at publication size. Eight overview labels are updated;
its geometry and illustrations are unchanged. All upstream changes from
`ec53c1892ca1fa31b349f1d19ff10c0b319ea03d` outside the figure wording and associated
method/caption edits are preserved. The upstream introduction's Unicode dash is
written as equivalent TeX `--` to avoid a missing character in the existing font.

The separate conditioning and SONIC figures remain disabled, with their assets
unchanged. The author explicitly kept the appendix disabled, so inherited appendix
references remain unresolved in the PDF. The final checks report any missing
glyphs, overfull boxes, or unresolved figure references in `validation.json`.

See `terminology-audit.md` for the complete active-figure wording review.

## Alignment follow-up

CoF initial context, rollout tiles, updated context and generator now share one
horizontal centerline. Row names are optically centered on each row. Tile-group
labels share a baseline; history/state headings and Commit/Discard headings are
centered over their respective content. Boundary glyphs use their visible stroked
bounds for centering instead of their padded viewport. Reconstruction brackets
explicitly group both coordinate bands, and decoder arrows meet their midpoint.
These relationships are checked in `review_wide_method_figures.py`, in addition
to overlap tests and final manuscript inspection.

The label-correspondence revision adjusts the codebook's local point positions
while retaining nearest-prototype geometry. Each point label is adjacent to its
own point, and Detail is centered above the corresponding horizontal offset.
The boundary state is explicitly connected to the encoder as required by
`encode_clean_components(motion, state)`, as well as to the shared decoder.
The same glyph and state name identify these two uses. The initial CoF context
has an enclosure matching the subsequent context, and Commit/Discard labels have
span brackets. Connector labels use proximity to their own paths rather than a
shared arbitrary text baseline. Font size and weight follow information priority.
