# eBay Seller Assistant — Implementation Plan

## Overview
This assistant will:
- Track all seller items (active, sold, cancelled) via eBay API
- Enable new listings by referencing similar past listings
- (Optional) Suggest prices based on eBay/online data

---

## Steps

### Phase 1: Item Tracking & Extraction
1. Integrate with eBay API (OAuth, inventory endpoints)
2. Implement backend service to fetch/store item data (active, sold, cancelled)
3. Design item data model (status, title, price, category, etc.)
4. Build React dashboard to display/filter items

### Phase 2: Listing Creation via Similarity
5. Implement search for similar past listings (title, category, attributes)
6. Build UI to select a past listing as template
7. Pre-fill new listing form with template data
8. Integrate with eBay API to create new listing

### Phase 3: Pricing Recommendation (Optional)
9. Fetch pricing data for similar items from eBay/other sources
10. Implement pricing suggestion logic (average, trends)
11. Display suggested price in listing creation UI

---

## Relevant files
- backend/api/ebay_client.py — eBay API integration
- backend/models/item.py — Item data model
- backend/services/item_service.py — Item management logic
- frontend/components/ItemDashboard.jsx — Item tracking UI
- frontend/components/NewListingForm.jsx — New listing UI
- backend/services/pricing_service.py — (Optional) Pricing logic

---

## Verification
1. Authenticate and fetch all item statuses; verify with eBay dashboard
2. Create new listing from template; confirm on eBay
3. (Optional) Compare suggested price with market prices

---

## Decisions
- Single eBay account support for MVP
- Tech stack: Python FastAPI (backend), React (frontend)
- Data sync: on-demand + periodic background sync
