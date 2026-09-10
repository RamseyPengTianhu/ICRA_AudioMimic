# Reference completion — 2026-09-09

Reconciled all 37 existing bibliography entries with active prose: 15 previously uncited entries now have explanatory Related Work sentences. Added two method sources (rotation representation and diffusion). No forced bibliography inclusion or new experimental comparisons.

## Primary-source checks

The following pages were checked live for the added descriptions and bibliographic corrections. Previously cited entries outside this list were not all independently re-audited in this pass.

- [dhariwal2020jukebox](https://arxiv.org/abs/2005.00341)
- [yang2025megadance](https://proceedings.neurips.cc/paper_files/paper/2025/hash/102bd3c1076dfe98043b19340ac44e08-Abstract-Conference.html)
- [zhang2026opendance](https://openaccess.thecvf.com/content/CVPR2026/html/Zhang_OpenDance_Multimodal_Controllable_3D_Dance_Generation_with_Large-scale_Internet_Data_CVPR_2026_paper.html)
- [huang2025selfforcing](https://proceedings.neurips.cc/paper_files/paper/2025/hash/f4823f831af67a3ef15e41a85434422a-Abstract-Conference.html)
- [zhuang2026selfgradientforcing](https://arxiv.org/abs/2607.20368)
- [jiang2025motionstream](https://openaccess.thecvf.com/content/ICCV2025W/I-HFM/html/Jiang_Causal_Motion_Tokenizer_for_Streaming_Motion_Generation_ICCVW_2025_paper.html)
- [chi2023diffusionpolicy](https://roboticsproceedings.org/rss19/p026.pdf)
- [black2025rtc](https://proceedings.neurips.cc/paper_files/paper/2025/hash/300ccb2187dedd4edcc07f7e76d8e553-Abstract-Conference.html)
- [yuan2023physdiff](https://openaccess.thecvf.com/content/ICCV2023/html/Yuan_PhysDiff_Physics-Guided_Human_Motion_Diffusion_Model_ICCV_2023_paper.html)
- [luo2023phc](https://openaccess.thecvf.com/content/ICCV2023/papers/Luo_Perpetual_Humanoid_Control_for_Real-time_Simulated_Avatars_ICCV_2023_paper.pdf)
- [ji2024exbody2](https://arxiv.org/abs/2412.13196)
- [xie2026kungfubot](https://proceedings.neurips.cc/paper_files/paper/2025/hash/5a0e51901cff2b42d379ec7869603e91-Abstract-Conference.html)
- [liao2025beyondmimic](https://arxiv.org/abs/2508.08241)
- [li2026roboperform](https://openaccess.thecvf.com/content/CVPR2026/papers/Li_Do_You_Have_Freestyle_Expressive_Humanoid_Locomotion_via_Audio_Control_CVPR_2026_paper.pdf)
- [gdmlyria2025live](https://arxiv.org/abs/2508.04651)
- [luo2026sonic](https://arxiv.org/abs/2511.07820)
- [zhou2019rotation](https://openaccess.thecvf.com/content_CVPR_2019/papers/Zhou_On_the_Continuity_of_Rotation_Representations_in_Neural_Networks_CVPR_2019_paper.pdf)
- [ho2020ddpm](https://proceedings.neurips.cc/paper/2020/hash/4c5bcfec8584af0d967f1ab10179ca4b-Abstract.html)

## Corrections

- RTC: NeurIPS 2025 conference record, replacing preprint-only metadata.
- KungfuBot: NeurIPS 2025 conference record and year, replacing the 2026 preprint designation. Existing citation key retained for compatibility.
- SONIC: Science Robotics 11(117), eaed4592 (2026), DOI and complete author list.
- Diffusion Policy: removed Russ Tedrake, absent from the RSS 2023 author list.
- MLD checked against CVPR version: its existing seven-author record is correct; arXiv has a different author list.
- Magenta RealTime 2 recorded as a technical web resource; FiLM retains volume without an incompatible inproceedings issue number.

The additions provide literature context, not claims of experimentally beating those systems. CoF versus TF remains the approved comparison.

## Merged bibliography and author display (2026-09-10)

Compared the supplied 51-entry BibTeX list with the current 53-entry library using a BibTeX parser. Every supplied key was already present. The current-only entries, `zhou2019rotation` and `ho2020ddpm`, are both used in the method and are retained. There are no duplicate keys, normalized titles, DOI fields, or URL fields. The compiled manuscript cites 38 literature entries, with no unresolved citation keys; uncited literature remains in the library without forced inclusion in the manuscript.

### Reconciliation decisions

- Keep RTC and KungfuBot as NeurIPS 2025 proceedings papers, and SONIC as Science Robotics 11(117), eaed4592 (2026), rather than reverting to the supplied preprint records. Their primary sources are linked above. Preserve all citation keys, including keys whose embedded year predates or differs from the publication year.
- Keep MRT2 as a web resource (`@misc`), match the official title's ampersand, and identify the source as the Magenta blog rather than assigning a formal technical-report status. [Official release and suggested citation](https://magenta.withgoogle.com/magenta-realtime-2).
- Keep FiLM as a proceedings paper with volume 32; do not merge issue 1 into an `@inproceedings` entry that already has a volume, which this IEEEtran style rejects. Add the verified DOI and publisher URL. [AAAI record](https://ojs.aaai.org/index.php/AAAI/article/view/11671).
- Update MERT from arXiv 2023 to ICLR 2024, retaining its complete 20-author list and citation key. [ICLR record](https://proceedings.iclr.cc/paper_files/paper/2024/hash/33dffa2e3d2ab74a783d1a8c292f66d9-Abstract-Conference.html).
- Update MusicGen to NeurIPS 2023, volume 36, pp. 47704--47720, with its proceedings DOI. [Official record](https://proceedings.neurips.cc/paper_files/paper/2023/hash/94b472a1842cd7c56dcb125fb2765fbd-Abstract-Conference.html) and [BibTeX export](https://proceedings.neurips.cc/paper_files/paper/22279-/bibtex).
- Update MusicFM to ICASSP 2024, pp. 1226--1230. Its three authors are unchanged. The [authors' repository](https://github.com/minzwon/musicfm) confirms the venue; [publisher-deposited Crossref metadata](https://api.crossref.org/works/10.1109/ICASSP48485.2024.10448314) supplies DOI, year, authors, and pages.
- Update CLAP to ICASSP 2023, pp. 1--5, using the six-author published version. The preprint lists an additional author, Marianna Nezhurina; that list must not be mixed with the conference metadata. This is a publication-version correction, not author truncation. [Institutional publication record](https://cris.bgu.ac.il/en/publications/large-scale-contrastive-language-audio-pretraining-with-feature-f-2/) and [publisher-deposited metadata](https://api.crossref.org/works/10.1109/ICASSP49357.2023.10095969).
- Update MuLan to ISMIR 2022, pp. 559--566, preserving all six authors. [Conference paper](https://archives.ismir.net/ismir2022/paper/000067.pdf).
- Record MAP-Music2Vec as an ISMIR 2022 late-breaking/demo extended abstract, not a main-track paper. The venue name explicitly preserves that distinction; all 14 authors are retained. [Conference archive](https://archives.ismir.net/ismir2022/latebreaking/000049.pdf).
- Complete SoulNet's ICCV 2025 pages (14420--14430) and use its conference URL. [CVF record](https://openaccess.thecvf.com/content/ICCV2025/html/Li_Music-Aligned_Holistic_3D_Dance_Generation_via_Hierarchical_Motion_Modeling_ICCV_2025_paper.html).
- Complete the rotation paper's CVPR 2019 pages (5745--5753). [CVF record](https://openaccess.thecvf.com/content_CVPR_2019/html/Zhou_On_the_Continuity_of_Rotation_Representations_in_Neural_Networks_CVPR_2019_paper.html).
- Complete DDPM's NeurIPS 2020 pages (6840--6851) and Diffusion Forcing's NeurIPS 2024 pages (24081--24125), following the official exports. [DDPM BibTeX](https://proceedings.neurips.cc/paper_files/paper/10298-/bibtex), [Diffusion Forcing BibTeX](https://proceedings.neurips.cc/paper_files/paper/25298-/bibtex).
- Add the official VQ-VAE proceedings link. Its [official BibTeX](https://proceedings.neurips.cc/paper_files/paper/2017/file/7a98af17e63a0ac09ce2e96d03992fbc-Bibtex.bib) supplies no page range, so none is guessed.

The merge and citation-coverage checks cover the entire supplied/current library. External verification in this pass targets conflicting versions and the missing/outdated fields listed above; it is not a claim that every unchanged field in all 53 works was independently verified. Unconfirmed publication changes and missing optional metadata are left untouched.

### Author-list policy

Full author lists remain in `Reference.bib` for the selected publication versions. The official, unmodified `IEEEtran.bst` is controlled through `ForeDance:BSTcontrol`: forced et al. enabled, maximum displayed author count 3, first 3 names shown, repeated-name dashes disabled. `main.tex` activates the control before its first citation. Works with at most three authors display all authors. The control entry does not print or consume a reference number. This setting implements the requested manuscript display; it is not asserted to be a mandatory RA-L author-truncation rule.

### Build checks

- The main manuscript compiles with 38 references and no undefined citations or BibTeX warnings.
- A separate ignored-build-directory smoke document compiles all 53 works. Checks of both generated `.bbl` files confirm three displayed authors plus et al. for longer lists, no truncation for at most three authors, and no numbered control entry.
- `3D`, `Python`, and `librosa` are case-protected in titles so sentence-case bibliography formatting does not corrupt these names.
- No scientific prose, result values, or citation keys are changed by this bibliography pass. The reading PDF is regenerated; the official class and bibliography style remain unchanged.
