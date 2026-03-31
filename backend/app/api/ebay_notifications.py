from __future__ import annotations

import hashlib
import logging
from typing import Any

from fastapi import APIRouter, HTTPException, Query, Request

from app.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/api/ebay/marketplace_account_deletion")
def verify_marketplace_account_deletion(
    challenge_code: str | None = Query(default=None),
) -> dict[str, str]:
    if not challenge_code:
        raise HTTPException(
            status_code=400,
            detail="Missing required query parameter: challenge_code",
        )
    if not settings.ebay_verification_token or not settings.ebay_endpoint_url:
        raise HTTPException(
            status_code=500,
            detail="Missing EBAY_VERIFICATION_TOKEN or EBAY_ENDPOINT_URL configuration",
        )

    source = f"{challenge_code}{settings.ebay_verification_token}{settings.ebay_endpoint_url}"
    challenge_response = hashlib.sha256(source.encode("utf-8")).hexdigest()
    return {"challengeResponse": challenge_response}


@router.post("/api/ebay/marketplace_account_deletion")
async def handle_marketplace_account_deletion_notification(
    request: Request,
) -> dict[str, str]:
    payload: dict[str, Any] = await request.json()
    user_identifier = _extract_user_identifier(payload)

    if user_identifier:
        logger.info(
            "Received eBay marketplace account deletion notification for user: %s",
            user_identifier,
        )
    else:
        logger.info("Received eBay marketplace account deletion notification (no user id found)")

    logger.info("eBay marketplace account deletion payload: %s", payload)
    return {"status": "ok"}


def _extract_user_identifier(payload: dict[str, Any]) -> str | None:
    direct_username = payload.get("username")
    if isinstance(direct_username, str) and direct_username.strip():
        return direct_username.strip()

    direct_user_id = payload.get("userId")
    if isinstance(direct_user_id, str) and direct_user_id.strip():
        return direct_user_id.strip()

    for key in ("notification", "data", "metadata"):
        nested = payload.get(key)
        if isinstance(nested, dict):
            nested_username = nested.get("username")
            if isinstance(nested_username, str) and nested_username.strip():
                return nested_username.strip()

            nested_user_id = nested.get("userId")
            if isinstance(nested_user_id, str) and nested_user_id.strip():
                return nested_user_id.strip()

    return None
