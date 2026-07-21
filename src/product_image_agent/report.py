from __future__ import annotations

import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import GeneratedAsset, PromptPlan, QAItem, RunSummary


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def append_event(path: Path, event: str, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    row = {"ts": datetime.now(timezone.utc).isoformat(), "event": event, **payload}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_reports(
    out_dir: Path,
    summary: RunSummary,
    plans: list[PromptPlan],
    generated: list[GeneratedAsset],
    qa_items: list[QAItem],
    blocked: list[PromptPlan],
    failures: list[dict[str, str]],
) -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary.to_dict(),
        "plans": [item.to_dict() for item in plans],
        "generated_assets": [item.to_dict() for item in generated],
        "blocked": [item.to_dict() for item in blocked],
        "failures": failures,
    }
    qa_report = {"summary": summary.to_dict(), "items": [item.to_dict() for item in qa_items]}
    write_json(out_dir / "manifest.json", manifest)
    write_json(out_dir / "qa_report.json", qa_report)
    (out_dir / "report.md").write_text(render_markdown(summary, plans, generated, qa_items, blocked, failures), encoding="utf-8")
    (out_dir / "report.html").write_text(render_html(summary, generated, qa_items, blocked, failures), encoding="utf-8")
    package = package_outputs(out_dir)
    return {
        "manifest": str(out_dir / "manifest.json"),
        "qa_report": str(out_dir / "qa_report.json"),
        "report_md": str(out_dir / "report.md"),
        "report_html": str(out_dir / "report.html"),
        "package_zip": str(package),
    }


def package_outputs(out_dir: Path) -> Path:
    package = out_dir / "package.zip"
    with zipfile.ZipFile(package, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative_root in ["mock_outputs", "prompts", "manifest.json", "qa_report.json", "report.md", "report.html"]:
            path = out_dir / relative_root
            if path.is_file():
                archive.write(path, path.name)
            elif path.is_dir():
                for file in path.rglob("*"):
                    if file.is_file():
                        archive.write(file, file.relative_to(out_dir))
    return package


def render_markdown(summary: RunSummary, plans: list[PromptPlan], generated: list[GeneratedAsset], qa_items: list[QAItem], blocked: list[PromptPlan], failures: list[dict[str, str]]) -> str:
    lines = [
        "# Product Image Agent Run Report",
        "",
        f"Status: **{summary.status}**",
        "",
        "## Summary",
        "",
        "| found | generated | failed | moved | skipped | blocked |",
        "|---:|---:|---:|---:|---:|---:|",
        f"| {summary.found} | {summary.generated} | {summary.failed} | {summary.moved} | {summary.skipped} | {summary.blocked} |",
        "",
        "## Planned prompts",
    ]
    for plan in plans:
        lines.extend(["", f"### {plan.sku}", "", plan.image_prompt or plan.reason])
    if blocked:
        lines.extend(["", "## Blocked by safety gate"])
        for plan in blocked:
            lines.append(f"- `{plan.sku}`: {plan.reason}")
    if failures:
        lines.extend(["", "## Failures"])
        for failure in failures:
            lines.append(f"- `{failure.get('sku', 'unknown')}`: {failure.get('reason', '')}")
    lines.extend(["", "## QA"])
    for item in qa_items:
        issue_text = "; ".join(item.issues) if item.issues else "no issues"
        lines.append(f"- `{item.sku}`: {item.status} - {issue_text}")
    lines.extend(["", "## Generated assets"])
    for asset in generated:
        lines.append(f"- `{asset.sku}` image {asset.index}: `{asset.path}`")
    return "\n".join(lines) + "\n"


def render_html(summary: RunSummary, generated: list[GeneratedAsset], qa_items: list[QAItem], blocked: list[PromptPlan], failures: list[dict[str, str]]) -> str:
    cards = "\n".join(
        f'<article class="card"><h3>{asset.sku} / image {asset.index}</h3><img src="{asset.path.relative_to(asset.path.parents[2]).as_posix()}" alt="Mock output for {asset.sku}"></article>'
        for asset in generated
    )
    qa_rows = "\n".join(f"<tr><td>{item.sku}</td><td>{item.status}</td><td>{'; '.join(item.issues) or 'no issues'}</td></tr>" for item in qa_items)
    blocked_rows = "\n".join(f"<li><strong>{item.sku}</strong>: {item.reason}</li>" for item in blocked) or "<li>None</li>"
    failure_rows = "\n".join(f"<li><strong>{item.get('sku','unknown')}</strong>: {item.get('reason','')}</li>" for item in failures) or "<li>None</li>"
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Product Image Agent Run Report</title>
  <style>
    body {{ margin: 0; font-family: Inter, Segoe UI, Arial, sans-serif; background: #fff8f1; color: #181818; }}
    header {{ padding: 48px; background: linear-gradient(135deg, #111827, #7c2d12); color: white; }}
    main {{ padding: 32px 48px; }}
    .summary {{ display: grid; grid-template-columns: repeat(6, minmax(100px, 1fr)); gap: 12px; margin-top: 24px; }}
    .metric {{ background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.2); border-radius: 16px; padding: 16px; }}
    .metric b {{ display: block; font-size: 28px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; }}
    .card {{ background: white; border: 1px solid #ead8cb; border-radius: 20px; padding: 18px; box-shadow: 0 12px 30px rgba(80, 45, 20, .08); }}
    .card img {{ width: 100%; border-radius: 14px; border: 1px solid #eee; }}
    table {{ width: 100%; border-collapse: collapse; background: white; border-radius: 14px; overflow: hidden; }}
    th, td {{ text-align: left; padding: 12px 14px; border-bottom: 1px solid #eee; }}
    code {{ background: #fff; border: 1px solid #ead8cb; padding: 2px 6px; border-radius: 6px; }}
  </style>
</head>
<body>
  <header>
    <p>Local-first mock run</p>
    <h1>Product Image Agent Run Report</h1>
    <section class="summary">
      <div class="metric"><span>found</span><b>{summary.found}</b></div>
      <div class="metric"><span>generated</span><b>{summary.generated}</b></div>
      <div class="metric"><span>failed</span><b>{summary.failed}</b></div>
      <div class="metric"><span>moved</span><b>{summary.moved}</b></div>
      <div class="metric"><span>skipped</span><b>{summary.skipped}</b></div>
      <div class="metric"><span>blocked</span><b>{summary.blocked}</b></div>
    </section>
  </header>
  <main>
    <h2>Generated mock assets</h2>
    <section class="grid">{cards}</section>
    <h2>Safety gate</h2>
    <ul>{blocked_rows}</ul>
    <h2>Failures</h2>
    <ul>{failure_rows}</ul>
    <h2>QA report</h2>
    <table><thead><tr><th>SKU</th><th>Status</th><th>Issues</th></tr></thead><tbody>{qa_rows}</tbody></table>
  </main>
</body>
</html>
"""
