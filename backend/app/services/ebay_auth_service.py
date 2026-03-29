from sqlmodel import Session, select

from app.config import settings
from app.models.ebay_auth import EbayAuthConfig
from app.schemas.ebay_auth import EbayAuthConfigUpdate


class EbayAuthService:
    def get_or_create(self, session: Session) -> EbayAuthConfig:
        record = session.exec(select(EbayAuthConfig).where(EbayAuthConfig.id == 1)).first()
        if record:
            return record

        record = EbayAuthConfig(
            id=1,
            client_id=settings.ebay_client_id,
            client_secret=settings.ebay_client_secret,
            refresh_token=settings.ebay_refresh_token,
            marketplace_id=settings.ebay_marketplace_id,
            use_mock=settings.ebay_use_mock,
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record

    def update(self, session: Session, payload: EbayAuthConfigUpdate) -> EbayAuthConfig:
        record = self.get_or_create(session)
        record.client_id = payload.client_id.strip()
        record.client_secret = payload.client_secret.strip()
        record.refresh_token = payload.refresh_token.strip()
        record.marketplace_id = payload.marketplace_id.strip() or "EBAY_US"
        record.use_mock = payload.use_mock
        session.add(record)
        session.commit()
        session.refresh(record)
        return record
