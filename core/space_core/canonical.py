from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping, Sequence
from uuid import uuid4

SCHEMA_VERSION = "0.1.0"
STAGES = ("line", "linework", "sketch", "wall", "space", "film")
LOCK_NAMES = ("camera", "perspective", "geometry", "openings", "anchors")
DRAWING_KINDS = ("plan", "elevation", "section")
SKETCH_KINDS = ("rough_sketch", "linework", "concept_sketch", "perspective_sketch")
MODEL_STATES = ("DRAFT", "LOCKED", "STALE", "READY", "BLOCKED")
EVIDENCE_KINDS = ("observation", "inference", "hypothesis", "fact")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fingerprint(value: Any) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _copy(value: Any) -> Any:
    return copy.deepcopy(value)


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    path: str
    message: str
    severity: str = "error"

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path, "message": self.message, "severity": self.severity}


@dataclass(frozen=True)
class ValidationReport:
    errors: tuple[ValidationIssue, ...] = ()
    warnings: tuple[ValidationIssue, ...] = ()

    @property
    def ok(self) -> bool:
        return not self.errors

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "errors": [issue.as_dict() for issue in self.errors],
            "warnings": [issue.as_dict() for issue in self.warnings],
        }


def _blank_domain(value: Any = None) -> dict[str, Any]:
    return {"locked": False, "value": value, "evidence_ids": []}


def _blank_lock() -> dict[str, Any]:
    return {"enabled": True, "status": "unlocked", "fingerprint": None, "evidence_ids": []}


def create_canonical_payload(
    *,
    mode: str,
    source_kind: str,
    source_ref: str,
    project: Mapping[str, Any] | None = None,
    evidence: Sequence[Mapping[str, Any]] | None = None,
    auto_classification: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if mode not in ("drawing", "sketch"):
        raise ValueError(f"Unsupported intake mode: {mode}")
    allowed = DRAWING_KINDS if mode == "drawing" else SKETCH_KINDS
    if source_kind not in allowed:
        raise ValueError(f"{mode} intake requires one of {allowed}; got {source_kind}")
    if not source_ref:
        raise ValueError("source_ref is required")

    source_project = dict(project or {})
    project_id = str(source_project.get("project_id") or f"project-{uuid4().hex[:12]}")
    now = utc_now()
    evidence_items = [dict(item) for item in (evidence or [])]
    if not evidence_items:
        evidence_items = [{
            "id": "evidence:intake:1",
            "kind": "observation",
            "source_ref": source_ref,
            "content": f"User explicitly selected {source_kind} intake.",
            "confidence": 1.0,
        }]
    classification = dict(auto_classification or {
        "label": source_kind,
        "confidence": 1.0,
        "advisory_only": True,
    })
    classification["advisory_only"] = True
    evidence_ids = [str(item["id"]) for item in evidence_items if item.get("id")]
    project_data = {
        "project_id": project_id,
        "name": str(source_project.get("name") or "未命名空间项目"),
        "description": str(source_project.get("description") or ""),
        "ratio": str(source_project.get("ratio") or "9:16"),
        "duration": str(source_project.get("duration") or "15秒"),
        "space_type": str(source_project.get("space_type") or source_project.get("spaceType") or ""),
        "style": str(source_project.get("style") or ""),
    }
    empty_elements: list[dict[str, Any]] = []
    payload: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "space_core": {
            "model_id": f"space-model-{uuid4().hex[:12]}",
            "state": "DRAFT",
            "created_at": now,
            "updated_at": now,
        },
        "project": project_data,
        "intake": {
            "mode": mode,
            "source_kind": source_kind,
            "source_refs": [source_ref],
            "auto_classification": classification,
            "evidence": evidence_items,
        },
        "space": {
            "camera": _blank_domain(),
            "perspective": _blank_domain(),
            "geometry": _blank_domain({"levels": [], "elements": empty_elements}),
            "openings": _blank_domain({"items": []}),
            "anchors": _blank_domain({"items": []}),
            "design_intent": {"description": project_data["description"], "evidence_ids": evidence_ids},
        },
        "locks": {name: _blank_lock() for name in LOCK_NAMES},
        "assets": [],
    }
    return payload


class CanonicalSpaceModel:
    """Mutable wrapper around a versioned, JSON-serializable canonical model."""

    def __init__(self, payload: Mapping[str, Any]):
        self.data: dict[str, Any] = _copy(dict(payload))

    @classmethod
    def from_intake(cls, **kwargs: Any) -> "CanonicalSpaceModel":
        return cls(create_canonical_payload(**kwargs))

    @classmethod
    def from_legacy_project(cls, payload: Mapping[str, Any], *, intake_kind: str = "rough_sketch") -> "CanonicalSpaceModel":
        project = dict(payload.get("project") or {})
        return cls.from_intake(
            mode="sketch",
            source_kind=intake_kind,
            source_ref="legacy:examples/demo-project.json",
            project=project,
            evidence=[{
                "id": "evidence:legacy:1",
                "kind": "observation",
                "source_ref": "legacy:examples/demo-project.json",
                "content": "Imported from the existing Space Evolution v1.0 project shape.",
                "confidence": 1.0,
            }],
            auto_classification={"label": intake_kind, "confidence": 1.0, "advisory_only": True},
        )

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "CanonicalSpaceModel":
        return cls(payload)

    @property
    def model_id(self) -> str:
        return str(self.data["space_core"]["model_id"])

    @property
    def state(self) -> str:
        return str(self.data["space_core"]["state"])

    def to_dict(self) -> dict[str, Any]:
        return _copy(self.data)

    def to_json(self) -> str:
        return json.dumps(self.data, ensure_ascii=False, indent=2) + "\n"

    def update_space_domain(self, name: str, value: Any) -> None:
        if name not in LOCK_NAMES:
            raise ValueError(f"Only locked space domains may be updated: {LOCK_NAMES}")
        self.data["space"][name] = _copy(value)
        from .locks import SpatialEngineeringLock

        SpatialEngineeringLock(self).mark_stale((name,))
        self._touch()

    def add_evidence(self, *, kind: str, source_ref: str, content: str, confidence: float | None = None, evidence_id: str | None = None) -> str:
        if kind not in EVIDENCE_KINDS:
            raise ValueError(f"Unsupported evidence kind: {kind}")
        item_id = evidence_id or f"evidence:{uuid4().hex[:12]}"
        item: dict[str, Any] = {"id": item_id, "kind": kind, "source_ref": source_ref, "content": content}
        if confidence is not None:
            item["confidence"] = confidence
        self.data["intake"]["evidence"].append(item)
        self._touch()
        return item_id

    def register_asset(
        self,
        *,
        stage: str,
        prompt: str,
        provider: str,
        parent_asset_id: str | None = None,
        status: str = "ready",
    ) -> dict[str, Any]:
        if stage not in STAGES:
            raise ValueError(f"Unsupported stage: {stage}")
        if status not in ("planned", "ready", "stale", "blocked"):
            raise ValueError(f"Unsupported asset status: {status}")
        existing = next((item for item in self.data["assets"] if item.get("stage") == stage), None)
        revision = int(existing.get("revision", 0)) + 1 if existing else 1
        asset_id = str(existing.get("asset_id")) if existing else f"asset:{stage}:{uuid4().hex[:8]}"
        asset = {
            "asset_id": asset_id,
            "stage": stage,
            "spatial_dna_version": SCHEMA_VERSION,
            "parent_asset_id": parent_asset_id,
            "prompt": prompt,
            "continuity_locks": list(LOCK_NAMES),
            "provider": provider,
            "revision": revision,
            "status": status,
            "lock_fingerprints": {
                name: str(self.data["locks"][name].get("fingerprint") or "") for name in LOCK_NAMES
            },
        }
        if existing:
            index = self.data["assets"].index(existing)
            self.data["assets"][index] = asset
        else:
            self.data["assets"].append(asset)
        self._touch()
        return _copy(asset)

    def validate(self) -> ValidationReport:
        from .locks import SpatialEngineeringLock

        SpatialEngineeringLock(self).detect_changes()
        return validate_payload(self.data)

    def _touch(self) -> None:
        self.data["space_core"]["updated_at"] = utc_now()


def validate_payload(payload: Mapping[str, Any]) -> ValidationReport:
    errors: list[ValidationIssue] = []
    warnings: list[ValidationIssue] = []

    def error(code: str, path: str, message: str) -> None:
        errors.append(ValidationIssue(code, path, message))

    if payload.get("schema_version") != SCHEMA_VERSION:
        error("schema_version", "schema_version", f"Expected {SCHEMA_VERSION}.")
    for key in ("space_core", "project", "intake", "space", "locks", "assets"):
        if not isinstance(payload.get(key), (dict, list)):
            error("required", key, f"Missing or invalid required field: {key}.")
    core = payload.get("space_core")
    if isinstance(core, Mapping):
        if core.get("state") not in MODEL_STATES:
            error("state", "space_core.state", "Unknown model state.")
        for field in ("model_id", "created_at", "updated_at"):
            if not core.get(field):
                error("required", f"space_core.{field}", f"Missing {field}.")

    project = payload.get("project")
    if isinstance(project, Mapping):
        for field in ("project_id", "name", "description", "ratio", "duration", "space_type", "style"):
            if field not in project:
                error("required", f"project.{field}", f"Missing {field}.")

    intake = payload.get("intake")
    evidence_ids: set[str] = set()
    if isinstance(intake, Mapping):
        mode = intake.get("mode")
        source_kind = intake.get("source_kind")
        if mode not in ("drawing", "sketch"):
            error("intake_mode", "intake.mode", "Intake mode must be drawing or sketch.")
        allowed = DRAWING_KINDS if mode == "drawing" else SKETCH_KINDS
        if source_kind not in allowed:
            error("source_kind", "intake.source_kind", f"Source kind is not valid for {mode} intake.")
        if not isinstance(intake.get("source_refs"), list) or not intake["source_refs"]:
            error("source_ref", "intake.source_refs", "At least one source reference is required.")
        classification = intake.get("auto_classification")
        if not isinstance(classification, Mapping) or classification.get("advisory_only") is not True:
            error("classification_boundary", "intake.auto_classification", "Automatic classification must remain advisory only.")
        evidence = intake.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            error("evidence", "intake.evidence", "At least one input evidence item is required.")
        elif isinstance(evidence, list):
            for index, item in enumerate(evidence):
                if not isinstance(item, Mapping):
                    error("evidence_item", f"intake.evidence[{index}]", "Evidence item must be an object.")
                    continue
                item_id = item.get("id")
                if not item_id or item_id in evidence_ids:
                    error("evidence_id", f"intake.evidence[{index}].id", "Evidence ids must be present and unique.")
                if item_id:
                    evidence_ids.add(str(item_id))
                if item.get("kind") not in EVIDENCE_KINDS:
                    error("evidence_kind", f"intake.evidence[{index}].kind", "Unknown evidence kind.")

    space = payload.get("space")
    if isinstance(space, Mapping):
        for name in LOCK_NAMES:
            domain = space.get(name)
            if not isinstance(domain, Mapping):
                error("domain", f"space.{name}", "Missing locked domain.")
            else:
                if not isinstance(domain.get("evidence_ids"), list):
                    error("domain_evidence", f"space.{name}.evidence_ids", "evidence_ids must be a list.")
        intent = space.get("design_intent")
        if not isinstance(intent, Mapping):
            error("design_intent", "space.design_intent", "Missing design intent.")

    locks = payload.get("locks")
    if isinstance(locks, Mapping):
        for name in LOCK_NAMES:
            lock = locks.get(name)
            if not isinstance(lock, Mapping):
                error("lock", f"locks.{name}", "Missing lock record.")
                continue
            if lock.get("status") not in ("unlocked", "locked", "stale"):
                error("lock_status", f"locks.{name}.status", "Unknown lock status.")
            if lock.get("enabled") is not True:
                error("lock_disabled", f"locks.{name}.enabled", "All five engineering locks must remain enabled.")
            if lock.get("status") != "locked":
                error("lock_not_ready", f"locks.{name}.status", "All five engineering locks must be locked before execution.")
            domain = space.get(name) if isinstance(space, Mapping) else None
            if isinstance(domain, Mapping) and domain.get("locked") is not True:
                error("domain_not_locked", f"space.{name}.locked", "The canonical domain is not locked.")
            stored = lock.get("fingerprint")
            if lock.get("status") == "locked" and stored:
                current = fingerprint(domain)
                if current != stored:
                    error("lock_drift", f"locks.{name}.fingerprint", "Locked domain changed since capture.")

    assets = payload.get("assets")
    if isinstance(assets, list):
        asset_ids: set[str] = set()
        for index, asset in enumerate(assets):
            path = f"assets[{index}]"
            if not isinstance(asset, Mapping):
                error("asset_item", path, "Asset must be an object.")
                continue
            asset_id = asset.get("asset_id")
            if not asset_id or asset_id in asset_ids:
                error("asset_id", f"{path}.asset_id", "Asset ids must be present and unique.")
            if asset_id:
                asset_ids.add(str(asset_id))
            if asset.get("stage") not in STAGES:
                error("asset_stage", f"{path}.stage", "Unknown workflow stage.")
            if asset.get("spatial_dna_version") != SCHEMA_VERSION:
                error("asset_version", f"{path}.spatial_dna_version", "Asset must use the canonical schema version.")
            if asset.get("status") == "stale":
                warnings.append(ValidationIssue("stale_asset", path, "Asset is stale and must not be submitted to an external provider.", "warning"))

    return ValidationReport(tuple(errors), tuple(warnings))
