# Overview figure vector reconstruction — 2026-09-10

The active Figure 1 has been reconstructed from `figures/foredance/overview.png` into editable `overview.svg` and a PDF 1.5 companion, `overview.pdf`. The introduction includes the PDF at the original width and aspect ratio. The original PNG remains unchanged.

## Choice of method

| Route | Fidelity and editability | Decision |
| --- | --- | --- |
| Embed the complete PNG in SVG or PPTX | Preserves pixels, but text and lines remain raster | Does not meet the print-sharpness objective |
| Automatic bitmap tracing | Produces vector contours, including outlines around raster text; does not recover semantic labels or original drawing objects | Poor fit for small text, shaded robots, and a dense method diagram |
| Reconstruct diagram objects and preserve original robot crops | Editable labels, boxes, arrows, tokens and waveform; preserves detailed robot artwork | Used |
| PPTX intermediate | Requires the same reconstruction; introduces another export step | Unnecessary for this SVG/PDF delivery |

Primary documentation consulted:

- [Inkscape bitmap tracing tutorial](https://inkscape.org/en/doc/tutorials/tracing/tutorial-tracing.ru.html/): tracing creates paths from bitmap content.
- [Inkscape command-line export](https://wiki.inkscape.org/wiki/Using_the_Command_Line): SVG can be exported to PDF.
- [CairoSVG documentation](https://cairosvg.org/documentation/): SVG-to-PDF conversion, embedded raster-image support, and limitations of advanced font features.

The choice above is a local engineering assessment, not a claim of lossless automatic conversion. The generated PNG has no recoverable native shapes or font metadata. This version retains content, layout, palette, connectivity and robot poses, but is not pixel-identical: fonts, gradients, icons and waveform strokes have been reconstructed. The SVG is a hybrid vector figure, not a fully vectorized robot illustration.

## Figure content and invariants

Read the current abstract, introduction, related work, method, experiments and discussion before rebuilding. Figure 1 conveys causal musical forecasting, coupled structure/detail generation, joint prefix commitment, reference-derived feedback, kinematic supervision and Commit Forcing. No scientific claims, captions, results, or other figures were revised.

The two music-conditioning arrows and two motion-context arrows remain separate. Structure conditions detail. The committed output updates history and reconstructs the reference state. The recorded training target enters the next-plan stage. Robot poses remain schematic and retain the original caption's evidence boundary.

## Reproduction

Run `python scripts/build_overview_vector.py` with Pillow, CairoSVG and Cairo available. On macOS, the Cairo dynamic-library directory may need to be added to `DYLD_FALLBACK_LIBRARY_PATH`. The script measures text with Cairo and uses explicit horizontal transforms rather than unsupported SVG text-length features. The print PDF embeds fonts; the editable SVG uses Arial and Times New Roman with fallbacks, so another machine's font substitution may slightly alter appearance.

The source canvas is 1685 × 934. Exactly three lossless crops are embedded, in original pixel coordinates:

- Streaming poses: `(1240, 323, 1657, 518)`.
- Joint-view robot: `(40, 646, 149, 843)`.
- Geometry-view robot: `(300, 646, 424, 843)`.

Waveform extents are extracted from the source's teal pixels. All remaining diagram content is recreated as SVG text and geometry. The source PNG is required to regenerate the figure, but the delivered SVG is self-contained.

## Verification

The first conversion was checked against the earlier 15-page draft. After author review, the repository was advanced to upstream `4b01016ef921f1b647c7ee0460ea5ee05498167a`, including the RA-L format and revised narrative. The delivered PDF retains that upstream reading copy’s 12 pages. Render comparison changes only page 3; text below the figure is unchanged. The final figure has four embedded images and hundreds of vector drawing objects, with extractable labels. Detailed hashes and checks are recorded in `overview-vector-validation.json`.

## Author review adjustments

- Replace the star-like symbol with a six-arm branched snowflake.
- Use the official name **Magenta RealTime 2** and the official MRT2 application icon from [the Magenta repository](https://github.com/magenta/magenta-realtime/blob/main/examples/mrt2/auv3/assets/AppIcon.icns). The asset was converted losslessly from ICNS to PNG. This identifies the model's official application asset, not a separately claimed model logo. Name verified against [the official release](https://magenta.withgoogle.com/magenta-realtime-2).
- Sample the original image's individual music-bar colors, preserving differences between forecast-state tiles.
- Expand the lower headings to **Discrete Structure + Continuous Detail** and **Commit Forcing**.
- Replace the storage-cylinder commit icon with retained-prefix tiles, a cutoff line, and a check mark.
- Remove the corner disclaimer, parenthetical notes, and explanatory footer sentences from the figure. Preserve necessary module and view labels. Use the snowflake for frozen parameters, matching teal tiles for musical context, shared decoder glyphs linked across reconstructions, one enclosure for paired history and state, and a blocked backward-gradient path for the generated transition. The paper caption and method retain the scientific explanations.

The revised SVG has four embedded images: three original robot crops and the official application icon. Other drawing elements and all labels remain vectors.

## Latest-paper integration and PDF reproduction

The upstream commits, trees and all missing blobs were fetched from the repository using Git’s upload-pack endpoint plus verified byte-range retrieval after repeated transport timeouts. Every downloaded blob was checked against its Git object ID. The local `main` branch fast-forwarded from `2dd06e7` to `4b01016`; local figure changes were backed up before integration. No remote push was performed.

The revised source compiles successfully with the local Tectonic engine, but it produces 13 pages while upstream’s pdfTeX reading copy has 12. To preserve the requested latest-paper layout exactly, `scripts/place_overview_in_pdf.py` removes the original overview image invocation and places the vector figure in precisely the same rectangle in the upstream PDF. All other pages and text below the figure remain unchanged. `ForeDance.pdf` is this 12-page delivery; `build/main.pdf` is the local 13-page compiler output, retained for diagnostics. Both are based on the latest source, and `sections/introduction.tex` references the vector PDF for subsequent pdfLaTeX/Overleaf builds.

To reproduce the layout-preserving delivery, extract `ForeDance.pdf` from upstream commit `4b01016` to a temporary path, then run `python scripts/place_overview_in_pdf.py upstream.pdf output.pdf` with PyMuPDF available. The original PDF and source PNG remain available in Git history. Never use an already replaced PDF as the script’s input.
