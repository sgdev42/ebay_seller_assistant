from __future__ import annotations

from datetime import datetime, timezone

from sqlmodel import Session, col, select

from app.clients.ebay_client import EbayClient, EbayListingPayload
from app.models.item import Item


class ItemService:
    def __init__(self, ebay_client: EbayClient):
        self.ebay_client = ebay_client

    def sync_items(self, session: Session) -> dict[str, int]:
        remote_items = self.ebay_client.fetch_items()
        created = 0
        updated = 0

        for remote in remote_items:
            statement = select(Item).where(Item.ebay_item_id == remote.ebay_item_id)
            existing = session.exec(statement).first()

            if existing:
                existing.title = remote.title
                existing.category = remote.category
                existing.status = remote.status
                existing.price = remote.price
                existing.currency = remote.currency
                existing.quantity = remote.quantity
                existing.updated_at = datetime.now(timezone.utc)
                session.add(existing)
                updated += 1
            else:
                item = Item(
                    ebay_item_id=remote.ebay_item_id,
                    title=remote.title,
                    category=remote.category,
                    status=remote.status,
                    price=remote.price,
                    currency=remote.currency,
                    quantity=remote.quantity,
                )
                session.add(item)
                created += 1

        session.commit()
        return {"created": created, "updated": updated, "total_remote": len(remote_items)}

    def list_items(
        self,
        session: Session,
        status: str | None = None,
        search: str | None = None,
    ) -> list[Item]:
        statement = select(Item)
        if status:
            statement = statement.where(Item.status == status.lower())
        if search:
            statement = statement.where(col(Item.title).contains(search))
        statement = statement.order_by(Item.updated_at.desc())
        return list(session.exec(statement).all())

    def find_similar_items(
        self,
        session: Session,
        title: str,
        category: str | None = None,
        limit: int = 5,
    ) -> list[Item]:
        statement = select(Item).where(Item.status.in_(["sold", "active"]))

        if category:
            statement = statement.where(Item.category == category)

        title_terms = [term for term in title.split() if len(term) >= 3]
        if title_terms:
            for term in title_terms[:3]:
                statement = statement.where(col(Item.title).contains(term))

        statement = statement.order_by(Item.updated_at.desc()).limit(limit)
        return list(session.exec(statement).all())

    def create_listing_from_template(
        self,
        session: Session,
        template_item_id: int,
        title_override: str | None = None,
        price_override: float | None = None,
    ) -> Item:
        template = session.get(Item, template_item_id)
        if not template:
            raise ValueError("Template item not found")

        listing_payload = EbayListingPayload(
            title=title_override or template.title,
            category=template.category,
            price=price_override if price_override is not None else template.price,
            currency=template.currency,
            quantity=template.quantity,
        )

        result = self.ebay_client.create_listing(listing_payload)
        new_item = Item(
            ebay_item_id=result.ebay_item_id,
            title=listing_payload.title,
            category=listing_payload.category,
            status=result.status,
            price=listing_payload.price,
            currency=listing_payload.currency,
            quantity=listing_payload.quantity,
        )
        session.add(new_item)
        session.commit()
        session.refresh(new_item)
        return new_item
