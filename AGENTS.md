# AGENTS.md

## Project purpose

This is a public, sanitized, L2 open-source portfolio project extracted from local e-commerce image automation patterns.
It must stay easy to clone, run, inspect, and extend.

## Tech stack

- Python 3.11+
- Standard library only for the default demo
- `unittest` for tests
- CLI entrypoint: `product-image-agent` or `python -m product_image_agent.cli`

## Common commands

```powershell
python -m pip install -e .
python -m unittest discover -s tests
python -m product_image_agent.cli demo --out runs\demo
python -m product_image_agent.cli screenshot --report runs\demo\report.html --out docs\screenshots\report-demo.png
python -m product_image_agent.cli scan --products examples\products.csv --images examples\input-images
python -m product_image_agent.cli run --products examples\products.csv --images examples\input-images --out runs\manual
```

## Safety and privacy boundaries

- Do not add real API keys, tokens, cookies, Feishu/Base IDs, customer data, real order exports, or private product images.
- Default behavior must work in mock mode without paid API calls.
- Real providers, external upload, deletion, overwrite, or production queue access require explicit user approval and a code-level confirmation gate.
- Keep sample data synthetic and commercially neutral.

## Code conventions

- Prefer small modules with explicit dataclasses and JSON-serializable outputs.
- Keep the CLI stable and beginner-friendly.
- Every new behavior needs either a `unittest` or a deterministic demo artifact.
- Reports must keep the public summary fields: `found`, `generated`, `failed`, `moved`, `skipped`, `blocked`.

## Documentation conventions

- `README.md` is the GitHub landing page: problem, quickstart, screenshots/artifacts, and why to star.
- `docs/HUMAN_CHANGELOG.md` records non-developer-visible changes.
- `docs/architecture.md` records module boundaries and workflow shape.
