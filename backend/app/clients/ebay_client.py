from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass
from typing import Any

import httpx


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


logger = logging.getLogger(__name__)


class EbayClient:
    def __init__(
        self,
        use_mock: bool = True,
        client_id: str = "",
        client_secret: str = "",
        refresh_token: str = "",
        access_token: str = "",
        environment: str = "sandbox",
        marketplace_id: str = "EBAY_US",
    ):
        self.use_mock = use_mock
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self.access_token = access_token
        self.environment = environment.lower()
        self.marketplace_id = marketplace_id

    def fetch_items(self) -> list[EbayItemPayload]:
        if self.use_mock:
            return self._mock_items()

        if not self.access_token:
            logger.warning("EBAY_ACCESS_TOKEN is missing; returning empty item list.")
            return []

        try:
            offers = self._fetch_offer_items()
            sold_items = self._fetch_sold_items()
            merged = offers + sold_items
            deduped: dict[str, EbayItemPayload] = {}
            for item in merged:
                deduped[item.ebay_item_id] = item
            return list(deduped.values())
        except Exception:
            logger.exception("Failed to fetch sandbox items from eBay API")
            return []

    def create_listing(self, payload: EbayListingPayload) -> EbayListingResult:
        if self.use_mock:
            suffix = uuid.uuid4().hex[:10]
            return EbayListingResult(ebay_item_id=f"MOCK-{suffix}", status="active")
        # Placeholder for real listing API call.
        suffix = uuid.uuid4().hex[:10]
        return EbayListingResult(ebay_item_id=f"PENDING-{suffix}", status="active")

    def _fetch_offer_items(self) -> list[EbayItemPayload]:
        data = self._get("/sell/inventory/v1/offer", params={"limit": 200})
        offers = data.get("offers", [])
        items: list[EbayItemPayload] = []

        for offer in offers:
            offer_id = str(offer.get("offerId") or offer.get("listingId") or "")
            if not offer_id:
                continue

            status = str(offer.get("status", "")).upper()
            mapped_status = "active" if status in {"PUBLISHED", "ACTIVE"} else "cancelled"

            price_obj = offer.get("pricingSummary", {}).get("price", {})
            price = float(price_obj.get("value") or 0.0)
            currency = str(price_obj.get("currency") or "USD")
            quantity = int(offer.get("availableQuantity") or 1)
            category = str(offer.get("categoryId") or "Unknown")
            title = str(
                offer.get("listingDescription")
                or offer.get("merchantLocationKey")
                or f"Offer {offer_id}"
            )

            items.append(
                EbayItemPayload(
                    ebay_item_id=f"offer-{offer_id}",
                    title=title,
                    category=category,
                    status=mapped_status,
                    price=price,
                    currency=currency,
                    quantity=quantity,
                )
            )

        return items

    def _fetch_sold_items(self) -> list[EbayItemPayload]:
        data = self._get("/sell/fulfillment/v1/order", params={"limit": 100})
        orders = data.get("orders", [])
        items: list[EbayItemPayload] = []

        for order in orders:
            line_items = order.get("lineItems", [])
            for line_item in line_items:
                line_id = str(line_item.get("lineItemId") or "")
                if not line_id:
                    continue

                line_cost = line_item.get("lineItemCost", {})
                price = float(line_cost.get("value") or 0.0)
                currency = str(line_cost.get("currency") or "USD")
                quantity = int(line_item.get("quantity") or 1)
                title = str(line_item.get("title") or f"Order Line {line_id}")

                items.append(
                    EbayItemPayload(
                        ebay_item_id=f"sold-{line_id}",
                        title=title,
                        category="Unknown",
                        status="sold",
                        price=price,
                        currency=currency,
                        quantity=quantity,
                    )
                )

        return items

    def _get(self, path: str, params: dict[str, Any]) -> dict[str, Any]:
        with httpx.Client(timeout=20.0) as client:
            response = client.get(
                f"{self._base_url}{path}",
                params=params,
                headers={
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Type": "application/json",
                    "X-EBAY-C-MARKETPLACE-ID": self.marketplace_id,
                },
            )
            response.raise_for_status()
            return response.json()

    @property
    def _base_url(self) -> str:
        if self.environment == "production":
            return "https://api.ebay.com"
        return "https://api.sandbox.ebay.com"

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
