# Sayelf Space Evolution Skill v1.0

## Purpose
Turn a text idea, reference image, or hand sketch into a continuous spatial evolution sequence:

`Sketch → Structure / Line Becomes Wall → Finished Space → Film Storyboard`

## Prime Rule
**Completion changes; space does not.**

The skill must preserve the same Spatial DNA across stages unless the user explicitly unlocks or changes geometry.

## Required Spatial Locks
1. Camera position, height, direction, focal behavior
2. Horizon line, vanishing points, perspective
3. Major walls, columns, beams, slabs, stairs, floor levels
4. Door/window/opening position and proportion
5. Major spatial anchors and foreground/midground/background relationship

## Stage 01 — Sketch Cleanup
- Preserve the original hand sketch intent.
- Remove paper noise and meaningless guide lines.
- Clarify spatial relationships without redesign.
- Keep an architectural hand-drawn character.

## Stage 02 — Line Becomes Wall
- Inherit Stage 01 exactly.
- Convert existing key lines into architectural thickness and structure.
- Do not move walls, resize openings, flip stairs, change room proportions, or change camera.
- Keep materials neutral; emphasize structural emergence.

## Stage 03 — Space Formation
- Inherit Stage 02 geometry exactly.
- Add materials, natural light, furniture, plants, human scale and atmosphere only.
- Avoid geometry drift, plastic textures, fake bokeh and excessive HDR.

## Stage 04 — Film
- Use Stage 03 as the preferred first/reference frame for I2V.
- Motion must not destroy geometry.
- Preferred motion: slow push-in, restrained tilt-up, subtle parallax.
- Forbidden: wall melting, opening drift, furniture teleportation, camera jump.

## Local-first Principle
Use deterministic local templates, state, caching, validation and dependency tracking before calling an LLM. Only use external models when semantic interpretation or media generation is actually required.

## Asset Contract
Every generated asset should retain:
- project_id
- asset_id
- stage
- spatial_dna_version
- parent_asset_id
- prompt
- continuity_locks
- provider (if used)
- revision

## User Interaction
If the user changes geometry, update Spatial DNA first and mark downstream assets stale. Do not silently regenerate unrelated stages.
