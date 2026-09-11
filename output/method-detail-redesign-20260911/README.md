# ForeDance method figures — final vectors

The three figures are integrated in the 12-page manuscript. The approved main
overview and teammate SONIC figure are unchanged. The original 60-second
motion frames are retained, with a tighter three-frame layout.

## Deliverables

- [Music conditioning SVG](../../figures/foredance/music-conditioning-detail.svg)
  and its sibling PDF: the accepted physical-time alignment
  and residual-FiLM figure; the SVG is retained unchanged.
- [Representation SVG](../../figures/foredance/structure-detail-training.svg)
  and its sibling PDF: the v6 imagegen composition,
  reconstructed with native geometry and editable text. One shared pose master
  per pose is reused for the two supervision views.
- [Commit Forcing SVG](../../figures/foredance/cof-terminology.svg)
  and its sibling PDF: the v6 imagegen comparison. TF and CoF occupy
  matched rows; the separate geometric inset explicitly names residual rebasing
  and shows both residuals ending at the same recorded target.
- `final-figures.pdf` / `.png`: a combined review sheet.
- `raster-vector-comparison.pdf`: unchanged imagegen rasters beside the final
  native vector reconstructions.
- [ForeDance.pdf](../../ForeDance.pdf): the rebuilt complete paper.
- `foredance-method-vectors.zip`: the final figures, selected imagegen rasters,
  prompts, comparison document, and verification records.

Canonical figure sources are in `figures/foredance/`. Figure captions and the
method text were aligned to these designs. Low-level gradient definitions remain
in appendix equations. The duplicate appendix CoF workflow was consolidated
into the main comparison; its historical source remains available.

## Design provenance and permitted corrections

The built-in imagegen tool produced `representation-candidate-v6.png` and
`commit-candidate-v6.png` from the complete standalone prompts in
`imagegen-representation-v6-prompt.txt` and `imagegen-comparison-v6-prompt.txt`.
Neither generation used a reference image, and neither used a raster repair.
The user asked to continue through generation and final vectorization.

The vectors retain the selected composition, shape relationships, paired rows,
and palette. Solid fills remove incidental raster shading; Helvetica and line
weights are unified with the accepted conditioning figure. The three motion
poses are reconstructed once and recolored, preserving their exact geometry
between supervision views. Boundary glyphs use the common pose/velocity visual
language. Both code histories now share the same ellipsis gap. The strong
residual vector is explicitly labeled “Residual rebasing” per the final request.
This is a geometric reconstruction with semantic corrections, not a claim of
pixel-identical tracing. No bitmap is embedded in any of the three SVGs or PDFs.

## Verification

- All three SVGs contain native editable text, paths, and shapes, with no image
  elements, bitmap data, or external asset dependencies.
- Fonts in the exported PDFs are Helvetica and, for conditioning notation,
  Times New Roman. Text bounds fit the figure canvases.
- The actual manuscript compiled to 12 pages with no unresolved references,
  missing characters, or overfull boxes. Underfull spacing and PDF-version
  notices remain; they do not clip the figures.
- Rendered pages 4–6 were inspected for placement, labels, arrow clearance,
  captions, and the unchanged SONIC / original-frame material.
- Protected source and evidence files retain their recorded hashes. The
  evaluator/experiment appendix after “Evaluation Protocol” is unchanged.
- `vector-validation.json` and `paper-validation.json` retain the checks.

Source evidence is documented in `mechanism-audit.md`. Generators:
`scripts/build_music_conditioning_detail.py`, `scripts/finalize_method_details.py`
and `scripts/figure_svg_primitives.py`. The last script is a shared SVG helper.
Run the finalizer with `--all` to regenerate all three, or without it to keep
the accepted conditioning export untouched. Python, CairoSVG, and Cairo are
required; the configured workspace runtime supplies them.
