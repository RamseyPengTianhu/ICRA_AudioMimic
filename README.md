# ForeDance RA-L manuscript

Current title: **ForeDance: Structured Streaming Dance Generation with Anticipatory Music Conditioning**.

This FineDance manuscript now uses the official RA-L **initial/revised submission** format: `ieeeconf`, US Letter, 10 pt, two columns, an anonymous author byline, and IEEE numbered references. This is not the accepted-paper journal layout. The directory name is retained for compatibility. `main.tex` is the entry point; sections live in `sections/`. The working PDF is `build/main.pdf`; the checked-in reading copy is [ForeDance.pdf](ForeDance.pdf).

The RA-L layout is retained while the accepted MMR correspondence evidence now supplies the main numerical music result. It does not make the paper submission-ready. RA-L permits six pages plus at most two extra pages, **including references and all appendices**. The retained appendix files are compiled within that same manuscript, in two columns; they are not a separately admissible textual supplement. Content must still be reduced to the page limit and pending evidence completed before submission. Do not upload extra text/figures as multimedia to bypass the limit.

The three contributions are anticipatory music conditioning, kinematics-guided structure–detail decoupling with its paired training, and Commit Forcing. FHC and the MMR evaluator support the story. The manuscript is written as a contribution-led research paper. Generation follows the current ForeDance specification; the fixed-controller interface incorporates the teammate execution work. A separately identified earlier-configuration MuJoCo replay table is supporting evidence in the supplement, not a current-model result. It does not assume completed evidence for the three unfilled core comparisons; their status is stated briefly alongside the planned comparisons. Author instructions and historical evaluation planning are outside the compiled manuscript.

The music evaluation now separates reference-motion evaluator validation from evaluation of ForeDance generations. The generator table contains one learned-correspondence score and BAS, with their 60-second/11-track and 23-second/18-track cohorts identified. Startup variants are not displayed as competing methods. The matched history-training table contains clean history, dropout and corruption, including BAS. Full conditional correspondence statistics remain in the appendix; complete alternative outcomes and reporting choices remain in the evidence archive, with a single Discussion disclosure. Missing anticipation, paired-representation, single-representation and continuation ablations are explicit TODO paragraphs in the working manuscript and are tracked in `TODO.md`.

## Build

Use a complete TeX Live/MacTeX installation, or set `main.tex` as the Overleaf main document with pdfLaTeX:

```sh
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build main.tex
```

Or use Tectonic with its normal bundle available:

```sh
tectonic --keep-logs --outdir build main.tex
```

Regenerate the generation tables and verify the archived execution-table transcription from the archived original summaries:

```sh
python3 scripts/build_evidence_tables.py
python3 scripts/build_mmr_tables.py
```

The manuscript uses standard LaTeX packages; the official class and bibliography style are included locally so Overleaf does not depend on a system installation of `ieeeconf`.

## Bibliography

`Reference.bib` retains complete author lists for the cited publication versions. The `ForeDance:BSTcontrol` entry, activated by `\bstctlcite` before the first citation in `main.tex`, prints the first three authors followed by *et al.* for works with more than three authors; works with one to three authors retain all names. This is a manuscript-level display choice, not a change to the official `IEEEtran.bst`. Repeated author lists are printed rather than replaced by a dash.

The merged library contains 53 literature entries plus this nonprinting style-control record. All 51 entries in the supplied list were already present; the two additional method references are retained. The compiled manuscript currently cites 38 works. Uncited entries remain available without being forced into the PDF. Citation keys remain stable when publication years or venues are corrected. Version reconciliation and primary-source links are recorded in [the reference audit](evidence/foredance/REFERENCE_AUDIT.md).

## RA-L template provenance

The format follows the [official RA-L author instructions](https://www.ieee-ras.org/publications/ra-l/ra-l-information-for-authors/), checked on 2026-09-10. Initial and revised submissions use the conference class specified there; accepted manuscripts require a separate final-format conversion.

The following files are extracted unchanged from the packages linked by those instructions, with their upstream license notices retained:

- `ieeeconf.cls`: [PaperCept ieeeconf.zip](https://ras.papercept.net/conferences/support/files/ieeeconf.zip), SHA-256 `4befef671c2a996889d325f5170d3387bf42aac9a37dcaa93724ad49816e4ec2`.
- `IEEEtran.bst`: [PaperCept IEEEtranBST.zip](https://ras.papercept.net/conferences/support/files/IEEEtranBST.zip), SHA-256 `b11af8e5096681f1eccdce6c72c047dc056ddeef52dff340213104019bcf3409`.

No custom page geometry, title-space compression, caption package, or single-column appendix overrides the official layout. Submission-wide anonymity (including figure and artifact contents) remains a final author check; the format conversion removes identifying PDF author metadata and leaves the byline blank.

## Figures and evidence

- `figures/foredance/`: four main figures: the combined ForeDance overview, D+C training, CoF, and actual 60-second generation frames. The active image paths are declared in the sections.
- `evidence/foredance/EVIDENCE_MAP.md`: source revisions, evidence identity and limitations.
- `evidence/foredance/image-prompts.json` and `image-revisions.json`: exact image-generation prompts.
- `evidence/foredance/REFERENCE_AUDIT.md`: primary sources, publication-version reconciliation, and citation coverage checks.
- `TODO.md`: specific missing evidence before a submission-ready result claim.
- `PAPER_DECISIONS.md`: latest approved direction plus preserved historical decisions.

Method diagrams were produced with the built-in imagegen tool and visually checked. The interface has no model or quality selector: the requested Image 2.5 / highest-level sunburst setting could not be verified. No generated illustration is used as measured dance or execution evidence.

Figure 1 uses `figures/foredance/overview.pdf`, exported from the editable `overview.svg`. The refinement is based on the author-selected `output/overview-editable-20260911/overview-editable.png`: its panel bounds and palette are retained; local spacing follows author corrections. The bottom legend now sits beside the ForeDance title in place of the explanatory subtitle, and the former footer is cropped, giving a 1536 × 956 canvas. The header explains the four meaningful colors and the Frozen symbol; the ambiguous External module entry is removed. Purple denotes Motion context and is used for the original context blocks in b and d. The first three training steps carry a no-gradients scope label; supervision is labeled Next-segment targets (encoded from data). Changes repair connector crossings and endpoints, separate boundary-state and measured-feedback routes, use Context / Boundary state terminology and an append return label, show shared decoding inside both reconstruction paths, and use robot variants derived from one neutral master. Music conditioning remains in panel b, without a connector from panel a. Five transparent robot/human illustrations plus the official Magenta RealTime 2 icon are separately available and embedded in the SVG. Rebuild with `python scripts/refine_overview_editable.py`, check with `python scripts/validate_overview_refined.py`, and activate the verified output with the builder’s `--activate` option. The title uses the supplied `figures/foredance/foredance-logo.svg` wordmark as native paths, and the two boundary-state symbols show a posed humanoid without an arrow. The history/state pairs in b and d use matching vertical separators. Sampled q has a separate Embed + add arrow and a codebook-embedding path; Learn shows flame-marked Structure and Detail models. Both decoder instances in c carry flames; the b feedback payload has explicit compute and append arrows. Figure labels use Helvetica without horizontal compression, and mathematical symbols remain italic. The conditioning label sits below its arrow with clear spacing from both modules. Font examples and the verified input mechanism are recorded in `evidence/foredance/overview-typography-research.json`. The reading copy matches `build/main.pdf`. The published preview and checks are in `output/overview-refined-20260911/`; the selected earlier layout is retained for comparison. Additional comparison PDFs, asset archives and rejected candidates remain in the local working folder.

The editable `.tex` figure layouts are retained as schematic sources. They are not pixel-identical reproductions of the generated assets. Previous image drafts remain named separately and are not active manuscript figures.

The original local manuscript and its uncommitted changes were backed up outside this repository in `../paper-backups/pre-foredance-20260909-203922.tar.gz`. No new training or controller experiment is part of this revision. The user authorized publishing the checked integration to GitHub on 2026-09-10.

## Teammate integration

The 2026-09-10 integration merges Overleaf revision d12a5c0 while retaining the ForeDance title, current 38D/71D generator, main figures, and generation evaluation. The latest teammate interface is adapted to absolute-orientation reconstruction. Earlier 34D execution diagnostics from 0cc6cee are identified separately in the supplement. Exact source snapshots and transcription provenance are retained under evidence/foredance/team-execution/. Additional teammate literature and the inactive architecture image remain available; only cited works appear in the PDF.
