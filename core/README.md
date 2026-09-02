# Space Core v0.1

`core/space_core/` 是从现有 Space Evolution v1.0 抽取的最小平台无关核心。

```text
Drawing Intake (plan / elevation / section) ─┐
                                             ├─ Canonical Space Model
Sketch Intake (rough sketch / linework) ─────┘          │
                                                        ↓
                                         Spatial Engineering Lock
                                                        ↓
                                              Native / optional Provider
```

## Zero-plugin path

```python
from core.space_core import DrawingIntake, NativeProvider, SpatialEngineeringLock

model = DrawingIntake(
    source_ref="local/plan.pdf",
    drawing_kind="plan",
    project={"name": "PoC", "description": "脱敏空间测试"},
).ingest()
SpatialEngineeringLock(model).lock_all()
result = NativeProvider().execute(model, "build_prompts")
```

核心只使用 Python 标准库。专业软件、图像/视频模型、DWG/DXF/PDF 几何解析和远程接口都在 Core 外部。
