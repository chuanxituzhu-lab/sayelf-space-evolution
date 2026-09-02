from __future__ import annotations

import json
import unittest
from pathlib import Path

from core.space_core import (
    DrawingIntake,
    LOCK_NAMES,
    NativeProvider,
    SCHEMA_VERSION,
    SketchIntake,
    SpatialEngineeringLock,
    STAGES,
)


ROOT = Path(__file__).resolve().parents[1]


class SpaceCoreV01Tests(unittest.TestCase):
    def project(self) -> dict[str, str]:
        return {
            "project_id": "test-project-001",
            "name": "测试展厅",
            "description": "脱敏展厅，左侧高窗，右侧短楼梯。",
            "ratio": "16:9",
            "duration": "15秒",
            "space_type": "展厅",
            "style": "现代极简",
        }

    def locked_model(self):
        model = SketchIntake(
            source_ref="local-fixture/concept-sketch.png",
            sketch_kind="rough_sketch",
            project=self.project(),
        ).ingest()
        SpatialEngineeringLock(model).lock_all()
        return model

    def test_schema_artifact_is_versioned_and_declares_canonical_roots(self):
        schema = json.loads((ROOT / "core/schemas/canonical-space.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(schema["properties"]["schema_version"]["const"], SCHEMA_VERSION)
        self.assertEqual(
            schema["required"],
            ["schema_version", "space_core", "project", "intake", "space", "locks", "assets"],
        )

    def test_drawing_and_sketch_have_the_same_canonical_shape(self):
        drawing = DrawingIntake(
            source_ref="local-fixture/floor-plan.pdf",
            drawing_kind="plan",
            project=self.project(),
        ).ingest()
        sketch = SketchIntake(
            source_ref="local-fixture/concept-sketch.png",
            sketch_kind="rough_sketch",
            project=self.project(),
        ).ingest()
        self.assertEqual(set(drawing.data), set(sketch.data))
        self.assertEqual(set(drawing.data["space"]), set(sketch.data["space"]))
        self.assertEqual(set(drawing.data["locks"]), set(LOCK_NAMES))
        self.assertEqual(set(sketch.data["locks"]), set(LOCK_NAMES))
        self.assertEqual(drawing.data["intake"]["mode"], "drawing")
        self.assertEqual(sketch.data["intake"]["mode"], "sketch")

    def test_explicit_route_wins_and_auto_classification_is_advisory(self):
        model = DrawingIntake(
            source_ref="local-fixture/floor-plan.png",
            drawing_kind="section",
            project=self.project(),
        ).ingest()
        self.assertEqual(model.data["intake"]["source_kind"], "section")
        self.assertEqual(model.data["intake"]["auto_classification"]["label"], "plan")
        self.assertTrue(model.data["intake"]["auto_classification"]["advisory_only"])

    def test_five_locks_are_enabled_by_default_and_require_capture(self):
        model = SketchIntake(source_ref="local-fixture/sketch.png").ingest()
        self.assertTrue(all(model.data["locks"][name]["enabled"] for name in LOCK_NAMES))
        self.assertFalse(SpatialEngineeringLock(model).all_locked())
        self.assertFalse(model.validate().ok)
        SpatialEngineeringLock(model).lock_all()
        self.assertTrue(SpatialEngineeringLock(model).all_locked())
        self.assertTrue(model.validate().ok, model.validate().as_dict())
        self.assertEqual(model.state, "LOCKED")

    def test_geometry_change_marks_lock_and_downstream_assets_stale(self):
        model = self.locked_model()
        NativeProvider().execute(model, "build_prompts")
        self.assertEqual(len(model.data["assets"]), len(STAGES))
        model.update_space_domain("geometry", {"locked": False, "value": {"elements": [{"id": "wall-1"}]}, "evidence_ids": []})
        self.assertEqual(model.state, "STALE")
        self.assertEqual(model.data["locks"]["geometry"]["status"], "stale")
        self.assertTrue(all(asset["status"] == "stale" for asset in model.data["assets"]))
        self.assertFalse(model.validate().ok)
        result = NativeProvider().execute(model, "plan")
        self.assertFalse(result.ok)
        self.assertEqual(result.external_calls, 0)

    def test_native_provider_is_complete_without_plugins(self):
        model = self.locked_model()
        provider = NativeProvider()
        self.assertFalse(provider.manifest()["requires_auth"])
        planned = provider.execute(model, "plan")
        self.assertTrue(planned.ok, planned.as_dict())
        self.assertEqual(planned.external_calls, 0)
        built = provider.execute(model, "build_prompts")
        self.assertTrue(built.ok, built.as_dict())
        self.assertEqual(tuple(built.payload["stages"]), STAGES)
        self.assertEqual([asset["stage"] for asset in model.data["assets"]], list(STAGES))
        self.assertEqual(model.data["assets"][0]["parent_asset_id"], None)
        self.assertIsNotNone(model.data["assets"][1]["parent_asset_id"])

    def test_legacy_space_skill_project_is_readable(self):
        legacy = json.loads((ROOT / "examples/demo-project.json").read_text(encoding="utf-8"))
        from core.space_core.canonical import CanonicalSpaceModel

        model = CanonicalSpaceModel.from_legacy_project(legacy)
        self.assertEqual(model.data["project"]["space_type"], legacy["project"]["spaceType"])
        self.assertEqual(model.data["project"]["style"], legacy["project"]["style"])
        SpatialEngineeringLock(model).lock_all()
        result = NativeProvider().execute(model, "build_prompts")
        self.assertTrue(result.ok, result.as_dict())
        self.assertEqual(len(model.data["assets"]), 6)

    def test_evidence_kinds_are_preserved_without_promotion(self):
        model = SketchIntake(
            source_ref="local-fixture/sketch.png",
            observations=[{
                "id": "evidence:hypothesis:scale",
                "kind": "hypothesis",
                "source_ref": "local-fixture/sketch.png",
                "content": "门洞尺寸待核验。",
                "confidence": 0.35,
            }],
        ).ingest()
        kinds = {item["kind"] for item in model.data["intake"]["evidence"]}
        self.assertIn("hypothesis", kinds)
        self.assertNotIn("fact", kinds)


if __name__ == "__main__":
    unittest.main()
