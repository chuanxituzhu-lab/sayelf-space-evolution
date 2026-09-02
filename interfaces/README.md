# Interfaces

v1.0 ships a local WebUI as the primary interface.

Space Core v0.1 additionally exposes a local Python API under `core.space_core` for
deterministic intake, canonical modeling, lock validation and Native Provider planning.
This is an internal Core surface, not a new remote API.

Reserved integration directions:
- MCP: expose `create_project`, `build_prompts`, `validate_continuity`, `export_storyboard`
- CLI: expose the same deterministic local workflow for automation (future wrapper)
- API: local service endpoints for future provider/agent integration

The public repository is the MIT Core. It does not pretend to support a third-party platform unless that adapter has actually been installed and configured. Commercial Pro adapters and customer delivery modules remain outside this public repository.
