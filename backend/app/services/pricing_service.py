from __future__ import annotations

from statistics import mean

from sqlmodel import Session, col, select

from app.models.item import Item
from app.schemas.pricing import PricingSuggestionRead


class PricingService:
    def suggest_price(
        self,
        session: Session,
        title: str,
        category: str | None = None,
        currency: str = "USD",
        min_samples: int = 2,
    ) -> PricingSuggestionRead:
        candidates = self._find_candidates(
            session,
            title=title,
            category=category,
            currency=currency,
        )
        sold_candidates = [item for item in candidates if item.status == "sold"]

        dataset = sold_candidates if len(sold_candidates) >= min_samples else candidates
        if len(dataset) < min_samples:
            raise ValueError("Not enough comparable listings to generate a suggestion yet")

        prices = [item.price for item in dataset]
        avg_price = mean(prices)
        min_price = min(prices)
        max_price = max(prices)
        trend = self._estimate_trend(dataset)

        trend_factor = {"upward": 1.03, "downward": 0.97, "stable": 1.0}[trend]
        suggested = round(avg_price * trend_factor, 2)

        confidence = min(0.95, 0.35 + (0.1 * len(dataset)))
        strategy = (
            "Sold-listing weighted average with trend adjustment"
            if dataset is sold_candidates
            else "Fallback to active+sold comparable average with trend adjustment"
        )

        notes = [
            f"Comparable listings analyzed: {len(dataset)}",
            f"Trend detected: {trend}",
            "Uses internal historical listings for now; external market data adapters are pending.",
        ]

        return PricingSuggestionRead(
            suggested_price=suggested,
            currency=currency,
            sample_size=len(dataset),
            min_price=round(min_price, 2),
            max_price=round(max_price, 2),
            average_price=round(avg_price, 2),
            trend=trend,
            confidence=round(confidence, 2),
            strategy=strategy,
            notes=notes,
        )

    def _find_candidates(
        self,
        session: Session,
        title: str,
        category: str | None,
        currency: str,
    ) -> list[Item]:
        statement = (
            select(Item)
            .where(Item.status.in_(["sold", "active"]))
            .where(Item.currency == currency)
        )

        if category:
            statement = statement.where(Item.category == category)

        title_terms = [term for term in title.split() if len(term) >= 3]
        if title_terms:
            for term in title_terms[:3]:
                statement = statement.where(col(Item.title).contains(term))

        statement = statement.order_by(Item.updated_at.desc()).limit(50)
        return list(session.exec(statement).all())

    @staticmethod
    def _estimate_trend(items: list[Item]) -> str:
        if len(items) < 4:
            return "stable"

        ordered = sorted(items, key=lambda item: item.updated_at)
        midpoint = len(ordered) // 2
        older = ordered[:midpoint]
        newer = ordered[midpoint:]

        if not older or not newer:
            return "stable"

        older_avg = mean(item.price for item in older)
        newer_avg = mean(item.price for item in newer)

        if older_avg == 0:
            return "stable"

        delta = (newer_avg - older_avg) / older_avg
        if delta >= 0.03:
            return "upward"
        if delta <= -0.03:
            return "downward"
        return "stable"
