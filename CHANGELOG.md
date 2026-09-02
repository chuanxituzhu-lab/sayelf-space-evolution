# Changelog

## Unreleased — Space Core v0.1
- 从现有 Space Skill 抽取平台无关的 Canonical Space Model、双入口、Spatial Engineering Lock 与零插件 Native Provider。
- 新增 `core/schemas/canonical-space.schema.json`、Core Python API、Provider 合同、脱敏展厅 PoC fixture 与 8 项标准库回归测试。
- 保持原有 v1.0 WebUI、六阶段 Prompt 工作流和五锁命名兼容；本轮不接入第三方 Provider、不修改 UI。
- 公开仓库定位为 MIT Core；商业 Pro、专业适配器、客户资产和交付材料移出公开分支，另行私有化。

## 1.0.0
- 优化客户关联与视角冲击：01 只保留大框架并呈现笔划过纸，02 建立主骨架，03 保持原有草图风格
- 新增「保存项目」本地落盘：默认写入应用目录 `exports/space-evolution-project.json`，并在 WebUI 显示实际路径，服务不可用时回退下载
- 新增空间描述优先自动匹配：本地识别项目名称、空间类型和空间风格，支持手动覆盖，不识别时保留默认项
- 新增自媒体画幅原则：9:16 或 4:5 保持单张独立画幅，5 张或 N 张图片统一高度横向排列，不拼接、不裁切、不拉伸
- 明确材质与完成度按场景、建筑空间和视觉风格匹配，不默认清水混凝土，支持豪华、极简、自然、商业等方向
- README 新增产品定位、客户价值与 01—05 阶段示例图展示
- 新增空间风格选择：现代极简、美式、法式、侘寂、简中、中式、自然原木、现代商业等
- 新增空间类型选择：现代商业、展厅、体育馆、办公空间、酒店大堂、文化中心，可与空间风格自由组合
- 预存 5 个不同空间场景，支持客户一键套用后继续改写空间创意
- AI 辅助平台预览模式：一次生成 5 份独立空间 Prompt 与 1 份视频 Prompt，支持逐份复制
- WebUI 视觉系统优化：清晰阶段导航、输入/输出层级、响应式布局与本地反馈
- 本地 WebUI 可运行
- 手绘稿/参考图录入
- Spatial Continuity Lock
- 线、线稿、草图、线落成墙、空间生成、视频六阶段提示词
- 10/15/20 秒分镜
- 本地保存
- JSON/Markdown 导出
- Skill / Agent / Plugin / Interface 规范
