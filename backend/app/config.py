from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "eBay Seller Assistant API"
    database_url: str = "sqlite:///./ebay_assistant.db"

    ebay_client_id: str = ""
    ebay_client_secret: str = ""
    ebay_refresh_token: str = ""
    ebay_access_token: str = ""
    ebay_environment: str = "sandbox"
    ebay_marketplace_id: str = "EBAY_US"
    ebay_verification_token: str = ""
    ebay_endpoint_url: str = ""
    ebay_use_mock: bool = True
    enable_periodic_sync: bool = True
    sync_interval_seconds: int = 900

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
