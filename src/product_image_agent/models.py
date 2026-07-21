from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class ProductTask:
    sku: str
    product_name: str
    category: str
    style: str
    output_count: int = 1
    target: str = "mock_only"
    requested_action: str = "generate_mock_images"
    source_image: str = ""
    notes: str = ""

    @classmethod
    def from_row(cls, row: dict[str, str]) -> "ProductTask":
        def text(key: str, default: str = "") -> str:
            return (row.get(key) or default).strip()

        try:
            output_count = int(text("output_count", "1"))
        except ValueError:
            output_count = 1
        return cls(
            sku=text("sku"),
            product_name=text("product_name"),
            category=text("category", "general"),
            style=text("style"),
            output_count=max(0, output_count),
            target=text("target", "mock_only"),
            requested_action=text("requested_action", "generate_mock_images"),
            source_image=text("source_image"),
            notes=text("notes"),
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ProductAsset:
    sku: str
    path: Path
    role: str = "product_reference"

    def to_dict(self) -> dict[str, Any]:
        return {"sku": self.sku, "path": str(self.path), "role": self.role}


@dataclass(frozen=True)
class PromptPlan:
    sku: str
    status: str
    image_prompt: str
    negative_prompt: str
    style_tags: list[str]
    output_count: int
    requires_human_approval: bool = False
    reason: str = ""
    safety_rules: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class GeneratedAsset:
    sku: str
    index: int
    path: Path
    kind: str = "mock_svg"

    def to_dict(self) -> dict[str, Any]:
        return {"sku": self.sku, "index": self.index, "path": str(self.path), "kind": self.kind}


@dataclass(frozen=True)
class QAItem:
    sku: str
    status: str
    checks: dict[str, bool]
    issues: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class RunSummary:
    found: int = 0
    generated: int = 0
    failed: int = 0
    moved: int = 0
    skipped: int = 0
    blocked: int = 0

    @property
    def status(self) -> str:
        if self.failed:
            return "fail"
        if self.blocked or self.skipped:
            return "warn"
        return "pass"

    def to_dict(self) -> dict[str, int | str]:
        return {
            "status": self.status,
            "found": self.found,
            "generated": self.generated,
            "failed": self.failed,
            "moved": self.moved,
            "skipped": self.skipped,
            "blocked": self.blocked,
        }
