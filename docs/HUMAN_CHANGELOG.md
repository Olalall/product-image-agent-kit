# Human Changelog

## 2026-07-21 - Public starter rebuild

Type: new open-source project rebuild.

Before: the useful e-commerce image automation knowledge was split across local workflow projects and was not packaged as a clean GitHub-ready tool.

After: this project provides a sanitized, local-first product image agent demo with CSV input, source-image discovery, prompt planning, mock image generation, QA, reports, and a ZIP package.

User-visible result:

1. Run the demo without any API key.
2. Open `runs/demo/report.html` to see generated mock product-image cards.
3. Inspect `manifest.json`, `qa_report.json`, and `events.jsonl` to verify what happened.

## 2026-07-21 - README launch polish

Type: documentation and launch packaging.

Before: the project could run, but the GitHub landing page did not show the generated report visually.

After: `README.md` includes a demo screenshot from `docs/screenshots/report-demo.png`, the expected demo summary, and a short launch checklist.

## 2026-07-21 - GitHub community readiness

Type: open-source packaging.

Before: the repository had working code and docs, but lacked common GitHub contribution, security, issue-template, CI, and launch-copy files.

After: the repository includes issue templates, `CONTRIBUTING.md`, `SECURITY.md`, `docs/launch-posts.md`, and a GitHub Actions CI template under `docs/github-actions-ci.yml`.

Risk: this is a mock starter kit, not a production image-generation backend. Real image providers and external uploads are intentionally blocked until a future explicit approval gate is implemented.

## 2026-07-21 - README conversion rewrite

Type: documentation and launch-positioning optimization.

Before: the README explained the project, but it still read like a normal technical README.

After: the README now follows a higher-conversion GitHub launch shape: screenshot-first hero, 30-second demo, clear use cases, safety-gate proof, agent-builder notes, comparison table, and direct star CTA.

## 2026-07-21 - Post-publish README cleanup

Type: public page cleanup.

Before: after the first GitHub push, the README still contained a "Before publishing to GitHub" section.

After: the README now uses a public-facing "Share this project" section with a star CTA and launch-post pointer.

## 2026-07-21 - Chinese introduction and license clarification

Type: public communication polish.

Before: Chinese readers could misread GitHub's machine-translated "MIT license" as a Massachusetts Institute of Technology affiliation, and there was no ready-to-send Chinese introduction.

After: the repository includes `docs/project-introduction.zh-CN.md`, Chinese launch snippets, and an explicit README license clarification.

## 2026-07-21 - Chinese README and examples guide

Type: documentation and starter-template improvement.

Before: Chinese readers had a short introduction, but not a full quickstart README; examples were present but not explained in one place.

After: the repository includes `README.zh-CN.md`, `examples/README.md`, and a synthetic Shopify CSV template at `examples/templates/shopify-products.csv`.

## 2026-07-21 - JSON input adapter

Type: input compatibility improvement.

Before: the workflow only loaded product tasks from CSV files.

After: `--products` accepts both CSV and JSON inputs, with a synthetic `examples/products.json` sample and tests covering JSON runs.

## 2026-07-21 - Amazon image package template

Type: starter-template improvement.

Before: the examples included generic CSV/JSON inputs and a Shopify-oriented template, but no Amazon-oriented package planning template.

After: `examples/templates/amazon-image-package.csv` demonstrates synthetic main image, secondary feature image, and A+ banner planning slots without adding any Amazon upload behavior.
