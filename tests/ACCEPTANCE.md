# v1.0 Acceptance

A build is accepted when:
1. `python app.py` starts with no third-party dependency.
2. `/api/health` returns version 1.0.0.
3. WebUI opens locally.
4. A hand sketch can be selected and previewed.
5. Five preset scenes are available for direct trial and can populate the project fields locally.
6. Space style options include modern minimal, American, French, wabi-sabi, simplified Chinese and Chinese styles.
7. Space type options include modern commercial, exhibition hall, sports arena, office, hotel lobby and cultural center.
8. Space type and style can be combined in generated prompts without changing the six-stage workflow.
9. Changing style changes the visual direction text without changing the six-stage workflow.
10. Material and completion level are matched to scene, architecture, type and style; concrete is not forced unless specified.
11. Explicit project name, space type and style phrases in the customer description locally match existing fields before generation.
12. A manual project name, space type or style selection is preserved on later description edits.
13. An unclear description keeps the current field defaults and does not invent a new option or call an external model.
14. Stage 01 prompt contains only the major framework and explicitly shows the stroke moving across paper.
15. Stage 02 prompt contains the main structural skeleton, while Stage 03 retains its current sketch treatment.
16. Each generated prompt carries customer-described needs into a visual focus and first-look viewpoint impact without changing locked geometry.
17. Clicking Save Project writes JSON to the local exports path and displays the returned path; unavailable local save falls back to a download.
18. Selecting 9:16 or 4:5 records one independent image per stage and a horizontal-row presentation for five or N images.
19. The ratio principle forbids merging, cropping or stretching individual stage images.
20. Six independent prompts are generated locally: line, linework, sketch, wall, space generation and film.
21. Each independent prompt has its own copy action, including the film prompt.
22. Five continuity locks are enabled by default.
23. Project JSON can be exported.
24. Workflow Markdown can be exported.
25. No external API is called during local prompt generation or copying.
26. README clearly states the boundary between the local workflow and third-party media generation.
27. README includes the five public workflow demonstration images.
