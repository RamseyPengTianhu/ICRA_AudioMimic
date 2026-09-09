# ForeDance research manuscript

Current title: **ForeDance: Structured Streaming Dance Generation with Anticipatory Music Conditioning**.

This is the author-approved, venue-neutral FineDance research draft. The directory name is retained for compatibility. `main.tex` is the entry point; sections live in `sections/`. The working PDF is `build/main.pdf`.

The three contributions are anticipatory music conditioning, kinematics-guided structure–detail decoupling with its paired training, and Commit Forcing. FHC and the MMR evaluator support the story. The manuscript is written as a contribution-led research paper. It does not assume completed evidence for the three unfilled core comparisons; their status is stated briefly alongside the planned comparisons. Author instructions and historical evaluation planning are outside the compiled manuscript.

## Build

Use a complete TeX Live/MacTeX installation:

```sh
latexmk -pdf -outdir=build main.tex
```

Or use Tectonic with its normal bundle available:

```sh
tectonic --keep-logs --outdir build main.tex
```

Regenerate the two populated tables from the archived original summaries:

```sh
python3 scripts/build_evidence_tables.py
```

The local build used bundled Tectonic with cached format resources and byte-range retrieval of missing bundle files. That recovery is an environment workaround, not a manuscript dependency. The manuscript uses standard LaTeX packages.

## Figures and evidence

- `figures/foredance/`: four main figures: the combined ForeDance overview, D+C training, CoF, and actual 60-second generation frames. The active image paths are declared in the sections.
- `evidence/foredance/EVIDENCE_MAP.md`: source revisions, evidence identity and limitations.
- `evidence/foredance/image-prompts.json` and `image-revisions.json`: exact image-generation prompts.
- `evidence/foredance/REFERENCE_AUDIT.md`: primary sources and corrections for reference completion (39 cited entries).
- `TODO.md`: specific missing evidence before a submission-ready result claim.
- `PAPER_DECISIONS.md`: latest approved direction plus preserved historical decisions.

Method diagrams were produced with the built-in imagegen tool and visually checked. The interface has no model or quality selector: the requested Image 2.5 / highest-level sunburst setting could not be verified. No generated illustration is used as measured dance or execution evidence.

The editable `.tex` figure layouts are retained as schematic sources. They are not pixel-identical reproductions of the generated assets. Previous image drafts remain named separately and are not active manuscript figures.

The original local manuscript and its uncommitted changes were backed up outside this repository in `../paper-backups/pre-foredance-20260909-203922.tar.gz`. No training, commit, push, or remote publication is part of this revision.
