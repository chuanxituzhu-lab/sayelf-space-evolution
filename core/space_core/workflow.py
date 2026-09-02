from __future__ import annotations

from typing import Any

from .canonical import CanonicalSpaceModel, LOCK_NAMES, STAGES


def _lock_text(model: CanonicalSpaceModel) -> str:
    labels = {
        "camera": "同一机位、相机高度、朝向与焦距",
        "perspective": "同一地平线、透视关系与消失点",
        "geometry": "同一墙、柱、梁、楼板、楼梯及层高关系",
        "openings": "同一门窗尺寸、位置与开口比例",
        "anchors": "同一核心家具与前中后景锚点",
    }
    return "\n".join(f"- {labels[name]}" for name in LOCK_NAMES if model.data["locks"][name].get("status") == "locked")


def _base(model: CanonicalSpaceModel) -> str:
    project = model.data["project"]
    return "\n".join([
        f"项目：{project['name']}",
        f"空间描述：{project['description'] or '依据输入资料，不新增未经证实的空间结构。'}",
        f"空间类型：{project['space_type'] or '未指定；保持输入中的功能关系。'}",
        f"画幅：{project['ratio']}",
        f"视觉方向：{project['style'] or '沿用客户原始意图，材质和光线保持克制。'}",
        "客户关联与第一眼视角：只把描述中明确的使用场景、情绪、记忆或品牌需求转成视觉焦点、前景引导、尺度参照和光线节奏；不得新增故事或改变机位、几何。",
        "Spatial Engineering Lock：",
        _lock_text(model),
        "最高规则：变的是完成度，不变的是空间。",
    ])


def build_prompts(model: CanonicalSpaceModel, *, provider_id: str = "native.local") -> dict[str, str]:
    """Build the original six local workflow prompts and register them as assets."""
    report = model.validate()
    if not report.ok:
        details = "; ".join(f"{issue.path}: {issue.message}" for issue in report.errors)
        raise ValueError(f"Cannot build prompts before the canonical model is locked: {details}")

    base = _base(model)
    prompts: dict[str, str] = {
        "line": f"{base}\n\n【阶段 01｜线】\n只保留 3—6 个最重要的大框架、主要体块轮廓、地平线和一条主轴；不画家具、材质、阴影、细节或辅助线。镜头近距离观察纸面，一笔清晰经历接触、移动、停顿、转向和落下，保留大片留白与原始构图。",
        "linework": f"{base}\n\n【阶段 02｜线稿】\n严格继承阶段 01，只叠加主要墙体、柱、梁、楼板、楼梯、开口、地平线和前中后景关系。保持建筑线稿特征，不展开装饰、家具、最终材质或新的空间布局。",
        "sketch": f"{base}\n\n【阶段 03｜草图】\n严格继承阶段 02，形成完整建筑草图，明确体块、透视、比例、空间关系和主要构件；清理无意义辅助线但保留探索性的手绘笔触。不加入最终材质，不改变原设计。",
        "wall": f"{base}\n\n【阶段 04｜线落成墙】\n严格继承阶段 03，将已有关键线条转为有厚度和结构逻辑的墙、柱、梁、楼板、窗框、楼梯及固定构件。不得移动墙体、改变门窗、翻转楼梯、改变层高或重新布局；保持建筑灰模/白模状态。",
        "space": f"{base}\n\n【阶段 05｜空间生成】\n严格继承阶段 04 的全部几何。只增加与空间类型、结构和视觉方向匹配的材质、自然光、家具、植物和生活尺度；不得移动墙、柱、门窗、楼梯或相机。避免塑料质感与过度 HDR。",
        "film": f"{base}\n\n【阶段 06｜{model.data['project']['duration']} 视频分镜】\n按 Line → Linework → Sketch → Line Becomes Wall → Space Generation 连续演化；相机只做缓慢推进、克制抬升或细微视差。阶段 05 作为首帧，必要时以阶段 04 作为结构参考。严禁结构漂移、墙体融化、门窗变形、家具瞬移和相机跳变。",
    }
    previous: str | None = None
    for stage in STAGES:
        asset = model.register_asset(
            stage=stage,
            prompt=prompts[stage],
            provider=provider_id,
            parent_asset_id=previous,
            status="ready",
        )
        previous = asset["asset_id"]
    return prompts
