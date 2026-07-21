from __future__ import annotations

from pathlib import Path

from .models import GeneratedAsset, PromptPlan, QAItem, RunSummary
from .planner import build_prompt_plan
from .providers import check_provider_readiness, get_provider
from .qa import qa_task
from .report import append_event, write_reports
from .scanner import discover_assets, load_products


def run_pipeline(
    products_csv: Path,
    images_dir: Path,
    out_dir: Path,
    provider_name: str = "mock",
    confirm_cost: bool = False,
) -> dict[str, object]:
    tasks = load_products(products_csv)
    assets = discover_assets(images_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    events_path = out_dir / "events.jsonl"
    if events_path.exists():
        events_path.unlink()
    provider_readiness = check_provider_readiness(provider_name, confirm_cost=confirm_cost)
    append_event(
        events_path,
        "run_started",
        {
            "products": str(products_csv),
            "images": str(images_dir),
            "out": str(out_dir),
            "provider": provider_readiness.to_dict(),
        },
    )

    summary = RunSummary(found=len(tasks))
    plans: list[PromptPlan] = []
    blocked: list[PromptPlan] = []
    generated: list[GeneratedAsset] = []
    qa_items: list[QAItem] = []
    failures: list[dict[str, str]] = []
    if provider_readiness.status != "pass":
        if provider_readiness.status == "blocked":
            summary.blocked = len(tasks)
            summary.skipped = len(tasks)
            failures = []
        else:
            summary.failed = len(tasks)
            failures = [{"sku": "provider", "reason": provider_readiness.reason}]
        artifacts = write_reports(out_dir, summary, plans, generated, qa_items, blocked, failures)
        append_event(events_path, "provider_blocked", {"provider": provider_readiness.to_dict()})
        append_event(events_path, "run_finished", {"summary": summary.to_dict(), "artifacts": artifacts})
        return {"summary": summary.to_dict(), "provider": provider_readiness.to_dict(), "artifacts": artifacts, "events": str(events_path)}

    provider = get_provider(provider_readiness.provider)

    for task in tasks:
        plan = build_prompt_plan(task)
        append_event(events_path, "plan_created", {"sku": plan.sku, "status": plan.status, "reason": plan.reason})
        if plan.status == "failed":
            summary.failed += 1
            failures.append({"sku": plan.sku, "reason": plan.reason})
            continue
        if plan.status == "blocked":
            summary.blocked += 1
            summary.skipped += 1
            blocked.append(plan)
            continue
        asset = assets.get(task.sku)
        if asset is None:
            summary.failed += 1
            reason = "Missing source product image. Add a file named <SKU>.svg/.png/.jpg under the images folder."
            failures.append({"sku": task.sku, "reason": reason})
            append_event(events_path, "task_failed", {"sku": task.sku, "reason": reason})
            continue
        plans.append(plan)
        outputs = provider.generate(task, asset, plan, out_dir)
        generated.extend(outputs)
        summary.generated += len(outputs)
        summary.moved += len(outputs)
        qa_item = qa_task(task, outputs)
        qa_items.append(qa_item)
        if qa_item.status != "pass":
            append_event(events_path, "qa_warned", {"sku": task.sku, "issues": qa_item.issues})
        append_event(events_path, "task_generated", {"sku": task.sku, "count": len(outputs)})

    artifacts = write_reports(out_dir, summary, plans, generated, qa_items, blocked, failures)
    append_event(events_path, "run_finished", {"summary": summary.to_dict(), "artifacts": artifacts})
    return {"summary": summary.to_dict(), "provider": provider_readiness.to_dict(), "artifacts": artifacts, "events": str(events_path)}
