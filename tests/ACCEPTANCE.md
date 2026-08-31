# v1.0 Acceptance

A build is accepted when:
1. `python app.py` starts with no third-party dependency.
2. `/api/health` returns version 1.0.0.
3. WebUI opens locally.
4. A hand sketch can be selected and previewed.
5. Six stage prompts are generated locally: line, linework, sketch, wall, space generation and film.
6. Five continuity locks are enabled by default.
7. Project JSON can be exported.
8. Workflow Markdown can be exported.
9. No external API is called during local prompt generation.
10. README clearly states the boundary between the local workflow and third-party media generation.
