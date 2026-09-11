# MuRoDance method figures — full-width revision

The author restored both method figures to two-column width and removed the
separate conditioning figure. The final manuscript is `ForeDance.pdf`; the
two revised method figures appear on page 5. The overview changes only its
upper-left wordmark to MuRoDance. SONIC and the disabled appendix are preserved.

## Included figures

- **Representation:** preserves the original long encoder/codebook/shared-decoder
  composition. The codebook is a regular circle and the selected prototype is
  actually nearest to the encoded point. Both output rows show complete neutral
  motions. Blue/empty coordinate masks distinguish full and structural supervision;
  limb color no longer implies an incorrect anatomical loss selection.
- **Commit Forcing:** matched TF/CoF contexts feed next-segment generation. TF uses
  a recorded segment. CoF samples a plan from a recorded seed, commits its prefix,
  appends that prefix to history and derives the paired state from decoded motion.
  The faded tail has no outgoing connection. A geometric inset retains rebasing
  to the same fixed target. The diagram illustrates one training transition.

## Files

Editable SVG and vector PDF masters are in `figures/foredance/`.
`final-figures.pdf` and PNG provide the combined preview; `full-width-proof.pdf`
shows actual print size. `comparison.pdf` compares with the original long figures.
`murodance-method-vectors.zip` contains the masters, previews and review records.
The conditioning assets remain in the repository but are excluded from the paper
and this delivery bundle.

`cof-wide-candidate.png` and `cof-imagegen-prompt.txt` preserve the fresh built-in
imagegen design. Native reconstruction corrects its repeated Commit labels,
extra arrowhead, inconsistent histories and unequal context-group sizes. The
original long representation is the visual baseline for the supervision repair.
No bitmap is embedded in either final method SVG/PDF. The overview retains its
existing illustrations.

## Verification

Native shapes, all four supervision blocks, nearest-prototype geometry, fixed
rebasing target, text bounds, line/arrowhead-to-text and text-to-text clearance
were checked. The page was visually inspected at manuscript size. Figure labels
are at least about 7.1 pt at full width. Compilation has no missing characters or
overfull boxes. Existing appendix references remain unresolved because the author
explicitly kept the appendix disabled; no new figure reference is unresolved.

Source evidence and limitations are recorded in `mechanism-audit.md`,
`source-manifest.json`, `reference-record.json` and `validation.json`.

## Rebuild

With CairoSVG, Cairo, PyMuPDF and Pillow available, run
`scripts/build_wide_method_figures.py`, copy the two SVG/PDF pairs to
`figures/foredance/`, then compile `main.tex`. Run
`scripts/review_wide_method_figures.py` for geometric and clearance checks;
inspect the resulting paper page after any placement change.
