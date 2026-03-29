from typing import Optional

from sqlmodel import Field, SQLModel


class EbayAuthConfig(SQLModel, table=True):
    id: Optional[int] = Field(default=1, primary_key=True)
    client_id: str = Field(default="")
    client_secret: str = Field(default="")
    refresh_token: str = Field(default="")
    marketplace_id: str = Field(default="EBAY_US")
    use_mock: bool = Field(default=True)
