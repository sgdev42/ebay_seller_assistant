from pydantic import BaseModel


class EbayAuthConfigRead(BaseModel):
    client_id: str
    marketplace_id: str
    use_mock: bool
    has_client_secret: bool
    has_refresh_token: bool


class EbayAuthConfigUpdate(BaseModel):
    client_id: str = ""
    client_secret: str = ""
    refresh_token: str = ""
    marketplace_id: str = "EBAY_US"
    use_mock: bool = True
