from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol

from .generator import generate_mock_assets
from .models import GeneratedAsset, ProductAsset, ProductTask, PromptPlan

MOCK_PROVIDER = "mock"
RESERVED_REAL_PROVIDERS = {"openai"}
SUPPORTED_PROVIDERS = {MOCK_PROVIDER, *RESERVED_REAL_PROVIDERS}


@dataclass(frozen=True)
class ProviderReadiness:
    provider: str
    status: str
    reason: str = ""
    requires_confirm_cost: bool = False

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


class ImageProvider(Protocol):
    name: str

    def generate(
        self,
        task: ProductTask,
        asset: ProductAsset,
        plan: PromptPlan,
        output_dir: Path,
    ) -> list[GeneratedAsset]:
        """Generate product image assets for one planned task."""


class MockImageProvider:
    name = MOCK_PROVIDER

    def generate(
        self,
        task: ProductTask,
        asset: ProductAsset,
        plan: PromptPlan,
        output_dir: Path,
    ) -> list[GeneratedAsset]:
        return generate_mock_assets(task, asset, plan, output_dir)


def check_provider_readiness(provider_name: str, confirm_cost: bool = False) -> ProviderReadiness:
    normalized = provider_name.strip().lower()
    if normalized not in SUPPORTED_PROVIDERS:
        return ProviderReadiness(provider=normalized, status="fail", reason=f"Unsupported provider: {provider_name}")
    if normalized == MOCK_PROVIDER:
        return ProviderReadiness(provider=normalized, status="pass")
    if normalized in RESERVED_REAL_PROVIDERS and not confirm_cost:
        return ProviderReadiness(
            provider=normalized,
            status="blocked",
            reason=f"Provider '{normalized}' is reserved for a future real adapter and requires --confirm-cost before it can run.",
            requires_confirm_cost=True,
        )
    return ProviderReadiness(
        provider=normalized,
        status="blocked",
        reason=f"Provider '{normalized}' passed the cost-confirmation gate, but the real adapter is not implemented yet.",
        requires_confirm_cost=True,
    )


def get_provider(provider_name: str) -> ImageProvider:
    normalized = provider_name.strip().lower()
    if normalized == MOCK_PROVIDER:
        return MockImageProvider()
    raise ValueError(f"Provider '{provider_name}' is not executable in this mock-first release.")
