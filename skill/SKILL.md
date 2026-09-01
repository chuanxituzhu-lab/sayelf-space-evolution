# Sayelf Space Evolution Skill v1.0

## Purpose
Turn a text idea, reference image, or hand sketch into a continuous spatial evolution sequence:

`Line → Linework → Sketch → Line Becomes Wall → Space Generation → Film Storyboard`

## Prime Rule
**Completion changes; space does not.**

The skill must preserve the same Spatial DNA across stages unless the user explicitly unlocks or changes geometry.

## Required Spatial Locks
1. Camera position, height, direction, focal behavior
2. Horizon line, vanishing points, perspective
3. Major walls, columns, beams, slabs, stairs, floor levels
4. Door/window/opening position and proportion
5. Major spatial anchors and foreground/midground/background relationship

## Stage 01 — Line
- Start from the first meaningful line and preserve its direction, weight and spatial intent.
- Establish the initial outline of the imagined space without adding unrequested structure.

## Stage 02 — Linework
- Inherit Stage 01 exactly.
- Layer lines to clarify foreground, middle ground, background, openings, stairs and spatial anchors.
- Keep an architectural line-drawing character; do not add final materials.

## Stage 03 — Sketch
- Inherit Stage 02 exactly.
- Form a complete architectural sketch with clear massing, perspective, proportion and spatial relationships.
- Remove paper noise and meaningless guide lines while keeping an exploratory hand-drawn character.

## Stage 04 — Line Becomes Wall
- Inherit Stage 03 exactly.
- Convert existing key lines into architectural thickness and structure.
- Do not move walls, resize openings, flip stairs, change room proportions, or change camera.
- Keep materials neutral; emphasize structural emergence.

## Stage 05 — Space Generation
- Inherit Stage 04 geometry exactly.
- Add materials, natural light, furniture, plants, human scale and atmosphere only.
- Avoid geometry drift, plastic textures, fake bokeh and excessive HDR.

## Stage 06 — Film
- Use Stage 05 as the preferred first/reference frame for I2V.
- Motion must not destroy geometry.
- Preferred motion: slow push-in, restrained tilt-up, subtle parallax.
- Forbidden: wall melting, opening drift, furniture teleportation, camera jump.

## Mobile / Social Presentation Principle
When the selected single-image ratio is `9:16` or `4:5`, output one independent image per stage. When presenting five or N stage images, keep them at a consistent height and arrange them in one horizontal row for mobile and social-media viewing. Never merge the assets into one image, crop them, or stretch their individual ratio.

## Description-first Matching Principle
When a customer description explicitly names a project, space type, or style, match it locally against the existing project field and select options before prompt generation. Preserve a customer-edited field as a manual override. If no clear keyword is present, keep the current default and do not invent a new category or call an external model.

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
