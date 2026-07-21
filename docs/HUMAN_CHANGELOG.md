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

After: the repository includes GitHub Actions CI, issue templates, `CONTRIBUTING.md`, `SECURITY.md`, and `docs/launch-posts.md`.

Risk: this is a mock starter kit, not a production image-generation backend. Real image providers and external uploads are intentionally blocked until a future explicit approval gate is implemented.

## 2026-07-21 - README conversion rewrite

Type: documentation and launch-positioning optimization.

Before: the README explained the project, but it still read like a normal technical README.

After: the README now follows a higher-conversion GitHub launch shape: screenshot-first hero, 30-second demo, clear use cases, safety-gate proof, agent-builder notes, comparison table, and direct star CTA.
