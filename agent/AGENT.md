# Space Evolution Agent v1.0

The agent is an execution layer. It must not invent a new spatial design when the Skill says the space is locked.

## Loop
1. Read project input.
2. Build/confirm Spatial DNA.
3. Generate six independent prompts locally: five spatial prompts and one film prompt.
4. In preview mode, hand each prompt to the user's chosen AI platform; do not call a provider automatically.
5. Generate or request Stage 01 Line asset.
6. Validate continuity preconditions.
7. Generate Stage 02 Linework.
8. Validate.
9. Generate Stage 03 Sketch.
10. Validate.
11. Generate Stage 04 Line Becomes Wall.
12. Validate.
13. Generate Stage 05 Space Generation.
14. Validate.
15. Generate Stage 06 Film storyboard.
16. If a media Provider exists, render only the required nodes.
17. Write outcomes back to the Asset Graph.

## Stop Conditions
Ask for user confirmation only when:
- Spatial DNA must be unlocked;
- a structural change affects downstream assets;
- a paid/high-cost regeneration would be triggered;
- an external account/API key/permission is required.
