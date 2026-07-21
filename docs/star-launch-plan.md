# GitHub Star Launch Plan

## Positioning

Use this tagline:

> Local-first AI product image workflow toolkit with mock generation, QA reports, and safe human approval gates.

## First launch checklist

- Add a real repository URL to the badges in `README.md` after creating the GitHub repo.
- Run `python -m unittest discover -s tests`.
- Run `python -m pip install -e .`, then `python -m product_image_agent.cli demo --clean --out runs/demo`.
- Capture a screenshot of `runs/demo/report.html` and place it under `docs/screenshots/report-demo.png`.
- Add GitHub topics: `ai-agents`, `ecommerce`, `image-generation`, `workflow-automation`, `product-images`, `mock-first`, `qa-report`.

## Where to post

- GitHub repository README
- Hacker News: Show HN
- Reddit: r/LocalLLaMA, r/Python, r/ecommerce
- X / LinkedIn with the report screenshot

## Good first issues

- Add a JSON input adapter.
- Add a Shopify CSV template.
- Add real-provider adapter interface with cost-confirmation gate.
- Add screenshot automation for `report.html`.
