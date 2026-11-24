# SehatSetu 2.0

**AI-Powered Healthcare Query Classification and Intelligent Routing Platform**

> Bridging Healthcare Access Through Intelligent Technology.

SehatSetu upgrades the supplied TeleCare Rural / ExtroNerds Telemedicine project into a research-oriented healthcare navigation platform. The original HTML/CSS/JS and Express implementation is preserved under `legacy/`; the new application uses React + TypeScript + Vite, FastAPI/scikit-learn, and Supabase.

## Safety boundary

SehatSetu classifies healthcare queries and routes users toward an appropriate service. It is **not** a diagnostic, prescription, or emergency-response substitute. A separate emergency safety layer can override normal classification when configured high-risk phrases are detected and directs the user to local emergency medical assistance.

## Repository layout

- `frontend/` — React + TypeScript + Vite + Tailwind CSS + Framer Motion + Recharts + Lucide
- `ml-service/` — FastAPI + scikit-learn training/inference service
- `supabase/` — SQL migrations and Row Level Security policies
- `docs/` — architecture, migration audit and validation notes
- `legacy/` — original project preserved for auditability

## Requirements

- Node.js 20+ recommended
- Python 3.10+
- A Supabase project for persistent authentication/data

## 1. Frontend

```bash
cd frontend
npm install
cp .env.example .env   # Windows: copy .env.example .env
npm run dev
```

Set these variables in `frontend/.env`:

```env
VITE_SUPABASE_URL=
VITE_SUPABASE_ANON_KEY=
VITE_API_BASE_URL=http://localhost:8000
```

`VITE_SUPABASE_*` enables real authentication and persistence. Without them, the public UI can still be viewed, but protected/persistent workflows are unavailable.

## 2. ML/API service

```bash
cd ml-service
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m app.train --data data/health_queries.csv
uvicorn app.main:app --reload --port 8000
```

The training command creates the ignored files under `ml-service/artifacts/`. Do not commit those generated artifacts unless you deliberately choose a model-artifact release workflow.

Optional service environment (`ml-service/.env.example`):

```env
CORS_ORIGINS=http://localhost:5173
RATE_LIMIT_PER_MINUTE=30
```

When deployed, set `CORS_ORIGINS` to the exact HTTPS frontend origin and use a production rate limit appropriate for your infrastructure.

## 3. Supabase

Create a Supabase project and apply, in order:

1. `supabase/migrations/202611250001_init.sql`
2. `supabase/migrations/202611250002_security.sql`

Then create a trusted administrator using an authorized database administrator. The application does not expose self-service role promotion.

The schema contains profiles, healthcare queries and appointments with Row Level Security. User-owned rows are restricted to the authenticated user; administrator reads/updates are policy-controlled.

## 4. Run the full local stack

Terminal 1:

```bash
cd ml-service
.venv\Scripts\activate   # Windows
uvicorn app.main:app --reload --port 8000
```

Terminal 2:

```bash
cd frontend
npm run dev
```

Open the Vite URL shown in the terminal (normally `http://localhost:5173`).

## Validation

Python tests:

```bash
PYTHONPATH=ml-service pytest -q ml-service/tests
```

Frontend tests:

```bash
cd frontend
npm test
```

Production build:

```bash
cd frontend
npm run build
```

Run the build in the target environment after installing dependencies. The repository does not claim a successful build unless that command has actually completed successfully.

## ML evaluation

The training pipeline reports accuracy, precision, recall, F1-score, confusion matrix and per-class metrics. The included CSV is **synthetic development data**, not a clinically validated dataset. Do not present its metrics as clinical performance. Before any research or production claim, replace it with a properly licensed, clinically reviewed and representative dataset and document the annotation/evaluation protocol.

## Production boundaries

- Keep `.env` files, service-role keys and patient information out of Git.
- Deploy frontend/API over HTTPS.
- Use a managed/production video consultation provider before claiming live video calls.
- The medicine interface is informational and non-prescriptive.
- The emergency safeguard is a routing feature, not an emergency response service.
- Real-world clinical use requires appropriate clinical, privacy, security and regulatory review.

## Research value

The project demonstrates applied NLP, supervised multi-class classification, confidence-aware routing, explainable model evidence, safety overrides, full-stack integration, Supabase RLS and reproducible evaluation. See `docs/ARCHITECTURE.md`, `docs/MIGRATION_AUDIT.md` and `docs/VALIDATION.md`.
