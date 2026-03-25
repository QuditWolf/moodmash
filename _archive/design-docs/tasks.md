# MoodMash — Implementation Task Tracker

> Single source of truth for what's done, what's in progress, and what's left.
> Last updated: agent stopped cleanly after completing Group 1 partial.

---

## LEGEND
- ✅ Done
- ❌ Not Started / Not Yet Created
- ⚠️ Exists but needs review/fix

---

## PHASE 0 — Archive & Scaffold
- ✅ Archive old backend (python-api, python-src, docker, scripts) to `_archive/`
- ✅ Archive old frontend components to `_archive/old-frontend/`
- ✅ New directory structure created: `backend/lib/`, `backend/functions/`, `frontend/src/components/{Onboarding,DNACard,GrowthPath,Analytics,DataPanel,common}/`, `knowledge-base/`, `prompts/`

---

## PHASE 1 — Backend Core

### Infrastructure
- ✅ `backend/lib/__init__.py`
- ✅ `backend/lib/db.py` — all 6 functions: put_session, get_session, put_path_feedback, get_path_feedback, delete_session, list_all_sessions
- ✅ `backend/lib/vector_ops.py` — cosine_similarity, normalize_vector
- ✅ `backend/requirements.txt`
- ✅ `package.json` (root) — `npm run dev` with concurrently
- ⚠️ `.env.example` (root) — exists but not verified

### AI Adapter
- ✅ `backend/lib/ai.py` — all 4 functions wired to sub-modules

### AI Pipeline Modules
- ✅ `backend/lib/archetypes.py` — 8 Indian-cultural archetypes + match_archetype()
- ✅ `backend/lib/path_engine.py` — scoring, sequencing, why_love/why_grow templates
- ✅ `backend/lib/taste_analyzer.py` — quiz answers → domain_scores + 5 signal dimensions
- ❌ `backend/lib/insight_engine.py` — analytics insight generator (NOT YET CREATED)

### Lambda Handlers
- ✅ `backend/functions/__init__.py`
- ✅ `backend/functions/onboard.py`
- ✅ `backend/functions/generate_dna.py`
- ✅ `backend/functions/get_path.py` — uses pathlib to load knowledge-base/content.json ✅
- ✅ `backend/functions/path_feedback.py`
- ✅ `backend/functions/analytics.py`
- ✅ `backend/functions/data_control.py`

### FastAPI App
- ✅ `backend/main.py` — all 8 routes + CORS + /health

---

## PHASE 2 — Knowledge Base & Prompts

### Content Knowledge Base
- ✅ `knowledge-base/content.json` — 65 items: music(15), films(12), books(10), art(8), creators(8), exercises(12). All fields valid.

### Prompt Templates
- ✅ `prompts/dna.prompt.md`
- ✅ `prompts/path.prompt.md`
- ✅ `prompts/analytics.prompt.md`
- ✅ `prompts/adaptiveQuiz.prompt.md`

---

## PHASE 3 — Frontend Integration

### Core Wiring
- ✅ `frontend/src/App.jsx` — BrowserRouter, all routes
- ✅ `frontend/src/services/api.js` — clean API client (onboard, getDNA, getPath, submitFeedback, getAnalytics, exportData, deleteData)
- ✅ `frontend/src/data/onboardingQuestions.js` — 15 questions, 5 domains, Indian-first
- ✅ `frontend/src/components/Onboarding/OnboardingPage.jsx` — goal step + API call + navigate /dna/:id
- ✅ `frontend/vite.config.js` — proxy /api → :8000, port 3000

### Feature Components
- ✅ `frontend/src/pages/Landing.jsx`
- ✅ `frontend/src/components/DNACard/DNACard.jsx` — recharts radar, share, navigation
- ✅ `frontend/src/components/GrowthPath/GrowthPath.jsx` — mood/time selector, feedback buttons
- ✅ `frontend/src/components/Analytics/Analytics.jsx` — radar, goal %, domain bars, insight
- ✅ `frontend/src/components/DataPanel/DataPanel.jsx` — export/delete, DPDP Act 2023
- ✅ `frontend/src/components/common/Sidebar.jsx` — correct icons, sessionStorage, mobile-hidden

### Existing Onboarding Components (Unverified)
- ⚠️ `frontend/src/components/Onboarding/QuestionScreen.jsx` — not yet checked against new props
- ⚠️ `frontend/src/components/Onboarding/OptionTile.jsx` — not yet checked for long option text
- ⚠️ `frontend/src/components/Onboarding/ProgressBar.jsx` — not yet checked

---

## PHASE 4 — Integration & Testing

- ❌ Run frontend build check: `cd frontend && npm run build`
- ❌ Run backend: `cd backend && uvicorn main:app --reload --port 8000` — check no import errors
- ❌ Fix `backend/lib/ai.py` import of insight_engine (will fail until insight_engine.py is created)
- ❌ Verify QuestionScreen/OptionTile/ProgressBar props match OnboardingPage
- ❌ Full flow smoke test: / → /onboard → /dna/:id → /path/:id → /analytics/:id → /data/:id

---

## REMAINING WORK (priority order)
1. ❌ Create `backend/lib/insight_engine.py` — **BLOCKER**: analytics.py will 500 without it
2. ⚠️ Verify `backend/lib/ai.py` correctly imports insight_engine once it exists
3. ⚠️ Review QuestionScreen.jsx props interface vs OnboardingPage.jsx
4. ❌ Run build to catch any remaining import errors in frontend

---

## INTEGRATION DECISIONS (Resolved)
- **Session storage**: `sessionStorage` for session_id (not localStorage)
- **Vite port**: 3000
- **Backend port**: 8000
- **Spotify**: NOT in MVP — "coming soon" placeholder only
- **AI mode**: Mock (USE_MOCK=true) — text-based, no embeddings or Bedrock calls
- **Archetype caching**: Generated once on onboard, cached in session
