# Existing Space Skill Inventory and Migration Plan

盘点基线：`sayelf-space-evolution-repo`，当前 HEAD `3787ccb`，版本文件为 `1.0.0`。工作区盘点为只读，原仓库无未提交修改。

## Existing assets

| Asset | Current capability | Decision | Migration target |
|---|---|---|---|
| `skill/SKILL.md` | 六阶段 Line → Film、Spatial DNA 五锁、stage focus、资产契约、local-first、几何变更 stale 规则 | 保留并作为行为基线 | `core/spec/` 与 `core/workflow.py` 的规则测试；原 Skill 文件继续作为 Agent 执行规范 |
| `agent/AGENT.md` | 读取输入、生成六份 Prompt、顺序校验、保存本地项目、停止条件 | 保留 | 通过 Core 的 Intake/Lock/Provider 接口调用；不让 Agent 直接改几何 |
| `webui/index.html` | 本地表单、手绘稿预览、关键词匹配、六份独立 Prompt、复制/保存/导出 | 保留原行为；暂不重写 | 后续可用 Core facade 替换内嵌逻辑；本轮不改变 UI |
| `app.py` | Python 标准库静态服务、本地 JSON 保存、health endpoint | 保留 | 未来可增加 Core API，但本轮仅做 import-level compatibility 骨架，不新增远程能力 |
| `core/spatial-dna.schema.json` | 五锁名称与简单 notes | 抽取并扩展 | 升级为 `core/schemas/canonical-space.schema.json`；保留原文件兼容旧 Skill |
| `core/continuity-rules.yaml` | prime rule、严格锁、允许/禁止变化、stage/presentation 规则 | 保留 | 作为 `core/spec/continuity-rules.yaml` 的来源；以 Python 常量实现本轮最小确定性校验，避免引入 YAML 依赖 |
| `plugins/PLUGIN_CONTRACT.md` | Provider 分类、manifest、MCP → CLI → HTTP 偏好、无 Provider 仍可用 | 抽取并收紧 | `core/providers/contract.py` + `plugins/PROVIDER_CONTRACT_V0_1.md` |
| `interfaces/README.md` | 预留 MCP/CLI/API 方向 | 保留为路线说明 | 本轮只实现可被 CLI/测试调用的 Python API；不实现 MCP/API |
| `examples/demo-project.json` | 演示项目字段、展示、匹配、stage focus、锁 | 转为 fixture 来源 | 增加 `examples/space-core-poc.json`，保留原示例 |
| `tests/ACCEPTANCE.md` | 27 条 v1.0 UI/工作流验收项 | 保留 | 新增 Core 验收条目与 `unittest`；UI 验收仍按原文执行 |
| `docs/assets/workflow/*` | 五张公开演示图 | 保留 | 不复制进 Core，继续由原 README 引用 |
| `COMMERCIAL_LICENSE.txt`、`docs/SALES_DELIVERY_README.md`、`seller-kit/` | 旧商业交付与销售资料 | 从公开分支移除 | 保留在 git 历史/私有 Pro 交付材料中，不作为 MIT Core 内容 |

## Extracted Core objects

- `CanonicalSpaceModel`：版本化、可序列化的空间事实/推断/假设容器。
- `DrawingIntake`：只接受明确的 `plan`/`elevation`/`section` drawing kind。
- `SketchIntake`：只接受明确的 sketch kind；不进行自动入口切换。
- `SpatialEngineeringLock`：五锁状态与变更/stale 传播。
- `NativeProvider`：本地无插件默认 Provider；返回 capabilities、validation 和 execution plan。
- `ProviderContract`：最小 Provider 协议，禁止 Provider 直接拥有空间真值。

## Compatibility rules

1. 原有六阶段顺序不变：`line`, `linework`, `sketch`, `wall`, `space`, `film`。
2. 原有五锁命名不变：`camera`, `perspective`, `geometry`, `openings`, `anchors`。
3. 原有 `project`, `presentation`, `input_matching`, `stage_focus`, `client_association`, `continuity_locks`, `prompts` 字段继续可读。
4. 新 Core 字段放在独立 `space_core` 命名空间，不要求旧 WebUI 立即迁移。
5. 没有 Provider 时，Core 仍可建模、验证和导出执行计划；不会伪造渲染、CAD、BIM 或视频结果。

## Migration order

1. 建立 Canonical Space Schema v0.1 与版本校验。
2. 将双入口数据映射到 Canonical Model，自动识别只保留 suggestion。
3. 将五锁与变更传播从“布尔列表”升级为状态化 Lock。
4. 接入 Native Provider，验证零插件运行路径。
5. 用两个脱敏 PoC fixture 做回归；再考虑 WebUI facade。

## Deferred / no migration in v0.1

- 从图片/DWG/PDF 自动提取几何。
- 直接把前端 Prompt 模板搬入 Python Core。
- 任何第三方 Provider 的真实调用。
- 把草稿推断升格为工程事实。
- 改写原有 Skill、Agent、WebUI 的用户路径。
