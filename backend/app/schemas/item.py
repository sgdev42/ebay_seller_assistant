from datetime import datetime

from pydantic import BaseModel


class ItemRead(BaseModel):
    id: int
    ebay_item_id: str
    title: str
    category: str
    status: str
    price: float
    currency: str
    quantity: int
    created_at: datetime
    updated_at: datetime


class ListingCreateRequest(BaseModel):
    title: str
    category: str
    price: float
    currency: str = "USD"
    quantity: int = 1


class ListingCreateFromTemplateRequest(BaseModel):
    template_item_id: int
    title: str | None = None
    price: float | None = None
