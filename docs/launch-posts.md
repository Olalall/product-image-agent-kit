# Launch Posts

## Core positioning

Tagline:

```text
Local-first AI product image workflow toolkit with mock generation, QA reports, and approval gates.
```

One-liner:

```text
Product Image Agent Kit helps e-commerce automation builders test the full product-image workflow before connecting paid image APIs or live stores.
```

## X / LinkedIn

```text
I just open-sourced Product Image Agent Kit.

Most AI image demos stop at "generate an image". Real e-commerce workflows need the boring parts too:

- CSV/SKU input checks
- prompt planning
- mock image outputs without API keys
- QA reports
- event logs
- package.zip
- human approval gate for live upload/publish actions

Built for e-commerce operators and AI automation builders who want a safe mock-to-production starter.
```

## Hacker News - Show HN

Title:

```text
Show HN: Product Image Agent Kit - local-first AI workflow for e-commerce images
```

Body:

```text
I built a small Python starter kit for product-image automation workflows.

It reads a product CSV and source images, creates prompt plans, generates deterministic mock SVG outputs, runs QA checks, and writes report.html, manifest.json, qa_report.json, events.jsonl, and package.zip.

The default workflow is local-first and does not require an API key. Live publish/upload actions are intentionally blocked by a human approval gate.

I built it because many AI image automation demos skip the operational parts: input validation, audit logs, QA, packages, and safety gates.
```

## Reddit

```text
I made a local-first product image automation starter kit.

It is not another chatbot demo. It focuses on the operational workflow around AI image generation:

- product CSV + source-image scan
- prompt planning
- mock generation without API keys
- QA report
- event log
- package.zip
- human approval gate for live upload/publish actions

Looking for feedback from people building e-commerce or image-generation automations.
```

## GitHub About text

```text
Local-first AI product image workflow toolkit with mock generation, QA reports, and approval gates.
```

## GitHub topics

```text
ai-agents ecommerce image-generation workflow-automation product-images mock-first qa-report python cli
```

## Regenerate launch screenshot

```powershell
python -m product_image_agent.cli demo --clean --out runs\demo
python -m product_image_agent.cli screenshot --report runs\demo\report.html --out docs\screenshots\report-demo.png
```

## Chinese short intro

```text
我做了一个电商商品图 AI 自动化工具包。它不是单纯“让 AI 画图”，而是把商品图生产前后的流程也做进去：表格检查、素材匹配、prompt 规划、mock 输出、质检报告、日志、打包，以及上传/发布前的安全拦截。
```

## Chinese technical intro

```text
Product Image Agent Kit 是一个 local-first 的 AI workflow starter kit。输入 products.csv 和商品素材图后，它会完成 source-image scan、prompt planning、mock image generation、QA check、event logging，并输出 report.html、manifest.json、qa_report.json、events.jsonl 和 package.zip。默认 mock-first，不调用付费 API；遇到 live publish、upload、overwrite、delete 等动作时，会进入 human approval gate。
```
