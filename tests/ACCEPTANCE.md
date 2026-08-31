# v1.0 Acceptance

A build is accepted when:
1. `python app.py` starts with no third-party dependency.
2. `/api/health` returns version 1.0.0.
3. WebUI opens locally.
4. A hand sketch can be selected and previewed.
5. Five preset scenes are available for direct trial and can populate the project fields locally.
6. Space style options include modern minimal, American, French, wabi-sabi, simplified Chinese and Chinese styles.
7. Changing style changes the visual direction text without changing the six-stage workflow.
8. Six independent prompts are generated locally: line, linework, sketch, wall, space generation and film.
9. Each independent prompt has its own copy action, including the film prompt.
10. Five continuity locks are enabled by default.
11. Project JSON can be exported.
12. Workflow Markdown can be exported.
13. No external API is called during local prompt generation or copying.
14. README clearly states the boundary between the local workflow and third-party media generation.
