# Space Core v0.1 Build Decision Record

## Idea / real task

在不解冻 Space Evolution v1.0 的六阶段空间演化边界的前提下，把现有 Skill 中可复用的空间输入、Spatial DNA 与连续性规则抽取成一个可独立验证的 Canonical Space Core。它必须在没有任何专业软件插件和第三方 Provider 时仍能完成本地建模、锁校验和 PoC 流程。

## Closest existing projects or capabilities

- 本仓库 `skill/SKILL.md`：已有六阶段工作流、Spatial DNA 五锁、输入匹配、本地优先和资产契约。
- 本仓库 `webui/index.html`：已有本地关键词匹配、五个锁选项、六份 Prompt、项目保存与导出；其内嵌逻辑是可迁移的行为参考，不作为 Core 依赖。
- 本仓库 `core/spatial-dna.schema.json` 与 `core/continuity-rules.yaml`：已有锁字段和规则，但不足以表示入口、观测证据、构件、资产依赖与锁状态。
- [IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell) / [官方几何处理文档](https://docs.ifcopenshell.org/ifcopenshell-python/geometry_processing.html)：作为未来 IFC Provider 的成熟参考；本切片不强制安装或依赖它。
- Blueprint3D 类开源 floor-planner：证明浏览器端三维平面编辑存在可复用方向，但不满足本项目的空间连续性与本地工程锁边界，因此不引入。

## Step 0 decision: Improve

复用现有 Space Skill，补齐最小 Core 接口与证据链，而不是重写 WebUI 或引入新的建模框架。

## Measurable improvement or differentiator

- 零第三方依赖下，Drawing Intake 与 Sketch Intake 都能产出同一份 Canonical Space Model。
- Canonical Model 具备可校验 schema、输入证据等级、五类 Spatial Engineering Lock 与下游 stale 状态。
- Native Provider 在无插件状态下可稳定完成 `validate → plan`；Provider 仅替换执行能力，不改变模型或锁规则。
- 通过 `unittest` 验证：双入口、默认五锁、几何变更使下游资产 stale、未锁模型阻止执行、零 Provider 仍可运行。

## Success measure and required evidence

成功条件是 `python -m unittest discover -s tests -v` 在零第三方依赖下通过，并且 PoC 能从两个入口进入同一 Canonical Model，运行最小验证，产出可审计的执行计划。证据包括：schema、合同、实现、fixture、测试结果与迁移清单。

## Minimum Core

- Canonical Space Schema v0.1：项目、输入、空间、几何/开口/锚点、证据、资产、锁状态。
- Drawing Intake：明确的平面图/立面图/剖面图入口；自动识别仅产生辅助建议，不决定入口。
- Sketch Intake：明确的草稿/线稿/概念草图入口；未知尺度保持为推断，不冒充工程事实。
- Spatial Engineering Lock：camera、perspective、geometry、openings、anchors 五锁；状态化验证和下游 stale 传播。
- Native Provider：本地无插件 Provider，支持验证与执行计划，不生成虚假的专业软件文件。
- Provider/Adapter Contract：最小 manifest、能力查询、可执行性检查与执行计划接口。

## Plugin boundaries (if any)

- `drawing_intake` / `sketch_intake`：输入适配边界。
- `native`：默认本地 Provider，永远可用。
- `image_provider` / `video_provider` / `cad_provider` / `bim_provider`：未来可插拔增强；不得拥有 Canonical Model 的真值或修改锁规则。

## Local-first boundary

确定性解析、关键词匹配、schema 校验、锁计算、stale 传播、Provider discovery 和执行计划全部本地运行。第三方模型、CAD/BIM 软件和媒体服务不在本切片内调用。

## Data classification and local trust boundary

本次准备公开的 Core 代码、Schema、文档、测试和脱敏 fixture 已分类为 `Public`；本地工作树、真实客户空间描述、草稿、图纸、项目 JSON、Prompt、日志均仍按 `Internal` 或 `Sensitive` 留在本机。凭据、API key、个人信息和客户原图不得进入 fixture、日志、远程仓库或公开发布物。

## GitHub/public release decision: Allowed — review evidence

用户已明确授权按 MIT Core / 私有 Pro 原则推送。当前功能分支的 staged diff 将只包含公开 Core、脱敏示例和边界文档；商业买方许可、销售资料和私有 Pro 内容已从当前分支移除。已完成测试、PoC、原 v1.0 health、凭据模式与临时路径审查；主分支不会被直接改写，先推送功能分支并通过 PR 审核。

## External transfer plan (if any; local and sensitive data excluded)

目标为已知的公开 GitHub remote `https://github.com/chuanxituzhu-lab/sayelf-space-evolution.git`。用户授权此次公开推送；只传输分类为 `Public` 的 Core 代码、文档、脱敏 fixture 和测试。GitHub 的公开可见、fork 和历史留存视为长期公开保留；不传输本地客户数据、商业 Pro、凭据或未知内容。

## State, change signals, and next-check rule

- `DRAFT`：模型可编辑，未满足执行前提。
- `LOCKED`：五锁均存在且模型验证通过。
- `STALE`：锁定字段或其输入证据发生变化，下游资产需要重新验证。
- `READY`：当前 Provider 能力覆盖且模型/锁/输入有效。
- `BLOCKED`：缺少必需锁、存在冲突、未知关键数据或 Provider 能力不足。

只在输入、锁、模型版本、Provider 能力或资产依赖发生变化时重新验证；稳定状态不轮询。高重要性的几何/开口变化立即触发 stale，普通描述变化只影响 Prompt/意图字段。

## Observation / inference / hypothesis / fact boundary

- `Observation`：入口文件/用户描述中直接得到的文字、尺寸、线段或图纸标注。
- `Inference`：由规则从 Observation 推导的空间类型、可能的构件或视角。
- `Hypothesis`：待用户确认的尺寸、消失点、材质或构件关系。
- `Fact`：用户确认、图纸明确标注、或通过确定性校验得到的值。

Core 不把 `Inference`/`Hypothesis` 自动提升为 `Fact`；没有工程证据的草稿数据保持不确定性。

## Evolution, validation, canary, version, and rollback plan

Schema 与合同版本固定为 `0.1.0`。先以两个本地 PoC fixture 做回归，再逐步加入更多已脱敏案例作为 canary；通过后才提升 schema/contract 版本。当前提交 `487af3d` 保留在功能分支，可回退到 `3787ccb` 基线；公开推送后通过 PR 合并，正式产品 tag 另行决定。本轮不修改原有 WebUI 运行路径。

## WebUI decision: Not required — reason

本轮真实任务是 Core 建模、契约和可验证工程骨架；现有 WebUI 已承担人机交互，重复建设会扩大冻结范围。后续若接入 Core，沿用现有 `Open → Input → Execute → Result` 路径，并隐藏高级锁/Provider 细节。

## Default WebUI path (if required)

N/A；复用现有 WebUI，不在本切片新增 UI。

## Simplest reliable implementation

Python 标准库 + JSON Schema 文件 + 明确的数据字典 + `unittest`。Core 先以纯数据和确定性规则实现；Native Provider 只生成本地执行计划，专业软件适配器以后按合同接入。

## Explicitly not building

- 自动判断并切换平面/立面/剖面/草稿入口。
- DWG/DXF/PDF/CAD/BIM 几何解析器。
- SketchUp、Blender、IFC 或云媒体服务的真实生成调用。
- 图像/视频模型、视觉识别模型、自动设计和自动改几何。
- 新 WebUI、远程 API、账号体系、遥测、同步和公共发布。
- 绕过 Spatial Engineering Lock 的快捷执行路径。
