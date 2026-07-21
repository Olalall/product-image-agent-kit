from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from .pipeline import run_pipeline
from .scanner import scan_inputs

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PRODUCTS = PROJECT_ROOT / "examples" / "products.csv"
DEFAULT_IMAGES = PROJECT_ROOT / "examples" / "input-images"


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    if args.command == "demo":
        if args.clean and args.out.exists():
            shutil.rmtree(args.out)
        result = run_pipeline(DEFAULT_PRODUCTS, DEFAULT_IMAGES, args.out)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    if args.command == "scan":
        result = scan_inputs(args.products, args.images)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return
    if args.command == "run":
        if args.clean and args.out.exists():
            shutil.rmtree(args.out)
        result = run_pipeline(args.products, args.images, args.out)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        summary = result["summary"]
        if isinstance(summary, dict) and summary.get("status") == "fail":
            raise SystemExit(1)
        return
    raise SystemExit("Missing command. Use --help.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="product-image-agent")
    sub = parser.add_subparsers(dest="command")

    demo = sub.add_parser("demo", help="Run the built-in no-key mock workflow.")
    demo.add_argument("--out", type=Path, default=Path("runs/demo"))
    demo.add_argument("--clean", action="store_true", help="Delete the selected output folder before running.")

    scan = sub.add_parser("scan", help="Validate product rows and source image availability.")
    scan.add_argument("--products", type=Path, required=True)
    scan.add_argument("--images", type=Path, required=True)

    run = sub.add_parser("run", help="Run prompt planning, mock generation, QA, and packaging.")
    run.add_argument("--products", type=Path, required=True)
    run.add_argument("--images", type=Path, required=True)
    run.add_argument("--out", type=Path, default=Path("runs/manual"))
    run.add_argument("--clean", action="store_true", help="Delete the selected output folder before running.")
    return parser


if __name__ == "__main__":
    main()
