# v1.0 Acceptance

A build is accepted when:
1. `python app.py` starts with no third-party dependency.
2. `/api/health` returns version 1.0.0.
3. WebUI opens locally.
4. A hand sketch can be selected and previewed.
5. Six independent prompts are generated locally: line, linework, sketch, wall, space generation and film.
6. Each independent prompt has its own copy action, including the film prompt.
7. Five continuity locks are enabled by default.
8. Project JSON can be exported.
9. Workflow Markdown can be exported.
10. No external API is called during local prompt generation or copying.
11. README clearly states the boundary between the local workflow and third-party media generation.
