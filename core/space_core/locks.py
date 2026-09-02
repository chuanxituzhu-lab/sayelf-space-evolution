from __future__ import annotations

from typing import Iterable

from .canonical import CanonicalSpaceModel, LOCK_NAMES, fingerprint


class SpatialEngineeringLock:
    """Five-lock guard for camera, perspective, geometry, openings, and anchors."""

    def __init__(self, model: CanonicalSpaceModel):
        self.model = model

    def current_fingerprints(self) -> dict[str, str]:
        space = self.model.data["space"]
        return {name: fingerprint(space[name]) for name in LOCK_NAMES}

    def enable_all(self) -> None:
        for name in LOCK_NAMES:
            self.model.data["locks"][name]["enabled"] = True

    def lock_all(self, *, evidence_ids: Iterable[str] = ()) -> None:
        ids = list(dict.fromkeys(str(item) for item in evidence_ids))
        self.enable_all()
        for name in LOCK_NAMES:
            domain = self.model.data["space"][name]
            domain["locked"] = True
            if ids:
                domain["evidence_ids"] = list(ids)
        current = self.current_fingerprints()
        for name in LOCK_NAMES:
            lock = self.model.data["locks"][name]
            lock["status"] = "locked"
            lock["fingerprint"] = current[name]
            lock["evidence_ids"] = list(ids)
        self.model.data["space_core"]["state"] = "LOCKED"
        self.model._touch()

    def mark_stale(self, names: Iterable[str] = LOCK_NAMES) -> tuple[str, ...]:
        changed = tuple(dict.fromkeys(name for name in names if name in LOCK_NAMES))
        if not changed:
            return changed
        for name in changed:
            lock = self.model.data["locks"][name]
            lock["status"] = "stale"
            self.model.data["space"][name]["locked"] = False
        for asset in self.model.data.get("assets", []):
            if asset.get("status") in ("planned", "ready"):
                asset["status"] = "stale"
        self.model.data["space_core"]["state"] = "STALE"
        self.model._touch()
        return changed

    def detect_changes(self) -> tuple[str, ...]:
        current = self.current_fingerprints()
        changed: list[str] = []
        for name in LOCK_NAMES:
            lock = self.model.data["locks"][name]
            if lock.get("status") == "locked" and lock.get("fingerprint") != current[name]:
                changed.append(name)
        if changed:
            self.mark_stale(changed)
        return tuple(changed)

    def all_locked(self) -> bool:
        return all(
            self.model.data["locks"][name].get("enabled") is True
            and self.model.data["locks"][name].get("status") == "locked"
            and self.model.data["space"][name].get("locked") is True
            for name in LOCK_NAMES
        )
