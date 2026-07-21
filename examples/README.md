# Examples

This folder contains synthetic data for the default no-key demo.

## Files

```text
examples/
  products.csv
  input-images/
    DEMO-LAMP-01.svg
    DEMO-BAG-02.svg
    DEMO-LIVE-03.svg
  templates/
    shopify-products.csv
```

## `products.csv` columns

| Column | Required | Meaning |
|---|---:|---|
| `sku` | Yes | Product SKU. Also used to match source images. |
| `product_name` | Yes | Human-readable product name. |
| `category` | No | Product category used in prompt planning. |
| `style` | Yes | Visual style direction for product-image generation. |
| `output_count` | No | Number of mock outputs to generate. |
| `target` | No | Destination mode. Use `mock_only` for safe local runs. |
| `requested_action` | No | Intended action. Live publish/upload actions are blocked. |
| `source_image` | No | Expected source image filename. |
| `notes` | No | Operator notes for prompt planning and QA context. |

## Demo rows

The default demo contains three rows:

1. `DEMO-LAMP-01`: safe mock task, generates two SVG outputs.
2. `DEMO-BAG-02`: safe mock task, generates one SVG output.
3. `DEMO-LIVE-03`: intentionally blocked because it requests `shopify_live` + `publish_listing`.

That is why the expected demo summary is:

```text
found=3 generated=3 failed=0 moved=3 skipped=1 blocked=1
```

`blocked=1` is a feature, not a bug. It proves the human approval gate is working.

## Replace with your own mock data

1. Copy `examples/products.csv` to a new file.
2. Replace the SKU, product name, category, style, and notes.
3. Add a synthetic source image under `examples/input-images/`.
4. Name the source image with the SKU, for example:

```text
MY-SKU-001.svg
```

5. Run:

```powershell
python -m product_image_agent.cli run --products examples\products.csv --images examples\input-images --out runs\manual --clean
```

## Output artifacts

After a run, inspect:

```text
runs/manual/report.html
runs/manual/manifest.json
runs/manual/qa_report.json
runs/manual/events.jsonl
runs/manual/package.zip
```

Use `report.html` for human review and the JSON/JSONL files for agent or automation handoff.
