from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .models import ProductAsset, ProductTask

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".svg"}
REQUIRED_COLUMNS = {"sku", "product_name", "style"}


def load_products(products_path: Path) -> list[ProductTask]:
    if not products_path.exists():
        raise FileNotFoundError(f"Product input not found: {products_path}")
    if products_path.suffix.lower() == ".json":
        return load_products_json(products_path)
    return load_products_csv(products_path)


def load_products_csv(products_csv: Path) -> list[ProductTask]:
    with products_csv.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = REQUIRED_COLUMNS - columns
        if missing:
            raise ValueError(f"Product CSV is missing required columns: {', '.join(sorted(missing))}")
        return [ProductTask.from_row(row) for row in reader]


def load_products_json(products_json: Path) -> list[ProductTask]:
    payload = json.loads(products_json.read_text(encoding="utf-8"))
    rows = extract_product_rows(payload)
    return [ProductTask.from_row(row) for row in rows]


def extract_product_rows(payload: Any) -> list[dict[str, object]]:
    if isinstance(payload, list):
        rows = payload
    elif isinstance(payload, dict) and isinstance(payload.get("products"), list):
        rows = payload["products"]
    else:
        raise ValueError("Product JSON must be a list of product objects or an object with a 'products' list.")
    invalid_indexes = [str(index) for index, row in enumerate(rows) if not isinstance(row, dict)]
    if invalid_indexes:
        raise ValueError("Product JSON rows must be objects. Invalid indexes: " + ", ".join(invalid_indexes))
    return rows


def discover_assets(images_dir: Path) -> dict[str, ProductAsset]:
    if not images_dir.exists():
        raise FileNotFoundError(f"Image folder not found: {images_dir}")
    assets: dict[str, ProductAsset] = {}
    for path in sorted(images_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES:
            sku = path.stem.split("__", 1)[0]
            assets.setdefault(sku, ProductAsset(sku=sku, path=path))
    return assets


def scan_inputs(products_csv: Path, images_dir: Path) -> dict[str, object]:
    tasks = load_products(products_csv)
    assets = discover_assets(images_dir)
    ready: list[str] = []
    missing_images: list[str] = []
    invalid_tasks: list[dict[str, str]] = []
    for task in tasks:
        missing_fields = validate_task_fields(task)
        if missing_fields:
            invalid_tasks.append({"sku": task.sku, "reason": "missing " + ", ".join(missing_fields)})
            continue
        if task.sku not in assets:
            missing_images.append(task.sku)
            continue
        ready.append(task.sku)
    return {
        "status": "pass" if len(ready) == len(tasks) else "warn",
        "product_count": len(tasks),
        "asset_count": len(assets),
        "ready": ready,
        "missing_images": missing_images,
        "invalid_tasks": invalid_tasks,
    }


def validate_task_fields(task: ProductTask) -> list[str]:
    missing: list[str] = []
    if not task.sku:
        missing.append("sku")
    if not task.product_name:
        missing.append("product_name")
    if not task.style:
        missing.append("style")
    if task.output_count < 1:
        missing.append("output_count")
    return missing
