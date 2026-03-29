# eBay Seller Assistant — Implementation Plan

## Overview
This assistant will:
- Track all seller items (active, sold, cancelled) via eBay API
- Enable new listings by referencing similar past listings
- (Optional) Suggest prices based on eBay/online data

---

## Steps

### Phase 1: Item Tracking & Extraction
1. [~] Integrate with eBay API (OAuth, inventory endpoints)
Status: Partially completed. OAuth/token/user-input config exists (`/api/ebay/auth-config` + frontend form), but live eBay OAuth exchange + real inventory API calls are still stubbed.
Tested: Partially. Configuration save/load path tested manually via UI/API usage; no integration test against real eBay yet.
2. [x] Implement backend service to fetch/store item data (active, sold, cancelled)
Status: Completed for prototype using mock eBay client and SQLModel persistence.
Tested: Yes. `backend/tests/test_item_service.py` sync test passes in CI.
3. [x] Design item data model (status, title, price, category, etc.)
Status: Completed (`backend/app/models/item.py`).
Tested: Yes. Covered indirectly via sync/listing flow tests in `test_item_service.py`.
4. [x] Build React dashboard to display/filter items
Status: Completed (`frontend/src/components/ItemDashboard.jsx` + app wiring).
Tested: Yes via CI frontend lint/build pipeline (GitHub Actions), and functional verification during prototype assembly.

### Phase 2: Listing Creation via Similarity
5. [x] Implement search for similar past listings (title, category, attributes)
Status: Completed for title/category matching (`ItemService.find_similar_items`).
Tested: Partially. Exercised through API/UI flow; no dedicated unit test yet for ranking/filter edge cases.
6. [x] Build UI to select a past listing as template
Status: Completed (`frontend/src/components/NewListingForm.jsx` template radio selection).
Tested: Partially. Verified in prototype flow; no frontend automated tests yet.
7. [x] Pre-fill new listing form with template data
Status: Completed (title/price auto-fill when template selected).
Tested: Partially. Verified in UI behavior; no dedicated frontend test yet.
8. [~] Integrate with eBay API to create new listing
Status: Partially completed. Endpoint/service path exists and creates listing records via `EbayClient`; real external eBay listing API call is still stubbed.
Tested: Yes for mock path (`test_create_listing_from_template`), not tested against live eBay.

### Phase 3: Pricing Recommendation (Optional)
9. [ ] Fetch pricing data for similar items from eBay/other sources
Status: Not started.
Tested: No.
10. [ ] Implement pricing suggestion logic (average, trends)
Status: Not started.
Tested: No.
11. [ ] Display suggested price in listing creation UI
Status: Not started.
Tested: No.

---

## Relevant files
- backend/app/clients/ebay_client.py - eBay API integration abstraction (mock + future live client)
- backend/app/models/item.py - Item data model
- backend/app/services/item_service.py - Item management logic
- backend/app/models/ebay_auth.py - Stored eBay OAuth/token configuration
- backend/app/services/ebay_auth_service.py - eBay OAuth/token configuration service
- frontend/src/components/ItemDashboard.jsx - Item tracking UI
- frontend/src/components/NewListingForm.jsx - New listing UI
- frontend/src/components/EbayAuthForm.jsx - eBay OAuth/token user input UI
- backend/app/services/pricing_service.py - (Optional) Pricing logic (not implemented yet)

---

## Verification
1. [~] Authenticate and fetch all item statuses; verify with eBay dashboard
Current result: OAuth/token input + storage implemented, but real eBay API fetch is not connected yet.
2. [~] Create new listing from template; confirm on eBay
Current result: Mock listing creation works end-to-end and is unit-tested; real eBay confirmation pending live API integration.
3. [ ] (Optional) Compare suggested price with market prices
Current result: Not started.

## Test evidence (current)
- Backend lint: `ruff check app tests` passed
- Backend unit tests: `pytest` passed (`2 passed`)
- Frontend CI: lint/build passing after ESLint fix in latest commit

---

## Decisions
- Single eBay account support for MVP
- Tech stack: Python FastAPI (backend), React (frontend)
- Data sync: on-demand + periodic background sync
