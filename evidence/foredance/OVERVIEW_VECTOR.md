# Current overview refinement — 2026-09-11

The author explicitly selected `output/overview-editable-20260911/overview-editable.png` as the baseline. Its original canvas is 1536 × 1024. Keep its blue/orange/teal/purple palette, panel boundaries and main module arrangement. The author subsequently moved the bottom legend beside the ForeDance title, replacing the explanatory subtitle, and removed the former footer; the current canvas is 1536 × 956. The ambiguous External module legend item was then removed; the remaining four color meanings and Frozen symbol are evenly arranged beside the title. The larger 1536 × 1080 strict-layout alternative was rejected and is not active.

The active `figures/foredance/overview.svg` and `overview.pdf` repair the music/context crossing, give arrows exact module-boundary endpoints, separate the reference-state return from the other context input, avoid a generator border passing through the commit module, and separate the reverse-gradient and recorded-target paths. Music starts locally in b and feeds two distinct FiLM inputs. The author follow-up changes the labels to Context and Boundary state, removes Paired from b, and adds append above the return arrow. FiLM labels now clear the full arrowheads. Anatomy explanations in c are smaller single lines. Each reconstruction path includes its D_psi decoder, and a dashed parameter-sharing link identifies their shared decoder; the disconnected footer icons are removed. The reconstruction cards now have a 40 px gap with the sharing label centered between them. In d, the bracket under steps 1–3 is labeled Context generation (no gradients). The reverse dashed arrow and Stop gradient box are removed, so no backward data-flow path is implied. The supervision box reads Next-segment targets (encoded from data), matching the fixed recorded structural and latent targets described in method.tex and supplement.tex. The purple legend reads Motion context, and the original single-row history blocks in b and d use purple instead of gray. Other composition choices remain those of the specified reference. Sampled q now has separate paths to its codebook embedding and to residual diffusion. The conditioning arrow is labeled Embed + add below its horizontal segment, clear of both module boxes. Its start is on q rather than the codebook embedding e(q); the separate residual-model embedding and additive injection are verified against the paper-audited implementation, as recorded in overview-typography-research.json. Learn replaces output-like token strips with two model cards, Structure and Detail, each marked by a flame. The legend defines the flame as Trainable alongside Frozen. Both decoder instances in c are also marked by Trainable flames. The b return route now has explicit compute and append arrows on opposite sides of the history/boundary-state payload. No manuscript prose or scientific results were changed in this refinement. Commit/discard is now drawn by one shared glyph in b and d: identical tile dimensions, three retained tiles, two pale outlined discarded tiles, and a dashed cutoff. Commit and Discard appear directly above the corresponding column groups. D labels the upper row and C the lower row throughout the paired-latent illustrations. The two selection glyphs were rendered independently and verified pixel-identical when aligned. An earlier author correction borrowed two inner schematics from `figures/foredance/overview2.png`: noise tiles flowing into residual tiles under Residual diffusion, and discrete/continuous rows labeled D/C with the uncommitted tail faded in Commit segment. Detail generator and the earlier wave illustration are removed. The subsequent commit/discard correction above supersedes that component’s earlier appearance. The earlier header/footer-only revision preserved panel pixels; the subsequent author-requested typography revision changes text throughout all four panels.

One neutral robot image is reused in training, geometry supervision and generated state. Color and dance-pose variants are source-conditioned on that same master. These are artistic variants, not proof of physically exact rigging. Imagegen produced checkerboard backgrounds in the variants; after explicit author permission, Apple Vision supplied foreground masks and a separate operation added alpha while preserving every RGB pixel. Raw images, masks, complete prompts and preservation checks are in `figures/foredance/transparent-assets/`. The official icon and human source remain unchanged. The delivered figure is a hybrid SVG: native editable text, shapes, symbols and connectors with six unique transparent PNGs in eight placements. The two boundary-state symbols now share one native posed-humanoid design. The author removed their velocity arrows; the d history/state pair now uses the same pale vertical separator as b. These two local regions are the only pixels changed from v12, and the standalone icon is updated too. The title is the author-provided ForeDance wordmark, traced into ten editable paths in foredance-logo.svg. Its black and blue fills are sampled from the original PNG, the background is transparent, and there are no embedded images or font dependencies in that standalone logo. The source PNG is retained unchanged; contour and rendering checks are in foredance-logo-validation.json.

Run `python scripts/refine_overview_editable.py` and `python scripts/validate_overview_refined.py`. After review, the builder's `--activate` option installs the SVG/PDF as the active overview. `scripts/foreground_mask.swift` generates foreground masks; `scripts/apply_foreground_alpha.py` applies a saved mask without changing RGB. Earlier builders reproduce historical candidates, not this active revision.

The measured checks found no label overlap or edited connection crossing an unrelated module. All four panel styles and bounds are unchanged. In the latest typography revision, every non-text SVG attribute remains identical to revision v11 except the conditioning connector, and every illustration placement is unchanged. Text uses Helvetica regular/bold with italic mathematical symbols; all 18 former horizontal compressions are removed. The four anatomy explanations use 12 px text, with remaining body points shortened to other body points. The PDF embeds the chosen fonts; the SVG retains editable text. The legend has moved to the header as requested. The actual paper compiles to 11 pages with the figure on page 2; that page was visually inspected. The initial footer removal reflowed pages 2–11. This latest typography revision changes only page 2; all ten other pages match revision v11 pixel-for-pixel. No missing glyphs, unresolved references or overfull boxes were found; existing underfull paragraph warnings remain. See `overview-refined-validation.json` and `output/overview-refined-20260911/`. The author subsequently requested publication of this reviewed revision to the existing paper GitHub main branch. The candidate-only publication holds in earlier records are superseded.

## Earlier reconstruction record

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
