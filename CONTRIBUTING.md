# Contributing

Thanks for helping improve Product Image Agent Kit.

## Local setup

```powershell
python -m pip install -e .
python -m unittest discover -s tests
python -m product_image_agent.cli demo --clean --out runs\demo
```

## Contribution rules

- Keep the default workflow local-first and runnable without an API key.
- Use only synthetic sample data.
- Do not commit `.env`, credentials, customer data, real product exports, private marketplace data, or private product images.
- Add or update tests for behavior changes.
- Keep reports machine-readable: `manifest.json`, `qa_report.json`, and `events.jsonl` should remain stable.

## Good first issues

- Add a JSON input adapter.
- Add Shopify or Amazon CSV templates using synthetic data.
- Add more QA rules for copy claims, text density, aspect ratios, and source-image anchoring.
- Add screenshot automation for `report.html`.

## Real provider adapters

Real image providers are welcome, but they must be opt-in and guarded:

- no paid API calls by default;
- explicit cost-confirmation flag;
- clear provider readiness checks;
- no external upload, overwrite, delete, or publish without human approval.

The current code already includes the provider interface and a mock provider. Real providers should extend that interface without changing the default `mock` behavior.
