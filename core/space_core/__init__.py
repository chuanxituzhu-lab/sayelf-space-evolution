"""Platform-independent Space Core v0.1.

The package is intentionally stdlib-only. It owns canonical data, input
adapters, continuity locks, and the local Native Provider; media and CAD/BIM
providers remain optional integrations.
"""

from .canonical import (
    CanonicalSpaceModel,
    LOCK_NAMES,
    SCHEMA_VERSION,
    STAGES,
    ValidationIssue,
    ValidationReport,
)
from .intake import DrawingIntake, SketchIntake, suggest_input_kind
from .locks import SpatialEngineeringLock
from .providers import ExecutionResult, NativeProvider, ProviderContract
from .workflow import build_prompts

__all__ = [
    "CanonicalSpaceModel",
    "DrawingIntake",
    "ExecutionResult",
    "LOCK_NAMES",
    "NativeProvider",
    "ProviderContract",
    "SCHEMA_VERSION",
    "SketchIntake",
    "SpatialEngineeringLock",
    "STAGES",
    "ValidationIssue",
    "ValidationReport",
    "build_prompts",
    "suggest_input_kind",
]
