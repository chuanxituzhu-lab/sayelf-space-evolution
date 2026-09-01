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
11. Selecting 9:16 or 4:5 records one independent image per stage and a horizontal-row presentation for five or N images.
12. The ratio principle forbids merging, cropping or stretching individual stage images.
13. Six independent prompts are generated locally: line, linework, sketch, wall, space generation and film.
14. Each independent prompt has its own copy action, including the film prompt.
15. Five continuity locks are enabled by default.
16. Project JSON can be exported.
17. Workflow Markdown can be exported.
18. No external API is called during local prompt generation or copying.
19. README clearly states the boundary between the local workflow and third-party media generation.
20. README includes the five public workflow demonstration images.
