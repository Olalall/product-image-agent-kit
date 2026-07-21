from __future__ import annotations

import csv
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from product_image_agent.pipeline import run_pipeline  # noqa: E402
from product_image_agent.planner import build_prompt_plan  # noqa: E402
from product_image_agent.scanner import load_products, scan_inputs  # noqa: E402
from product_image_agent.screenshot import build_screenshot_command  # noqa: E402


class ProductImageAgentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp)

    def test_load_products_reads_example_csv(self) -> None:
        tasks = load_products(PROJECT_ROOT / "examples" / "products.csv")
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0].sku, "DEMO-LAMP-01")

    def test_load_products_reads_example_json(self) -> None:
        tasks = load_products(PROJECT_ROOT / "examples" / "products.json")
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].sku, "DEMO-LAMP-01")
        self.assertEqual(tasks[0].output_count, 2)

    def test_scan_reports_ready_inputs(self) -> None:
        result = scan_inputs(PROJECT_ROOT / "examples" / "products.csv", PROJECT_ROOT / "examples" / "input-images")
        self.assertEqual(result["product_count"], 3)
        self.assertEqual(result["asset_count"], 3)
        self.assertEqual(result["missing_images"], [])

    def test_shopify_template_uses_canonical_required_columns(self) -> None:
        tasks = load_products(PROJECT_ROOT / "examples" / "templates" / "shopify-products.csv")
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].sku, "DEMO-LAMP-01")
        self.assertEqual(tasks[0].target, "mock_only")

    def test_amazon_template_uses_canonical_required_columns(self) -> None:
        tasks = load_products(PROJECT_ROOT / "examples" / "templates" / "amazon-image-package.csv")
        self.assertEqual(len(tasks), 4)
        self.assertEqual(tasks[0].sku, "DEMO-LAMP-01")
        self.assertEqual(tasks[0].target, "mock_only")
        self.assertEqual(tasks[0].output_count, 1)

    def test_external_publish_is_blocked(self) -> None:
        task = load_products(PROJECT_ROOT / "examples" / "products.csv")[2]
        plan = build_prompt_plan(task)
        self.assertEqual(plan.status, "blocked")
        self.assertTrue(plan.requires_human_approval)

    def test_pipeline_writes_reports_and_package(self) -> None:
        result = run_pipeline(PROJECT_ROOT / "examples" / "products.csv", PROJECT_ROOT / "examples" / "input-images", self.tmp / "run")
        summary = result["summary"]
        self.assertEqual(summary["found"], 3)
        self.assertEqual(summary["generated"], 3)
        self.assertEqual(summary["failed"], 0)
        self.assertEqual(summary["blocked"], 1)
        self.assertTrue((self.tmp / "run" / "report.html").exists())
        self.assertTrue((self.tmp / "run" / "manifest.json").exists())
        self.assertTrue((self.tmp / "run" / "qa_report.json").exists())
        self.assertTrue((self.tmp / "run" / "package.zip").exists())
        manifest = json.loads((self.tmp / "run" / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["generated_assets"]), 3)
        events = (self.tmp / "run" / "events.jsonl").read_text(encoding="utf-8")
        self.assertIn("run_started", events)
        self.assertIn("run_finished", events)

    def test_pipeline_accepts_json_products(self) -> None:
        result = run_pipeline(PROJECT_ROOT / "examples" / "products.json", PROJECT_ROOT / "examples" / "input-images", self.tmp / "json-run")
        summary = result["summary"]
        self.assertEqual(summary["found"], 2)
        self.assertEqual(summary["generated"], 3)
        self.assertEqual(summary["failed"], 0)
        self.assertEqual(summary["blocked"], 0)

    def test_pipeline_accepts_amazon_template(self) -> None:
        result = run_pipeline(PROJECT_ROOT / "examples" / "templates" / "amazon-image-package.csv", PROJECT_ROOT / "examples" / "input-images", self.tmp / "amazon-run")
        summary = result["summary"]
        self.assertEqual(summary["found"], 4)
        self.assertEqual(summary["generated"], 6)
        self.assertEqual(summary["failed"], 0)
        self.assertEqual(summary["blocked"], 0)

    def test_missing_required_csv_column_fails_fast(self) -> None:
        products = self.tmp / "bad.csv"
        with products.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["sku", "product_name"])
            writer.writeheader()
            writer.writerow({"sku": "A", "product_name": "Missing style"})
        with self.assertRaises(ValueError):
            load_products(products)

    def test_invalid_json_shape_fails_fast(self) -> None:
        products = self.tmp / "bad.json"
        products.write_text(json.dumps({"items": []}), encoding="utf-8")
        with self.assertRaises(ValueError):
            load_products(products)

    def test_screenshot_command_uses_file_uri_and_output_path(self) -> None:
        report = self.tmp / "report.html"
        output = self.tmp / "report.png"
        report.write_text("<html><body>demo</body></html>", encoding="utf-8")
        command = build_screenshot_command("chrome", report, output, window_size="1000,800")
        self.assertEqual(command[0], "chrome")
        self.assertIn("--headless", command)
        self.assertIn("--window-size=1000,800", command)
        self.assertIn(f"--screenshot={output.resolve()}", command)
        self.assertEqual(command[-1], report.resolve().as_uri())


if __name__ == "__main__":
    unittest.main()
