# Anticipatory music conditioning: positioning review

Reviewed 2026-09-11 against freshly fetched origin/main, 956ad67. Local main matched this revision before editing. Reviewed the active abstract, introduction, related work, method, experiments and discussion. No numerical result, figure, or experiment contract was changed.

## Accepted positioning

MRT-2 is used as a frozen, general-purpose generative music foundation model. Its music continuation prior is pretrained outside our paired dance training, while the dance generator learns how to map its forecast states into motion. This provides access to a music prior learned beyond the paired dance corpus. It does not establish superior generalization, lower required dance-data volume, or superior motion quality without a matched experiment.

The introduction now states: “To our knowledge, ForeDance is the first streaming dance generation framework to explicitly condition motion on future music states forecast by a pretrained music foundation model using past and present audio alone.” This is a scoped literature-based novelty assessment, not an exhaustive proof of priority. It does not claim the first online dance system, first beat prediction for dance, or first use of foundation-model features in dance. D+C with paired reconstruction objectives and Commit Forcing remain the other principal contributions.

## Primary-source checks

- [MRT-2 official technical description](https://magenta.withgoogle.com/magenta-realtime-2), published June 4, 2026, technical appendix: autoregressive codec model with causal sliding-window attention, 25 Hz frames, and around 71,000 hours of mostly instrumental stock music with inferred MIDI labels. These support the pretrained musical-prior description. Do not infer that this music corpus is disjoint from our held-out songs; corpus overlap is not established.
- [DiscoForcing v1](https://arxiv.org/html/2605.28491v1), Sections 3.1 and 4.1: causal VQ-PAE features from a sliding observed-audio window; FineDance and AIST++ paired benchmarks. The paper supports the task-specific encoder versus explicit future-state forecast distinction. Its encoder-specific pretraining corpus and initialization are not sufficiently documented to claim it categorically has no external pretraining. The manuscript therefore does not assert that DiscoForcing's encoder was trained exclusively from scratch on paired dance data.
- [DGFM](https://arxiv.org/abs/2502.20176), abstract, corroborated by the [author publication page](https://dipteshkanojia.co.uk/publication/liu-etal-2025-dgfm/): combines pretrained foundation-model features and acoustic features for dance. Added as prior foundation-model use; cited as the verified arXiv version.
- [Nakahara et al., ICEC 2009](https://ist.ksc.kwansei.ac.jp/~nagata/data/2009_nakahara_ICEC2009.pdf), Section 3.2: predicts inter-beat intervals and next beat time for robot dance. Added to distinguish our generative music-state forecasts from earlier beat anticipation.
- EDGE's Jukebox conditioning is already covered by existing citations and explicitly acknowledged in the revised related work.

Searches included “dance generation future music prediction”, “dance generation anticipatory conditioning”, “streaming dance forecast”, “dance generation music prediction”, “robot dance predicting future music”, and “DiscoForcing pretrain”. No directly matching foundation-model future-state conditioning mechanism was found among the inspected sources. The broad unqualified claim “first anticipatory dance generation” is not supported by these checks.

## Current manuscript findings

The accepted 198-trajectory correspondence result is unchanged. The forecast-versus-heard comparison, D+C comparison and CoF-versus-TF comparison remain explicitly pending. Correspondence scores cannot establish comparative forecast benefits. Generalization from broader music pretraining is a motivation and a testable hypothesis, not an accepted result. These limits are preserved in Discussion without displacing the main method narrative.

The existing draft also contains planned perceptual, timing-intervention and runtime protocols, and an IEEE/RA-L layout inherited from recent upstream revisions. These were outside this positioning edit and were not treated as newly approved experiments or a new venue decision.
