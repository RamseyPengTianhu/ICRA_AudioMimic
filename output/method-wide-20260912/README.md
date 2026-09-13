# MuRoDance method figures — full-width revision

Updated 13 September 2026 from the latest paper main (`ec53c189`). All three
included figures have a terminology audit. The two method figures remain at
two-column width on page 5; the overview remains on page 2. The rebuilt manuscript
is `ForeDance.pdf` (eight pages).

- **Representation:** retains the original long encoder, codebook, and shared
  decoder composition. Two simple blue/orange coordinate bands show comparison
  with ground truth. Full-motion loss supervises both; structural loss selects
  blue only. Both paths reconstruct complete motion. No supervision grids or
  repeated anatomical pictograms remain.
- **Commit Forcing:** compares ground-truth and model-generated conditioning
  contexts. The committed prefix supplies both history and boundary state.
  The faded tail has no outgoing connection. The rebasing inset distinguishes
  sampled and target codebook embeddings and their residuals to one fixed latent.
- **Overview:** eight wording changes clarify the same terminology without
  changing the layout, geometry, connections, or illustrations.

All boundary-state cues retain the same purple humanoid glyph. The separate
conditioning and teammate SONIC figures remain disabled, as in the pulled paper;
their source assets are unchanged. The appendix remains disabled by request.

Editable masters and publication PDFs are in `figures/foredance/`.
`final-figures.pdf` and PNG provide a combined preview; `full-width-proof.pdf`
shows print size. `comparison.pdf` compares with the original long references.
`murodance-method-vectors.zip` contains all three current figures and audit records.
The two method figures are entirely native vectors. The overview retains its
previously authorized embedded raster illustrations and editable diagram objects.

See `terminology-audit.md`, `mechanism-audit.md`, `figure-label-audit.json` and
`validation.json` for source evidence and checks. Prior raster references and
prompts are preserved as design provenance, not presented as current figures.
