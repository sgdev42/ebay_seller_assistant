from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app.clients.ebay_client import EbayClient
from app.config import settings
from app.db.database import get_session
from app.schemas.ebay_auth import EbayAuthConfigRead, EbayAuthConfigUpdate
from app.schemas.item import ListingCreateFromTemplateRequest
from app.services.ebay_auth_service import EbayAuthService
from app.services.item_service import ItemService

router = APIRouter(prefix="/api")


def get_ebay_client(session: Session) -> EbayClient:
    auth_service = EbayAuthService()
    auth = auth_service.get_or_create(session)
    return EbayClient(
        use_mock=auth.use_mock,
        client_id=auth.client_id or settings.ebay_client_id,
        client_secret=auth.client_secret or settings.ebay_client_secret,
        refresh_token=auth.refresh_token or settings.ebay_refresh_token,
        marketplace_id=auth.marketplace_id or settings.ebay_marketplace_id,
    )


def get_item_service(session: Session = Depends(get_session)) -> ItemService:
    return ItemService(get_ebay_client(session))


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ebay/auth-config", response_model=EbayAuthConfigRead)
def get_ebay_auth_config(session: Session = Depends(get_session)):
    auth = EbayAuthService().get_or_create(session)
    return EbayAuthConfigRead(
        client_id=auth.client_id,
        marketplace_id=auth.marketplace_id,
        use_mock=auth.use_mock,
        has_client_secret=bool(auth.client_secret),
        has_refresh_token=bool(auth.refresh_token),
    )


@router.put("/ebay/auth-config", response_model=EbayAuthConfigRead)
def update_ebay_auth_config(
    payload: EbayAuthConfigUpdate,
    session: Session = Depends(get_session),
):
    auth = EbayAuthService().update(session, payload)
    return EbayAuthConfigRead(
        client_id=auth.client_id,
        marketplace_id=auth.marketplace_id,
        use_mock=auth.use_mock,
        has_client_secret=bool(auth.client_secret),
        has_refresh_token=bool(auth.refresh_token),
    )


@router.post("/items/sync")
def sync_items(
    session: Session = Depends(get_session),
    service: ItemService = Depends(get_item_service),
) -> dict[str, int]:
    return service.sync_items(session)


@router.get("/items")
def list_items(
    status: str | None = Query(default=None),
    search: str | None = Query(default=None),
    session: Session = Depends(get_session),
    service: ItemService = Depends(get_item_service),
):
    return service.list_items(session, status=status, search=search)


@router.get("/items/similar")
def similar_items(
    title: str = Query(..., min_length=3),
    category: str | None = Query(default=None),
    session: Session = Depends(get_session),
    service: ItemService = Depends(get_item_service),
):
    return service.find_similar_items(session, title=title, category=category)


@router.post("/listings/from-template")
def create_listing_from_template(
    payload: ListingCreateFromTemplateRequest,
    session: Session = Depends(get_session),
    service: ItemService = Depends(get_item_service),
):
    try:
        return service.create_listing_from_template(
            session,
            template_item_id=payload.template_item_id,
            title_override=payload.title,
            price_override=payload.price,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
