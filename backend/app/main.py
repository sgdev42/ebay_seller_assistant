import asyncio
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from app.api.routes import get_ebay_client, router
from app.config import settings
from app.db.database import engine, init_db
from app.services.item_service import ItemService

app = FastAPI(title=settings.app_name)
logger = logging.getLogger(__name__)
sync_task: asyncio.Task | None = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    global sync_task
    init_db()
    if settings.enable_periodic_sync:
        sync_task = asyncio.create_task(run_periodic_sync())


@app.on_event("shutdown")
async def on_shutdown() -> None:
    global sync_task
    if sync_task:
        sync_task.cancel()
        try:
            await sync_task
        except asyncio.CancelledError:
            pass
        sync_task = None


async def run_periodic_sync() -> None:
    while True:
        try:
            with Session(engine) as session:
                service = ItemService(get_ebay_client(session))
                service.sync_items(session)
        except Exception:  # pragma: no cover - guardrail for background loop
            logger.exception("Periodic sync failed")

        await asyncio.sleep(settings.sync_interval_seconds)


app.include_router(router)
