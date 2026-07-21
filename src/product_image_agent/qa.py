from __future__ import annotations

from .models import GeneratedAsset, ProductTask, QAItem

BANNED_COPY_TERMS = {"#1", "guaranteed", "cure", "medical", "permanent", "free money", "official amazon"}


def qa_task(task: ProductTask, generated: list[GeneratedAsset]) -> QAItem:
    issues: list[str] = []
    checks = {
        "has_sku": bool(task.sku),
        "has_product_name": bool(task.product_name),
        "has_outputs": bool(generated),
        "output_count_matches": len(generated) == task.output_count,
        "copy_terms_safe": True,
    }
    searchable = " ".join([task.product_name, task.style, task.notes]).lower()
    banned = sorted(term for term in BANNED_COPY_TERMS if term in searchable)
    if banned:
        checks["copy_terms_safe"] = False
        issues.append("Banned or risky copy terms: " + ", ".join(banned))
    for name, passed in checks.items():
        if not passed and name != "copy_terms_safe":
            issues.append(f"Check failed: {name}")
    return QAItem(sku=task.sku or "unknown", status="pass" if all(checks.values()) else "warn", checks=checks, issues=issues)
