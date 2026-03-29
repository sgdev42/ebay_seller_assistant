from sqlmodel import Session, SQLModel, create_engine

from app.config import settings
from app.models.ebay_auth import EbayAuthConfig  # noqa: F401
from app.models.item import Item  # noqa: F401

engine = create_engine(settings.database_url, echo=False)


def init_db() -> None:
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
