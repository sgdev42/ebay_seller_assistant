import pytest
from sqlmodel import Session, SQLModel, create_engine

from app.clients.ebay_client import EbayClient
from app.services.item_service import ItemService
from app.services.pricing_service import PricingService


def test_suggest_price_returns_recommendation():
    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)

    item_service = ItemService(EbayClient(use_mock=True))
    pricing_service = PricingService()

    with Session(engine) as session:
        item_service.sync_items(session)

        suggestion = pricing_service.suggest_price(
            session,
            title="Nike Air Max 90",
            category="Shoes",
            currency="USD",
        )

        assert suggestion.sample_size >= 2
        assert suggestion.suggested_price > 0
        assert suggestion.min_price <= suggestion.suggested_price <= suggestion.max_price * 1.2


def test_suggest_price_requires_enough_data():
    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)
    pricing_service = PricingService()

    with Session(engine) as session:
        with pytest.raises(ValueError):
            pricing_service.suggest_price(session, title="Rare One-Off Item")
