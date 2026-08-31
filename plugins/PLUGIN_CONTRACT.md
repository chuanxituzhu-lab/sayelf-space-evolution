# Plugin Contract

Core must not depend on a specific AI platform or generation model.

## Plugin categories
- ai_platform_adapter
- image_provider
- video_provider
- continuity_validator
- export_provider

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

Provider integration is optional in v1.0. The local workflow must continue to function without any provider.
