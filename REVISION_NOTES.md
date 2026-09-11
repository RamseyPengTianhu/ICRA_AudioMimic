# ForeDance 更新记录 — 2026-09-09

已按确认方案完成研究初稿更新，标题暂用 **ForeDance: Structured Streaming Dance Generation with Anticipatory Music Conditioning**，采用不绑定会场的双栏排版。

正文围绕音乐预判条件、D+C 及配套训练、Commit Forcing 三项贡献展开。仅使用 FineDance；FHC 和 MMR 保持辅助地位。原稿及本地修改已备份，没有启动新训练或向远端发布。

## 图片

四张示意图使用内置 imagegen。当前接口不提供型号选择，因此无法确认用户要求的 Image 2.5。所有实际使用图片及原始提示词已保存在论文目录。

- 任务图：因果音乐预测、计划前缀提交和后续重规划。
- 总架构图：音乐条件进入两个生成分支；结构与细节分别汇入共同解码器；已提交参考动作更新历史与边界状态。
- D+C 图：按实际代码分别展示关节视图和几何点视图。关节视图的结构部分是根部、双腿、腰部，细节是双臂；几何视图的结构部分是躯干、双腕、双脚底，细节是其他身体点。仅画完整重建与仅结构重建，corrupted detail 只在正文说明。
- CoF 图：与 TF 对比如何形成下一步的训练上下文；不混淆动作代码与边界状态。
- 长序列图：从已校验的当前模型 60 秒原始视频提取 10、30、50 秒真实帧。它是单例展示，未冒充 TF 对照或机器人执行证据。

最终 D+C 图为 `figures/foredance/dc-bodyparts.png`。其他最终图片清单和校验值见 `evidence/foredance/figure-assets.json`；完整提示词见同目录的 `image-prompts.json` 和 `image-revisions.json`。

## 证据与检查

数值从原始汇总文件生成，核对了有音乐和无音乐对照的差值。已有数字仍属于完整 18 首歌曲的现有评估；没有擅自改变筛选范围，也没有把旧表示的数字搬来填新对照。

PDF 已成功编译，逐页检查了 11 页的文字、五张图、表格、公式和引用。没有内容越界、缺失字符或未解析引用；常规行间留白提示不影响阅读。检查输出保留在 `build/qa/`。

尚缺的音乐预判核心对照、当前 D+C 对照、TF 对照和执行案例集中列在 `TODO.md`。这是可以继续打磨的研究初稿，不能据此宣称这些尚缺的比较已经获得优势。


## 正文叙事重写 — 2026-09-09 后续

根据用户“论文内容要更新，符合论文叙事方式”的要求，进一步重写摘要、引言、相关工作、方法解释、实验分析、讨论、结论及补充材料。主线改为：流式舞蹈需要预判未到达的音乐；预测条件通过有明确运动学训练目标的 D+C 模型变成动作计划；CoF 让模型学习从自己已提交的动作继续。

- 摘要与引言突出问题、设计动机和已有证据，不再以审核状态开场。
- 方法解释结构、细节和提交训练为什么需要一起设计，保留代码对应的公式与身体部位定义。
- 实验明确区分已经完成的音乐条件及 FHC 对照，与尚待完成的预测/已听音乐、表示替代方案、TF/CoF 对照。未把对照设计写成已取得的实验结论。
- 正文移除“绑定结果”“补齐 receipts”“不得挪用旧表”等作者指令，以及补充材料里的任务清单。原内容保存在 evidence/foredance/author-evidence-notes.md 和 prior-evaluation-planning.tex。
- 讨论集中交代结果适用范围；未改变数值、筛选规则或此前批准的实验安排。
- 补充材料现在提供训练、部位划分、边界损失和成对评估的可复现说明。

本轮修改前版本另存为 ../paper-backups/pre-narrative-rewrite-20260909-212523.tar.gz。

后续重写版本已重新编译并逐页检查，共 11 页；无越界、缺字、未解析引用。数值来源校验保持一致，最终检查记录位于 build/qa-narrative/。


## 综合主图与机器人元素

按用户确认的未来乐谱方向，将任务图与架构图合并为一张 ForeDance 全宽主图。音乐时间线、结构与细节的生成、共享解码与前缀提交构成主流程；下方保留 D+C 身体监督视图与 Commit Forcing 训练摘要。机器人连续舞姿为示意，真实实验帧保持独立。论文同步更新图注、引用，主图总数由五张变为四张。完整提示词见 evidence/foredance/overview-prompt.json。

最终综合主图版本已编译并检查：11 页，四张主图，主图位于第 2 页。无越界、缺失字符或未解析引用；所有页面已重新渲染，检查记录在 build/qa-overview/。生成模式为内置 imagegen；未宣称已选择 sunburst 最高档。


## References completion

Reconciled the bibliography with active Related Work: 15 previously uncited entries now have explanatory citations, and two foundational method references were added for six-dimensional rotations and denoising diffusion. There are 39 cited bibliography entries. Updated RTC and KungfuBot to NeurIPS 2025 records, SONIC to its journal record, and corrected the RSS Diffusion Policy author list. Primary-source audit and coverage record are in evidence/foredance/REFERENCE_AUDIT.md and reference-coverage.json. Long reference URLs use flexible line breaking.

Final validation: 12 pages, 39 rendered references, no missing citations, bibliography warnings, missing glyphs, or overfull lines. Rendered pages are retained in build/qa-references/.


## Teammate execution integration — 2026-09-10

Merged latest Overleaf revision d12a5c0 into the current ForeDance paper. Generation method, title, narrative and active main figures follow the current local draft. Retained the incoming bibliography additions, architecture asset (inactive), and deletion of obsolete V1.tex. Adapted the teammate execution interface to current absolute pelvis orientation instead of old yaw-increment accumulation. Added a method interface subsection, a separately scoped execution subsection, and supplementary reference-delivery/measurement definitions with the previously reported four-row MuJoCo table. The old table is explicitly an earlier 34D configuration, not current ForeDance or live music execution. Removed no evidence limits; the current paired execution case remains pending. The newer teammate revision had removed the experiment block, so no old table was restored as a current-model main result.

Numeric transcription is checked against the archived source table with a source hash. Original controller logs were not recomputed. All-current-cohort statements now apply specifically to generator results. Main overview image is unchanged. No new experiment, blind evaluation, runtime study or hardware claim was introduced. User authorized GitHub publication after successful checks.

Final checks: 14-page PDF rendered and visually reviewed, 39 cited references, no overfull lines, missing glyphs or unresolved references. Current generation table bytes and the overview image match the pre-merge version. Supplementary tracking rows match the archived teammate table exactly. ForeDance.pdf is the checked reading copy for GitHub.

## Teammate figures retained (2026-09-10)

The main paper now includes an execution-interface diagram adapted from the teammate editable architecture, and the supplement includes their corrected Commit Forcing training diagram unchanged. The ForeDance overview remains the main figure. Historical 34D raster diagrams and codec results are not relabeled as current evidence.

## 2026-09-11: anticipatory foundation-model positioning

Revised the abstract, introduction, related work, anticipation method passage and discussion to identify MRT-2's general music pretraining and its role as a frozen future-state predictor. Added a qualified first claim scoped to foundation-model forecasts conditioning causal streaming dance. Added DGFM and early robot tempo prediction references so the novelty excludes prior feature reuse and beat anticipation. Kept the accepted numerical results and all figures unchanged. Full source checks are in `evidence/foredance/ANTICIPATION_POSITIONING_REVIEW.md`.

Moved T1 encoding initialization ahead of the IEEE class to avoid class-time font substitution under Tectonic. Restored missing local Times math-font resources. Rebuilt the full PDF, checked active citations, and inspected the edited pages and bibliography. The current complete working draft is 14 pages; pending comparison studies and inherited venue formatting remain to be reconciled before submission. Current validation is `evidence/foredance/anticipation-positioning-validation.json`; earlier validation files describe their historical revisions.

## 2026-09-11: contribution hierarchy and main-text execution

Reorganized the paper around musical anticipation, structured generation and committed-prefix continuation. Moved detailed state/coordinate definitions, optimization and evaluator settings to the supplement. Retained every previously active citation and all accepted result values. The main overview appears on page 2; the execution interface and teammate diagram remain in the main text as requested. Supporting replay findings remain explicitly historical MuJoCo evidence. Empty comparison tables and inherited unapproved study plans have been removed from the reader-facing manuscript; the missing matched comparisons are stated once in Discussion.

The rebuilt working manuscript has 11 pages, with main text and conclusion on pages 1–6. The two method detail figures remain separate for readability, and the original raster artwork and vector overview are unchanged. Current checks are recorded in `evidence/foredance/narrative-revision/validation.json`.


## 2026-09-11: terminology and imagegen-first overview review

Replaced reader-facing prefix terminology by contextual committed-motion wording and renamed the representation Structure–Detail Representation. Updated prose, captions, table display names, active overview labels and method diagrams. The two accepted initialization rows retain their original experiment identities and all numerical values. Existing teammate execution material remains.

Following author review, simplified vector robots were rejected. The overview was generated again with imagegen, preserving detailed robot artwork, MRT-2 icon and four panels. Forecast states differ visually; FiLM labels belong to music-conditioning arrows, with separate history/state inputs. Explanatory labels omit parentheses and FMS14. The final raster master is retained alongside a contour-converted SVG/PDF at unchanged layout coordinates; robots and icon remain raster artwork, and lettering is outlined rather than live text. The review PDF uses this candidate, while the active manuscript retains its existing overview layout with corrected terminology.

No merge or push was performed during this revision. Remote main was rechecked as 0e36903, and Overleaf conflict branch as 18386fa. Existing local merge history remains an unpublished draft and requires author review before publication.


## 2026-09-11: publish the reviewed editable overview

The author requested GitHub publication after the final figure review. The active overview is the faithful four-panel reconstruction with editable text and geometry, the author-supplied outlined wordmark, and the accepted transparent robot assets. Subsequent requested refinements include source-verified structure-to-detail embedding/addition, matching commit/discard diagrams, purple history context, explicit compute/append paths, trainable flames, natural-proportion Helvetica lettering, and boundary icons without arrows with matching dividers in b and d. Earlier candidate and publication-hold notes above are historical.

The reading copy is the actual 11-page manuscript build. The final icon/divider edit changed only page 2, and other pages match the previous reviewed revision. The publication includes active source dependencies, accepted reference artwork, source assets and current checks; temporary build work and rejected figure candidates stay local.


## 2026-09-11: concise abstract and complementary motion-quality results

Following the author's approval of the GitHub/HF audit, shortened the abstract to a contribution-led statement with one numerical soundtrack-correspondence sentence. Moved detailed scoring information to the experiment protocol and full statistics to the appendix. Promoted the completed 18-track motion-quality table to the main text and included the already archived history-dropout control, preserving the distribution/smoothness tradeoff. The 23-second motion-quality study and 60-second correspondence study remain separate. The additional archived controls and longer generated motions are documented in TODO.md for later results; no pending outcome is inserted into a result cell.

Reproduced all 198 accepted correspondence records, 18 score matrices, reported means and intervals; checked all 25 displayed motion-quality values against the archived summary. The existing full correspondence table, figures and bibliography are unchanged. Recompiled and rendered the complete 12-page working draft; the compact correspondence table is on page 5, motion-quality table on page 6, full correspondence statistics on page 10. Main text ends on page 7. No overfull boxes, missing glyphs or unresolved references/citations. Underfull spacing warnings remain. The current reading copy is ForeDance.pdf; validation is recorded in evidence/foredance/abstract-results-revision-validation.json.


## 2026-09-11: evaluator validation, generator alignment and explicit ablation TODOs

Separated reference-motion evaluator validation (68.41% ordinary and 64.08% similar-alternative discrimination) from scoring generated dance. The generator music table now reports one complete initialization result per metric: 75.01% correspondence on 99 sixty-second motions and BAS 0.4419 on the separate 18-track, 23-second cohort. Direct/startup labels are removed from result comparisons. Complete alternatives remain archived; one Discussion note describes post-hoc metric-specific initialization selection and descriptive uncertainty. The matched history table keeps a single initialization, three actual history-training controls, and adds BAS with four decimal places. Its raw five-route archive remains unchanged.

Added four visible working-draft TODOs for anticipation, paired representation training, independent discrete/continuous controls and Commit Forcing versus Teacher Forcing; synchronized TODO.md. Verified accepted score matrices and intervals, calibration-table transcription, BAS aggregation/source identity and all 18 history-table cells. Rebuilt and visually reviewed the 12-page PDF with no overfull boxes, missing glyphs or unresolved citations/references. Current validation: evidence/foredance/music-evaluation-revision-validation.json. No new experiment or rescore was launched.
