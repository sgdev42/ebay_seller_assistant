from typing import Optional

from pydantic import BaseModel, Field


class PricingSuggestionRequest(BaseModel):
    title: str = Field(min_length=3)
    category: Optional[str] = None
    currency: str = "USD"
    min_samples: int = 2


class PricingSuggestionRead(BaseModel):
    suggested_price: float
    currency: str
    sample_size: int
    min_price: float
    max_price: float
    average_price: float
    trend: str
    confidence: float
    strategy: str
    notes: list[str]
