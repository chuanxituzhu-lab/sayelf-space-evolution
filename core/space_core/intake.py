from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePath
from typing import Any, Mapping, Sequence

from .canonical import CanonicalSpaceModel, DRAWING_KINDS, SKETCH_KINDS


@dataclass(frozen=True)
class InputSuggestion:
    """A non-authoritative hint; it can never select an intake route."""

    label: str
    confidence: float
    advisory_only: bool = True

    def as_dict(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "confidence": self.confidence,
            "advisory_only": True,
        }


def suggest_input_kind(source_ref: str) -> InputSuggestion:
    """Suggest a kind from a filename without changing the user's chosen route."""
    name = PurePath(source_ref).name.lower()
    if any(token in name for token in ("plan", "floor", "平面")):
        return InputSuggestion("plan", 0.70)
    if any(token in name for token in ("elevation", "立面")):
        return InputSuggestion("elevation", 0.70)
    if any(token in name for token in ("section", "剖面")):
        return InputSuggestion("section", 0.70)
    if any(token in name for token in ("sketch", "draft", "草稿", "草图", "线稿")):
        return InputSuggestion("rough_sketch", 0.70)
    return InputSuggestion("unknown", 0.0)


def _evidence(source_ref: str, source_kind: str, extra: Sequence[Mapping[str, Any]] | None) -> list[dict[str, Any]]:
    items = [{
        "id": f"evidence:{source_kind}:selection",
        "kind": "observation",
        "source_ref": source_ref,
        "content": f"User explicitly selected {source_kind} as the input kind.",
        "confidence": 1.0,
    }]
    items.extend(dict(item) for item in (extra or ()))
    return items


class DrawingIntake:
    """Explicit engineering drawing entry: plan, elevation, or section."""

    mode = "drawing"

    def __init__(
        self,
        *,
        source_ref: str,
        drawing_kind: str,
        project: Mapping[str, Any] | None = None,
        observations: Sequence[Mapping[str, Any]] | None = None,
        suggestion: InputSuggestion | None = None,
    ) -> None:
        if drawing_kind not in DRAWING_KINDS:
            raise ValueError(f"drawing_kind must be one of {DRAWING_KINDS}")
        self.source_ref = source_ref
        self.drawing_kind = drawing_kind
        self.project = dict(project or {})
        self.observations = tuple(observations or ())
        self.suggestion = suggestion or suggest_input_kind(source_ref)

    def ingest(self) -> CanonicalSpaceModel:
        return CanonicalSpaceModel.from_intake(
            mode=self.mode,
            source_kind=self.drawing_kind,
            source_ref=self.source_ref,
            project=self.project,
            evidence=_evidence(self.source_ref, self.drawing_kind, self.observations),
            auto_classification=self.suggestion.as_dict(),
        )


class SketchIntake:
    """Explicit concept/sketch entry; uncertain geometry remains non-factual."""

    mode = "sketch"

    def __init__(
        self,
        *,
        source_ref: str,
        sketch_kind: str = "rough_sketch",
        project: Mapping[str, Any] | None = None,
        observations: Sequence[Mapping[str, Any]] | None = None,
        suggestion: InputSuggestion | None = None,
    ) -> None:
        if sketch_kind not in SKETCH_KINDS:
            raise ValueError(f"sketch_kind must be one of {SKETCH_KINDS}")
        self.source_ref = source_ref
        self.sketch_kind = sketch_kind
        self.project = dict(project or {})
        self.observations = tuple(observations or ())
        self.suggestion = suggestion or suggest_input_kind(source_ref)

    def ingest(self) -> CanonicalSpaceModel:
        return CanonicalSpaceModel.from_intake(
            mode=self.mode,
            source_kind=self.sketch_kind,
            source_ref=self.source_ref,
            project=self.project,
            evidence=_evidence(self.source_ref, self.sketch_kind, self.observations),
            auto_classification=self.suggestion.as_dict(),
        )
