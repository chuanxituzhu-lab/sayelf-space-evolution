# Sayelf Space Evolution v1.0

> 变的是完成度，不变的是空间。

一个本地优先的「手绘稿 → 线 → 线稿 → 草图 → 线落成墙 → 空间生成 → 视频分镜」工作台。

## 适合谁
- 建筑/室内设计师
- AI 视觉创作者
- 自媒体空间内容创作者
- 希望把手绘构想转成连续空间演化作品的人

## 你会得到什么
- 本地 WebUI 工作台
- 手绘稿录入口
- Spatial Continuity Lock（空间一致性锁）
- 五份独立空间 Prompt + 一份视频 Prompt 生成器
- 每份 Prompt 可单独复制，支持交给任意 AI 辅助图像/视频平台
- 10/15/20 秒视频分镜 Prompt 生成器
- 项目 JSON / Markdown 导出
- 可被 AI 辅助平台读取的 Skill 文件
- Agent 执行规范、插件接口规范、示例与验收规则

## Windows 安装
1. 解压整个 ZIP 到任意文件夹。
2. 确认电脑安装 Python 3.10+。
3. 双击 `start_windows.bat`。
4. 浏览器会自动打开 `http://127.0.0.1:8765/`。

> 不需要 `pip install`，v1.0 仅使用 Python 标准库。

## macOS / Linux
```bash
chmod +x start_mac_linux.sh
./start_mac_linux.sh
```

## 最短使用流程
1. 上传手绘稿。
2. 在「预存试用场景」中选择一个场景并点击「套用场景」，或直接写自己的空间描述。
3. 根据自己的想法修改项目名称、空间描述和视觉方向。
4. 保持默认 5 项 Spatial Continuity Lock。
5. 点击「生成完整工作流」，在下方 6 张独立 Prompt 卡片中逐份复制提示词。
6. 按 01 → 02 → 03 → 04 → 05 顺序，把空间 Prompt 和上一阶段图片交给 AI 图像平台；再把 06 视频 Prompt 交给文生视频或图生视频平台。
7. 视频阶段优先用阶段 05 成图作为首帧。

## v1.0 边界
本版本是可本地运行的商业工作流版，负责：输入、空间一致性规则、独立 Prompt/分镜编排、复制、项目保存与导出。

**它不内置第三方图像/视频模型，也不会偷偷调用任何付费 API。** 如果要一键生成图片/视频，需要用户自行接入有权限的生成 Provider；相关扩展位已经保留在 `plugins/`。

## 核心差异
普通工作流通常是：`Sketch → Render`。

本产品是：
`Line → Linework → Sketch → Line Becomes Wall → Space Generation → Film`

空间不是每一步重新设计，而是沿同一 Spatial DNA 连续生长。

## 文件说明
- `webui/`：本地交互工作台
- `skill/`：可供 AI 辅助平台读取的专业 Skill
- `agent/`：自动执行层规范
- `core/`：Spatial DNA 与连续性规则
- `plugins/`：AI 平台与生成 Provider 插件接口
- `interfaces/`：MCP / CLI / API 方向说明
- `examples/`：演示案例
- `docs/`：安装、销售交付、故障排查
- `tests/`：验收规则

## 购买者许可
请阅读 `COMMERCIAL_LICENSE.txt`。本包默认授权购买者在约定范围内使用，不授权转售、二次打包或公开分发本产品本身。
