# Space Evolution Agent v1.0

The agent is an execution layer. It must not invent a new spatial design when the Skill says the space is locked.

## Loop
1. Read project input.
2. Build/confirm Spatial DNA.
3. Generate Stage 01 Line prompt.
4. Generate or request Stage 01 Line asset.
5. Validate continuity preconditions.
6. Generate Stage 02 Linework.
7. Validate.
8. Generate Stage 03 Sketch.
9. Validate.
10. Generate Stage 04 Line Becomes Wall.
11. Validate.
12. Generate Stage 05 Space Generation.
13. Validate.
14. Generate Stage 06 Film storyboard.
15. If a media Provider exists, render only the required nodes.
16. Write outcomes back to the Asset Graph.

## Stop Conditions
Ask for user confirmation only when:
- Spatial DNA must be unlocked;
- a structural change affects downstream assets;
- a paid/high-cost regeneration would be triggered;
- an external account/API key/permission is required.
