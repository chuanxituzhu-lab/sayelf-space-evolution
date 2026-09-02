# Plugin Contract

Core must not depend on a specific AI platform or generation model.

Space Core v0.1 的最小 Python 合同、Native Provider 和外传边界见
[`PROVIDER_CONTRACT_V0_1.md`](PROVIDER_CONTRACT_V0_1.md)。没有插件时，`native.local`
仍提供模型校验、执行计划和六阶段 Prompt 编排。

## Plugin categories
- ai_platform_adapter
- image_provider
- video_provider
- continuity_validator
- export_provider
- cad_provider (future)
- bim_provider (future)

## Discovery preference
`MCP → CLI → HTTP/API/SDK → Local Socket → platform-specific connector`

## Minimal manifest
```yaml
id: example-provider
type: image_provider
version: 1.0.0
capabilities:
  - text_to_image
  - image_to_image
interfaces:
  - api
requires_auth: true
```

Provider integration is optional. The local workflow must continue to function without any optional provider.
