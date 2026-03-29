from __future__ import annotations

import uuid
from dataclasses import dataclass


@dataclass
class EbayItemPayload:
    ebay_item_id: str
    title: str
    category: str
    status: str
    price: float
    currency: str
    quantity: int


@dataclass
class EbayListingPayload:
    title: str
    category: str
    price: float
    currency: str
    quantity: int


@dataclass
class EbayListingResult:
    ebay_item_id: str
    status: str


class EbayClient:
    def __init__(
        self,
        use_mock: bool = True,
        client_id: str = "",
        client_secret: str = "",
        refresh_token: str = "",
        marketplace_id: str = "EBAY_US",
    ):
        self.use_mock = use_mock
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.marketplace_id = marketplace_id

    def fetch_items(self) -> list[EbayItemPayload]:
        if self.use_mock:
            return self._mock_items()
        # Placeholder for real OAuth + Inventory API integration.
        # For prototype purposes, return empty list when not mocked.
        return []

    def create_listing(self, payload: EbayListingPayload) -> EbayListingResult:
        if self.use_mock:
            suffix = uuid.uuid4().hex[:10]
            return EbayListingResult(ebay_item_id=f"MOCK-{suffix}", status="active")
        # Placeholder for real listing API call.
        suffix = uuid.uuid4().hex[:10]
        return EbayListingResult(ebay_item_id=f"PENDING-{suffix}", status="active")

    @staticmethod
    def _mock_items() -> list[EbayItemPayload]:
        return [
            EbayItemPayload(
                ebay_item_id="10001",
                title="Nike Air Max 90 - Men's Size 10",
                category="Shoes",
                status="active",
                price=92.0,
                currency="USD",
                quantity=1,
            ),
            EbayItemPayload(
                ebay_item_id="10002",
                title="Apple iPhone 12 - 128GB Black",
                category="Cell Phones & Smartphones",
                status="sold",
                price=330.0,
                currency="USD",
                quantity=1,
            ),
            EbayItemPayload(
                ebay_item_id="10003",
                title="Vintage Levi's 501 Jeans 34x32",
                category="Clothing",
                status="cancelled",
                price=45.0,
                currency="USD",
                quantity=1,
            ),
            EbayItemPayload(
                ebay_item_id="10004",
                title="Nike Air Max 90 - Men's Size 9",
                category="Shoes",
                status="sold",
                price=88.0,
                currency="USD",
                quantity=1,
            ),
        ]
