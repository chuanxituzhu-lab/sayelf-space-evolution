# v1.0 Acceptance

A build is accepted when:
1. `python app.py` starts with no third-party dependency.
2. `/api/health` returns version 1.0.0.
3. WebUI opens locally.
4. A hand sketch can be selected and previewed.
5. Five preset scenes are available for direct trial and can populate the project fields locally.
6. Six independent prompts are generated locally: line, linework, sketch, wall, space generation and film.
7. Each independent prompt has its own copy action, including the film prompt.
8. Five continuity locks are enabled by default.
9. Project JSON can be exported.
10. Workflow Markdown can be exported.
11. No external API is called during local prompt generation or copying.
12. README clearly states the boundary between the local workflow and third-party media generation.
