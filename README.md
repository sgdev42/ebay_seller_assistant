# eBay Seller Assistant (Prototype v1)

FastAPI + React prototype based on `IMPLEMENTATION_PLAN.md`.

## What this prototype covers
- Item sync and tracking (`active`, `sold`, `cancelled`)
- Item dashboard with status/search filters
- eBay OAuth/token settings from UI user input
- Similar past listing search
- Create listing from selected template
- CI workflow for backend/frontend checks

## Project structure
- `backend/` FastAPI API, SQLModel data model, item service, eBay client abstraction
- `frontend/` React (Vite) dashboard and listing creation UI
- `.github/workflows/ci.yml` CI for lint + tests/build
- `.github/workflows/cd.yml` CD packaging workflow (build container images)

## Backend setup
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

## Frontend setup
```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173` and proxies `/api` to backend `:8000`.

## Docker compose (optional)
```bash
docker compose up --build
```

This starts backend on `:8000` and frontend on `:5173`.

## API endpoints
- `GET /api/ebay/auth-config`
- `PUT /api/ebay/auth-config`
- `POST /api/items/sync`
- `GET /api/items?status=&search=`
- `GET /api/items/similar?title=&category=`
- `POST /api/listings/from-template`
- `GET /api/health`

## Notes
- MVP defaults to `EBAY_USE_MOCK=true` for deterministic local dev/testing.
- Real eBay OAuth + inventory/listing calls are stubbed behind `EbayClient` for later integration.
