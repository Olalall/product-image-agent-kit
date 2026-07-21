from __future__ import annotations

import html
from pathlib import Path

from .models import GeneratedAsset, ProductAsset, ProductTask, PromptPlan


def generate_mock_assets(task: ProductTask, asset: ProductAsset, plan: PromptPlan, output_dir: Path) -> list[GeneratedAsset]:
    sku_dir = output_dir / "mock_outputs" / task.sku
    sku_dir.mkdir(parents=True, exist_ok=True)
    generated: list[GeneratedAsset] = []
    for index in range(1, plan.output_count + 1):
        path = sku_dir / f"image_{index}.svg"
        path.write_text(render_mock_svg(task, asset, index), encoding="utf-8")
        generated.append(GeneratedAsset(sku=task.sku, index=index, path=path))
    prompt_path = output_dir / "prompts" / f"{task.sku}.txt"
    prompt_path.parent.mkdir(parents=True, exist_ok=True)
    prompt_path.write_text(plan.image_prompt + "\n\nNegative prompt: " + plan.negative_prompt + "\n", encoding="utf-8")
    return generated


def render_mock_svg(task: ProductTask, asset: ProductAsset, index: int) -> str:
    safe_name = html.escape(task.product_name)
    safe_sku = html.escape(task.sku)
    safe_style = html.escape(task.style)
    safe_asset = html.escape(asset.path.name)
    palette = ["#f8efe7", "#eef4ff", "#edf8f1", "#fff8dc"]
    accent = ["#b85e6a", "#4c6fff", "#358a59", "#b8860b"][index % 4]
    background = palette[index % len(palette)]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="900" viewBox="0 0 1200 900" role="img" aria-label="Mock product image for {safe_sku}">
  <rect width="1200" height="900" fill="{background}"/>
  <circle cx="960" cy="150" r="120" fill="{accent}" opacity="0.14"/>
  <circle cx="180" cy="750" r="180" fill="{accent}" opacity="0.10"/>
  <rect x="130" y="120" width="940" height="660" rx="46" fill="#fffdfb" stroke="#ead8cb" stroke-width="4"/>
  <rect x="215" y="210" width="360" height="430" rx="34" fill="#ffffff" stroke="{accent}" stroke-width="10"/>
  <rect x="255" y="260" width="280" height="260" rx="28" fill="{background}" stroke="#ddc9bc" stroke-width="3"/>
  <text x="395" y="410" text-anchor="middle" font-family="Arial, sans-serif" font-size="38" font-weight="700" fill="#222">SOURCE</text>
  <text x="395" y="458" text-anchor="middle" font-family="Arial, sans-serif" font-size="22" fill="#766">{safe_asset}</text>
  <text x="635" y="285" font-family="Arial, sans-serif" font-size="34" font-weight="700" fill="#181818">{safe_name}</text>
  <text x="635" y="340" font-family="Arial, sans-serif" font-size="24" fill="#5d514c">SKU {safe_sku}</text>
  <text x="635" y="395" font-family="Arial, sans-serif" font-size="24" fill="#5d514c">Style: {safe_style}</text>
  <rect x="635" y="455" width="315" height="58" rx="29" fill="{accent}" opacity="0.92"/>
  <text x="792" y="493" text-anchor="middle" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#fff">MOCK OUTPUT {index}</text>
  <text x="635" y="575" font-family="Arial, sans-serif" font-size="21" fill="#554944">No paid API call. Replace this SVG with a real provider adapter when ready.</text>
  <text x="635" y="615" font-family="Arial, sans-serif" font-size="21" fill="#554944">Safety: product anchor preserved, no fake logos, no unsupported claims.</text>
</svg>
"""
