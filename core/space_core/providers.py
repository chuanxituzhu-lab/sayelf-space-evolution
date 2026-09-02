from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol

from .canonical import CanonicalSpaceModel, ValidationIssue, ValidationReport


class ProviderContract(Protocol):
    """Minimal provider boundary; providers cannot own or redefine Canonical Space."""

    provider_id: str

    def manifest(self) -> dict[str, Any]: ...

    def can_execute(self, model: CanonicalSpaceModel, operation: str) -> ValidationReport: ...

    def execute(self, model: CanonicalSpaceModel, operation: str = "plan") -> "ExecutionResult": ...


@dataclass(frozen=True)
class ExecutionResult:
    ok: bool
    provider_id: str
    operation: str
    status: str
    external_calls: int = 0
    artifacts: tuple[dict[str, Any], ...] = ()
    payload: dict[str, Any] = field(default_factory=dict)
    errors: tuple[ValidationIssue, ...] = ()
    warnings: tuple[ValidationIssue, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "provider_id": self.provider_id,
            "operation": self.operation,
            "status": self.status,
            "external_calls": self.external_calls,
            "artifacts": list(self.artifacts),
            "payload": self.payload,
            "errors": [issue.as_dict() for issue in self.errors],
            "warnings": [issue.as_dict() for issue in self.warnings],
        }


class NativeProvider:
    """Always-available local provider for validation, planning and prompt assets."""

    provider_id = "native.local"
    supported_operations = ("validate", "plan", "build_prompts")

    def manifest(self) -> dict[str, Any]:
        return {
            "id": self.provider_id,
            "type": "native_provider",
            "version": "0.1.0",
            "capabilities": ["canonical_model", "validate", "execution_plan", "build_prompts"],
            "interfaces": ["python", "cli-compatible"],
            "requires_auth": False,
            "external_calls": False,
        }

    def can_execute(self, model: CanonicalSpaceModel, operation: str) -> ValidationReport:
        errors: list[ValidationIssue] = []
        if operation not in self.supported_operations:
            errors.append(ValidationIssue("unsupported_operation", "operation", f"Native Provider does not support {operation}."))
        report = model.validate()
        return ValidationReport(tuple(errors) + report.errors, report.warnings)

    def execute(self, model: CanonicalSpaceModel, operation: str = "plan") -> ExecutionResult:
        report = self.can_execute(model, operation)
        if not report.ok:
            model.data["space_core"]["state"] = "BLOCKED"
            return ExecutionResult(
                ok=False,
                provider_id=self.provider_id,
                operation=operation,
                status="blocked",
                errors=report.errors,
                warnings=report.warnings,
            )

        if operation == "validate":
            return ExecutionResult(
                ok=True,
                provider_id=self.provider_id,
                operation=operation,
                status="validated",
                payload=report.as_dict(),
                warnings=report.warnings,
            )

        if operation == "build_prompts":
            from .workflow import build_prompts

            prompts = build_prompts(model, provider_id=self.provider_id)
            return ExecutionResult(
                ok=True,
                provider_id=self.provider_id,
                operation=operation,
                status="ready",
                artifacts=tuple({"type": "prompt", "stage": stage} for stage in prompts),
                payload={"stages": prompts},
                warnings=report.warnings,
            )

        return ExecutionResult(
            ok=True,
            provider_id=self.provider_id,
            operation=operation,
            status="planned",
            artifacts=({"type": "canonical_space_execution_plan", "external": False},),
            payload={
                "steps": [
                    {"id": "validate_canonical_model", "status": "passed"},
                    {"id": "preserve_spatial_engineering_lock", "status": "required"},
                    {"id": "await_optional_provider", "status": "not_required"},
                ],
            },
            warnings=report.warnings,
        )
