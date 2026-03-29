from sqlmodel import Session, SQLModel, create_engine

from app.clients.ebay_client import EbayClient
from app.services.item_service import ItemService


def test_sync_items_creates_records():
    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)

    service = ItemService(EbayClient(use_mock=True))

    with Session(engine) as session:
        result = service.sync_items(session)
        assert result["created"] >= 3

        items = service.list_items(session)
        assert len(items) == result["total_remote"]


def test_create_listing_from_template():
    engine = create_engine("sqlite://", echo=False)
    SQLModel.metadata.create_all(engine)

    service = ItemService(EbayClient(use_mock=True))

    with Session(engine) as session:
        service.sync_items(session)
        template = service.list_items(session)[0]

        created = service.create_listing_from_template(
            session,
            template_item_id=template.id,
            title_override="Custom Listing Title",
            price_override=123.45,
        )

        assert created.title == "Custom Listing Title"
        assert created.price == 123.45
        assert created.status == "active"
        assert created.ebay_item_id.startswith("MOCK-")
