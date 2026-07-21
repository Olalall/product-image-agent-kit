from __future__ import annotations

from .models import ProductTask, PromptPlan
from .scanner import validate_task_fields

HIGH_RISK_TARGETS = {"external_upload", "feishu_live", "shopify_live", "amazon_live", "production"}
HIGH_RISK_ACTIONS = {"upload_to_external_system", "overwrite_live_assets", "delete_source_assets", "publish_listing"}


def build_prompt_plan(task: ProductTask) -> PromptPlan:
    missing = validate_task_fields(task)
    if missing:
        return PromptPlan(
            sku=task.sku or "unknown",
            status="failed",
            image_prompt="",
            negative_prompt="",
            style_tags=[],
            output_count=0,
            reason="Missing required fields: " + ", ".join(missing),
            safety_rules=default_safety_rules(),
        )

    high_risk = task.target in HIGH_RISK_TARGETS or task.requested_action in HIGH_RISK_ACTIONS
    if high_risk:
        return PromptPlan(
            sku=task.sku,
            status="blocked",
            image_prompt="",
            negative_prompt="",
            style_tags=style_tags(task),
            output_count=0,
            requires_human_approval=True,
            reason="External write/publish action requires explicit human approval.",
            safety_rules=default_safety_rules(),
        )

    return PromptPlan(
        sku=task.sku,
        status="planned",
        image_prompt=render_image_prompt(task),
        negative_prompt="no fake logos, no medical claims, no marketplace badges, no unreadable text, no distorted product shape",
        style_tags=style_tags(task),
        output_count=task.output_count,
        safety_rules=default_safety_rules(),
    )


def style_tags(task: ProductTask) -> list[str]:
    raw = [task.category, *task.style.replace("，", ",").split(",")]
    return [item.strip().lower().replace(" ", "-") for item in raw if item.strip()]


def render_image_prompt(task: ProductTask) -> str:
    return (
        f"Create a clean e-commerce product image for SKU {task.sku}. "
        f"Product: {task.product_name}. Category: {task.category}. "
        f"Style direction: {task.style}. "
        "Use the source product image as the visual anchor. Keep the product recognizable, centered, and commercially neutral. "
        "Use realistic lighting, readable composition, no invented brand logos, and no unsupported claims. "
        f"Operator notes: {task.notes or 'none'}."
    )


def default_safety_rules() -> list[str]:
    return [
        "Mock mode is the default and does not call paid APIs.",
        "External upload, overwrite, delete, or publish actions must be blocked until a human confirms them.",
        "Prompts must preserve the source product as the visual anchor.",
        "Generated copy must avoid fake marketplace badges, medical claims, and unverifiable superlatives.",
    ]
