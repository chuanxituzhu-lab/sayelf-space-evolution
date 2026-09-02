from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.space_core import DrawingIntake, NativeProvider, SketchIntake, SpatialEngineeringLock


def main() -> int:
    fixture = json.loads(Path(__file__).with_name("space-core-poc.json").read_text(encoding="utf-8"))
    project = fixture["project"]
    drawing_spec = fixture["drawing_input"]
    sketch_spec = fixture["sketch_input"]
    drawing = DrawingIntake(
        source_ref=drawing_spec["source_ref"],
        drawing_kind=drawing_spec["drawing_kind"],
        project=project,
        observations=drawing_spec["observations"],
    ).ingest()
    sketch = SketchIntake(
        source_ref=sketch_spec["source_ref"],
        sketch_kind=sketch_spec["sketch_kind"],
        project=project,
    ).ingest()
    provider = NativeProvider()
    for model in (drawing, sketch):
        SpatialEngineeringLock(model).lock_all()
        result = provider.execute(model, "build_prompts")
        print(json.dumps({
            "mode": model.data["intake"]["mode"],
            "source_kind": model.data["intake"]["source_kind"],
            "state": model.state,
            "result": result.as_dict(),
            "assets": len(model.data["assets"]),
        }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
