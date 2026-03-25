# IMPLEMENTATION PLAN
## MoodMash — AI for Bharat Hackathon
> Status: Awaiting approval. No code will be written until confirmed.

---

## AUDIT SUMMARY

### What Each Teammate Built

| Teammate | Area | State | Notes |
|---|---|---|---|
| T1 | Frontend (React/Vite) | 85% UI complete | Beautiful components, wrong feature structure, all API calls are dead (point to wrong backend) |
| T2 | Backend (FastAPI/Python) | 20% scaffold | Good API structure, DynamoDB schemas, vector math — ALL handlers are empty TODO stubs |
| T3 | Knowledge Base | 0% | All JSON files are 0 bytes — nothing curated |
| T4 | Prompts | 0% | All `.md` files are 0 bytes — nothing written |

### Critical Gap vs context.md Spec

The frontend was built as a generic "VibeGraph feed reader" (Sidebar + FeedPage, not the 5-feature flow). The backend was started in FastAPI but left as stubs. Knowledge base and prompts were never started. **The 5 features from context.md do not exist end-to-end yet.**

---

## FINAL ARCHITECTURE

```
Stack:
  Frontend   → React 18 + Vite + Tailwind (keep existing)
  Backend    → FastAPI (Python) + Mangum adapter → Lambda-deployable
  AI         → lib/ai.py mock adapter → swap to Bedrock Claude/Titan via env flag
  DB         → lib/db.py in-memory adapter → swap to DynamoDB via env flag
  Dev        → npm run dev (root) = Vite on :5173 + Uvicorn on :8000 via concurrently

Lambda path:
  FastAPI app → Mangum(app) → AWS Lambda handler
  Each "function" file in backend/functions/ is a pure Python handler:
    handler(event: dict, context=None) -> dict
  FastAPI routes call these handlers directly.
  SAM template deploys the whole FastAPI app as a single Lambda behind API GW.
```

### Directory Structure (Final State)

```
/workspace/moodmash/
│
├── frontend/                         # React/Vite — restructured to 5 features
│   ├── src/
│   │   ├── components/
│   │   │   ├── Onboarding/           # MIGRATED: existing quiz components
│   │   │   │   ├── OnboardingPage.jsx    (keep, minor rewire)
│   │   │   │   ├── QuestionScreen.jsx    (keep as-is)
│   │   │   │   ├── OptionTile.jsx        (keep as-is)
│   │   │   │   └── ProgressBar.jsx       (keep as-is)
│   │   │   ├── DNACard/              # MIGRATED: existing TasteDNACard
│   │   │   │   └── DNACard.jsx           (keep, minor rewire to use API)
│   │   │   ├── GrowthPath/           # NEW: Absorb/Create/Reflect path UI
│   │   │   │   └── GrowthPath.jsx
│   │   │   ├── Analytics/            # MIGRATED: Dashboard.jsx → rewired to real data
│   │   │   │   └── Analytics.jsx
│   │   │   ├── DataPanel/            # NEW: Privacy data control panel
│   │   │   │   └── DataPanel.jsx
│   │   │   └── common/               # MIGRATED: Sidebar, Button, Input, Modal, Loader
│   │   │       ├── Sidebar.jsx           (keep, update nav items)
│   │   │       ├── Button/           (keep)
│   │   │       ├── Input/            (keep)
│   │   │       ├── Modal/            (keep)
│   │   │       └── Loader/           (keep)
│   │   ├── pages/                    # NEW: thin page wrappers
│   │   │   ├── Landing.jsx           (new — value prop + "Start Quiz" CTA)
│   │   │   └── NotFound.jsx          (keep existing)
│   │   ├── hooks/                    # keep existing
│   │   ├── services/
│   │   │   └── api.js                (REWRITE — clean client for all 8 endpoints)
│   │   ├── data/
│   │   │   └── onboardingQuestions.js (REWRITE — Indian-first, per context.md spec)
│   │   ├── utils/                    # keep existing
│   │   └── App.jsx                   (REWRITE — React Router with 5-feature flow)
│   ├── index.html
│   ├── package.json                  (keep)
│   ├── vite.config.js                (keep)
│   └── tailwind.config.js            (keep)
│
├── backend/                          # FastAPI — rebuilt clean
│   ├── lib/
│   │   ├── ai.py                     (NEW — mock adapter, swappable to Bedrock)
│   │   └── db.py                     (NEW — in-memory adapter, swappable to DynamoDB)
│   ├── functions/                    (NEW — Lambda-style handlers, no FastAPI deps)
│   │   ├── onboard.py                POST /api/onboard
│   │   ├── generate_dna.py           GET  /api/dna/{session_id}
│   │   ├── get_path.py               POST /api/path
│   │   ├── path_feedback.py          POST /api/path/{path_id}/feedback
│   │   ├── analytics.py              GET  /api/analytics/{session_id}
│   │   └── data_control.py           GET + DELETE /api/data/{session_id}
│   ├── main.py                       (NEW — FastAPI app, routes call functions/, Mangum export)
│   ├── requirements.txt              (NEW — fastapi, uvicorn, mangum, anthropic, boto3)
│   └── template.yaml                 (NEW — SAM CloudFormation for AWS deployment)
│
├── knowledge-base/
│   └── content.json                  (NEW — 60+ items, 70%+ Indian content)
│
├── prompts/
│   ├── taste-embedding.md            (NEW)
│   ├── archetype-generation.md       (NEW)
│   ├── path-generation.md            (NEW)
│   └── analytics-insights.md         (NEW)
│
├── docs/                             (keep existing docs, no changes)
│
├── _archive/                         (MOVED — everything non-final goes here)
│   ├── python-api/                   old backend/api/ (FastAPI with stubs)
│   ├── python-src/                   old backend/src/ (handlers, services, utils)
│   ├── python-infra/                 old backend/infrastructure/
│   ├── python-scripts/               old backend/scripts/
│   ├── docker/                       docker-compose.yml, override, Dockerfiles
│   ├── design-docs/                  30+ root-level *.md design files
│   └── old-frontend/                 FeedPage, FeedCard, FeedSection, old pages/
│
├── package.json                      (ROOT — npm run dev via concurrently)
├── .env.example                      (updated)
└── README.md                         (updated with setup instructions)
```

---

## WHAT GETS ARCHIVED (and why)

| Path | Destination | Reason |
|---|---|---|
| `backend/api/` | `_archive/python-api/` | Old FastAPI scaffold — routes were stubs, being replaced by clean rebuild |
| `backend/src/` | `_archive/python-src/` | Handler stubs, bedrock_client.py (incomplete), replaced by clean `backend/functions/` and `backend/lib/` |
| `backend/infrastructure/` | `_archive/python-infra/` | DynamoDB JSON schemas referenced in new `lib/db.py`; template.yaml rebuilt per SAM spec |
| `backend/scripts/` | `_archive/python-scripts/` | DynamoDB init scripts useful for reference, not needed for local in-memory dev |
| `backend/handlers/`, `backend/services/` | `_archive/python-src/` | Empty directories with Dockerfiles — not used |
| `backend/tests/` | `_archive/python-src/tests/` | Tests for stub code |
| `docker-compose.yml`, `docker-compose.override.yml` | `_archive/docker/` | Not needed for npm run dev workflow |
| `frontend/src/components/FeedPage.jsx` | `_archive/old-frontend/` | Generic content feed — not one of the 5 features |
| `frontend/src/components/FeedCard/`, `FeedSection/`, `FeedItem.jsx` | `_archive/old-frontend/` | Feed components not part of final structure |
| `frontend/src/components/MediaCard.jsx`, `VideoCard.jsx` | `_archive/old-frontend/` | Feed-specific card types |
| `frontend/src/components/Sidebar.jsx` (root) | Replaced by `common/Sidebar.jsx` | Moved, nav items rewritten for 5-feature flow |
| `frontend/src/pages/Dashboard.jsx` | Migrated to `components/Analytics/` | Rewired to real API data |
| `frontend/src/pages/Login.jsx`, `Signup.jsx`, `Profile.jsx`, `Notifications.jsx` | `_archive/old-frontend/` | No auth in MVP |
| `frontend/src/contexts/AuthContext.jsx` | `_archive/old-frontend/` | No auth in MVP |
| `frontend/src/services/api.js` (existing) | Replaced | Complete rewrite to match 8 real endpoints |
| `frontend/src/data/onboardingQuestions.js` (existing) | Replaced | Rewrite with Indian-first questions per context.md spec |
| Root-level `*.md` (30 files: COMPONENTS.md, DESIGN_SYSTEM.md, FEED_*.md, etc.) | `_archive/design-docs/` | Design notes from previous iteration, not final docs |
| `restructure.sh`, `test-integration.sh` | `_archive/` | Shell scripts for old Docker setup |
| `scripts/` directory | `_archive/` | Docker/infra scripts, not needed |
| `tests/` directory | `_archive/` | Tests for old architecture; new tests can be added later |
| `tailwind.config.js` (root), `postcss.config.js` (root) | `_archive/` | Root-level config files that duplicate frontend's own config |

---

## WHAT GETS KEPT (migrated as-is or with minor changes)

| Asset | How Used | Changes Needed |
|---|---|---|
| `frontend/src/components/onboarding/QuestionScreen.jsx` | Moved to `Onboarding/QuestionScreen.jsx` | None — works perfectly |
| `frontend/src/components/onboarding/OptionTile.jsx` | Moved to `Onboarding/OptionTile.jsx` | None |
| `frontend/src/components/onboarding/ProgressBar.jsx` | Moved to `Onboarding/ProgressBar.jsx` | None |
| `frontend/src/components/onboarding/OnboardingPage.jsx` | Moved to `Onboarding/OnboardingPage.jsx` | Rewire: after quiz done, call `POST /api/onboard`, navigate to `/dna/:sessionId` |
| `frontend/src/components/onboarding/TasteDNACard.jsx` | Moved to `DNACard/DNACard.jsx` | Rewire: fetch data from `GET /api/dna/:sessionId`, display real AI archetype/summary/markers; add nav to `/path/:sessionId` |
| `frontend/src/components/ui/` (Button, Input, etc.) | Moved to `common/` | None |
| `frontend/src/components/Modal/`, `Loader/` | Moved to `common/` | None |
| `frontend/src/components/ErrorBoundary.jsx` | Kept in `common/` | None |
| `frontend/tailwind.config.js` | Keep | None |
| `frontend/package.json` | Keep | None — all deps already installed |
| `frontend/vite.config.js` | Keep | None |
| `backend/src/utils/vector_ops.py` | Copied to `backend/lib/vector_ops.py` | Keep as utility for cosine similarity in `lib/db.py` buddy matching |
| `context.md` | Root | None — it's the spec |
| `docs/` | Root | No changes — keep all existing docs |
| `.env.example` | Root | Rewrite with new variables |

---

## WHAT GETS BUILT (new files, file by file)

### Root

**`package.json`** (root)
```json
{
  "scripts": {
    "dev": "concurrently \"npm run dev --prefix frontend\" \"uvicorn backend.main:app --reload --port 8000\"",
    "install:all": "npm install && pip install -r backend/requirements.txt"
  },
  "devDependencies": { "concurrently": "^8.2.2" }
}
```

**`.env.example`**
```
VITE_API_URL=http://localhost:8000
USE_MOCK=true
USE_DYNAMODB=false
ANTHROPIC_API_KEY=your_key_here
AWS_REGION=ap-south-1
SPOTIFY_CLIENT_ID=
SPOTIFY_CLIENT_SECRET=
```

---

### Backend

**`backend/lib/ai.py`** — AI Adapter
- `USE_MOCK` env flag controls routing
- Mock path: deterministic, realistic Indian-themed responses
- Bedrock path (stub, clean swap): calls Anthropic SDK with prompts from `/prompts/`
- Functions exported:
  - `generate_embedding(quiz_answers: dict) -> list[float]` — 384-dim mock vector
  - `generate_archetype(embedding, quiz_answers) -> dict` — archetype name, vibe_summary, markers, radar_scores, cross_platform_insight
  - `generate_growth_path(embedding, mood, goal, time_available, content_items) -> list[dict]` — 3-5 sequenced items
  - `generate_analytics_insight(stats: dict) -> str` — one natural language observation

Mock archetype logic: maps quiz answer patterns to one of 8 Indian-cultural archetypes ("Midnight Philosopher", "Desi Renaissance Soul", "Chai Minimalist", "Chaos Creative", "Analog Futurist", "Rhythm Seeker", "The Storyteller", "Digital Nomad"). Realistic radar scores derived from quiz answers (music→music score, books→books score, etc.).

**`backend/lib/db.py`** — DB Adapter
- `USE_DYNAMODB` env flag controls routing
- In-memory path: Python dict, lives for process lifetime (fine for demo)
- DynamoDB path (stub, clean swap): boto3 calls with same interface
- Functions exported:
  - `put_session(session_id, data)` / `get_session(session_id) -> dict`
  - `put_path_feedback(session_id, item_id, status, reaction)`
  - `get_path_feedback(session_id) -> list`
  - `delete_session(session_id)`
  - `list_all_sessions() -> list` (for buddy matching)

**`backend/lib/vector_ops.py`** — MIGRATED from `backend/src/utils/vector_ops.py`
- `normalize_vector(vector)`, `cosine_similarity(a, b)` — working Python code, keep as-is

---

**`backend/functions/onboard.py`**
```
handler(event) -> dict
  Input:  quiz_answers (dict of category → selected options), goal (string)
  Steps:
    1. validate quiz_answers
    2. ai.generate_embedding(quiz_answers) → embedding_vector
    3. session_id = uuid4()
    4. db.put_session(session_id, {embedding, goal, created_at, quiz_answers_hash})
       Note: quiz_answers NOT stored — only hash for dedup (privacy)
    5. Return: {session_id, embedding_id: session_id}
```

**`backend/functions/generate_dna.py`**
```
handler(event) -> dict
  Input:  path param session_id
  Steps:
    1. db.get_session(session_id) → session
    2. ai.generate_archetype(session.embedding, session.quiz_answers_hash) → dna
    3. If dna not cached in session: compute + store back to db
    4. Return: {archetype, vibe_summary, markers[5-7], radar_scores{5 domains}, cross_platform_insight}
```

**`backend/functions/get_path.py`**
```
handler(event) -> dict
  Input:  session_id, mood, goal, time_available (minutes)
  Steps:
    1. db.get_session(session_id) → session
    2. Load knowledge-base/content.json
    3. Filter items by: mood_tags match, time_available, goal alignment
    4. ai.generate_growth_path(embedding, mood, goal, time, filtered_items)
       → ordered list with Absorb/Create/Reflect sequence
    5. Return: {path_id: uuid, items: [{id, title, creator, domain, engagement_type,
               why_youll_love_it, why_it_grows_you, external_link, time_minutes}]}
```

**`backend/functions/path_feedback.py`**
```
handler(event) -> dict
  Input:  path_id (path param), item_id, status (done/skipped/saved), reaction (optional)
  Steps:
    1. db.put_path_feedback(session_id, item_id, status, reaction)
    2. Return: {ok: true}
```

**`backend/functions/analytics.py`**
```
handler(event) -> dict
  Input:  path param session_id
  Steps:
    1. db.get_session(session_id) → session
    2. db.get_path_feedback(session_id) → completions
    3. Compute: items_done, items_skipped, domain_distribution, goal_alignment_pct
    4. ai.generate_analytics_insight(stats) → insight string
    5. Return: {radar_scores, goal_alignment_pct, items_done, items_skipped,
               domain_breakdown, pattern_insight, spotify_connected: false}
```

**`backend/functions/data_control.py`**
```
GET  handler(event): db.get_session → return sanitized taste vector as JSON (no raw answers)
DELETE handler(event): db.delete_session → return {deleted: true}
```

---

**`backend/main.py`** — FastAPI App
```python
app = FastAPI(title="MoodMash API")
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Each route: parse request → build event dict → call function handler → return response
POST /api/onboard         → functions/onboard.handler
GET  /api/dna/{id}        → functions/generate_dna.handler
POST /api/path            → functions/get_path.handler
POST /api/path/{id}/feedback → functions/path_feedback.handler
GET  /api/analytics/{id}  → functions/analytics.handler
GET  /api/data/{id}       → functions/data_control.get_handler
DELETE /api/data/{id}     → functions/data_control.delete_handler
GET  /health              → {"status": "ok", "mock_mode": USE_MOCK}

# Lambda export
from mangum import Mangum
lambda_handler = Mangum(app)
```

**`backend/requirements.txt`**
```
fastapi==0.115.0
uvicorn[standard]==0.30.1
mangum==0.17.0
anthropic==0.40.0
boto3==1.35.0
pydantic==2.9.0
python-multipart==0.0.9
```

**`backend/template.yaml`** — SAM CloudFormation
```yaml
# Single Lambda function running the full FastAPI app via Mangum
# API Gateway HTTP API in front
# Environment variables: USE_MOCK, USE_DYNAMODB, ANTHROPIC_API_KEY
# DynamoDB tables: taste_profiles, path_completions (defined as SAM resources)
# IAM: Lambda role with Bedrock + DynamoDB permissions
```

---

### Frontend

**`frontend/src/App.jsx`** (rewrite)
```jsx
Routes:
  /           → <Landing />           (new — value prop + Start Quiz CTA)
  /onboard    → <OnboardingPage />    (migrated)
  /dna/:id    → <DNACard />           (migrated, rewired)
  /path/:id   → <GrowthPath />        (new)
  /analytics/:id → <Analytics />      (migrated from Dashboard.jsx)
  /data/:id   → <DataPanel />         (new)
  *           → <NotFound />

Sidebar is visible on /dna, /path, /analytics, /data routes (not onboarding/landing)
Session ID stored in sessionStorage, set after /onboard completes
```

**`frontend/src/services/api.js`** (rewrite)
```js
const BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export const api = {
  onboard:        (answers, goal) => post('/api/onboard', {quiz_answers: answers, goal}),
  getDNA:         (id)            => get(`/api/dna/${id}`),
  getPath:        (id, opts)      => post('/api/path', {session_id: id, ...opts}),
  submitFeedback: (pathId, data)  => post(`/api/path/${pathId}/feedback`, data),
  getAnalytics:   (id)            => get(`/api/analytics/${id}`),
  exportData:     (id)            => get(`/api/data/${id}`),
  deleteData:     (id)            => del(`/api/data/${id}`),
}
```

**`frontend/src/data/onboardingQuestions.js`** (rewrite — Indian-first, per context.md spec)

15 questions across 5 domains, emotionally resonant:
```
Domain 1 — Music (3 questions):
  "Pick the album cover that feels like your Sunday morning"
    → options: [Prateek Kuhad - in fond farewell, AR Rahman's Roja, Nucleya's Bass Rani, Bhairav morning raga, Anuv Jain's BAARISHEIN, Bombay Bicycle Club, Cigarettes After Sex, King's Maan Meri Jaan]
  "Your 3am playlist is..."
    → options: [lo-fi Hindustani, indie-sad Hindi, old Bollywood classics, Tamil film score, bedroom pop, jazz from Mumbai session musicians, Carnatic instrumental, electronic/ambient]
  "Which describes your relationship with music?"
    → options: [I feel it before I understand it, I analyze lyrics obsessively, background texture for focus, I discover through people not algorithms, I chase live performances, regional is spiritual, my mood creates the playlist]

Domain 2 — Films & Stories (3 questions):
  "Pick the film still that makes you feel something"
    → options: [Masaan (ghat scene), Pather Panchali (rain scene), Dil Chahta Hai (road trip), Lootera (autumn), Lagaan (match final over), Gangs of Wasseypur (revenge arc), Udaan (rooftop), The Lunchbox (city loneliness)]
  "The last book/story that stayed with you was about..."
    → options: [identity and belonging, love across distance, class and ambition, the ordinary made extraordinary, grief and acceptance, rebellion and consequence, a city as a character, cultural inheritance]
  "You'd rather spend 3 hours..."
    → options: [watching a 1970s Bengali film, reading an essay that changes how you see something, bingeing a dark thriller series, listening to a 2-hour music documentary, playing story-rich game, deep-diving a niche Wikipedia rabbit hole]

Domain 3 — Visual World (3 questions):
  "You're decorating your room — which vibe?"
    → options: [bare walls, one good print, maximalist Indian textiles, brutalist concrete aesthetic, plants everywhere, one statement vintage piece, gallery white with curated objects, chaotic creative desk energy]
  "Which Indian designer/artist resonates with you?"
    → options: [Sabyasachi (maximalist heritage), Raw Mango (quiet luxury), Jyothy Karat (ethical craft), Thukral & Tagra (pop-art commentary), Zarina Hashmi (geometric meditation), Dayanita Singh (intimate documentary), Rina Banerjee (diaspora surrealism), Riyas Komu (social realism)]
  "Best use of color:"
    → options: [Rajasthan block print primary saturation, single color entire frame, black and white always, unexpected pastel combinations, earth tones only, gradient digital, hand-applied texture imperfection]

Domain 4 — Creative & Goals (3 questions):
  "When you have unstructured time, you..."
    → options: [start making something (writing/drawing/music), consume deeply (read/watch/listen), think about an idea, get restless, learn a new skill, reach out to someone interesting, do nothing intentionally, plan what I want to make next]
  "Pick one: which book title would you pick up without reading the description?"
    → options: ["The Ministry of Utmost Happiness", "Piranesi", "Why I Am Not a Hindu", "Zero to One", "Show Your Work", "A Gentleman in Moscow", "Atomic Habits", "The Remains of the Day"]
  "Your north star right now:"
    → options: [build something that matters (creative career), get technically excellent (tech skills), find what actually makes me happy (wellness), start something of my own (entrepreneurship), understand where I come from (cultural roots), I want to be inspired and see what emerges]

Domain 5 — Consumption Style (3 questions):
  "You discover new things through..."
    → options: [one trusted friend's recommendation, deep Reddit/forum rabbit holes, algorithmic serendipity, a genre you already love, reading about creators not content, podcasts specifically, stumbling in a bookstore/Spotify playlist, following one person obsessively]
  "Your attention span for content:"
    → options: [2-min videos only, 20-min essays and mid-form, hour-long documentaries, 3-hour films with no breaks, books over weeks, podcasts on commute, depends entirely on the topic, I finish everything I start]
  "Content that actually changed something in you:"
    → options: [a film scene I couldn't stop thinking about, an essay that reframed how I see myself, an album that defined a year, a person's work (not just one piece), a conversation more than any content, a skill I learned that unlocked other things]
```

**`frontend/src/components/Onboarding/OnboardingPage.jsx`** (migrated, minor rewire)
- After final question: calls `api.onboard(answers, goal)` → gets `session_id`
- Stores `session_id` in `sessionStorage`
- Navigates to `/dna/${session_id}` (React Router `navigate`)
- Shows loading state during API call ("Building your Taste DNA...")

**`frontend/src/components/DNACard/DNACard.jsx`** (migrated from TasteDNACard.jsx)
- On mount: `api.getDNA(sessionId)` → gets real archetype, vibe_summary, markers, radar_scores
- Keeps existing visual design (radar chart, bars, archetype hero) — just uses real API data
- "Enter Growth Path" button navigates to `/path/${sessionId}`
- Share button serializes archetype + summary to clipboard/Web Share API

**`frontend/src/components/GrowthPath/GrowthPath.jsx`** (new)
- Mood selector (5 options: focused, exploratory, melancholic, energized, calm)
- Time selector (15 / 30 / 60 / 90 minutes)
- Goal auto-read from session, or picker if not set
- "Get My Path" → calls `api.getPath(sessionId, {mood, goal, time_available})`
- Renders 3-5 sequenced items:
  - Each item: colored header (🎧 Absorb = blue / ✏️ Create = amber / 💭 Reflect = purple)
  - Title, creator, domain tag, time badge
  - "Why you'll love it" + "Why it grows you" (italicized, smaller)
  - External link + action buttons: ✅ Done / ⏭️ Skip / 🔖 Save
  - Button click calls `api.submitFeedback(pathId, itemId, status)`
- Analytics CTA at bottom: "See your patterns →"

**`frontend/src/components/Analytics/Analytics.jsx`** (migrated from Dashboard.jsx)
- On mount: `api.getAnalytics(sessionId)` → gets real stats
- Renders:
  - Radar chart (same component, uses real radar_scores from API)
  - Goal alignment score (big number, progress bar)
  - Items Done / Skipped / Saved count
  - Domain breakdown (which domains you've consumed most)
  - AI pattern insight (one sentence from Claude, displayed in a card)
  - "Spotify: Not connected" placeholder with note "Connect to see cross-platform insights"
- Data panel CTA at bottom: "Control your data →"

**`frontend/src/components/DataPanel/DataPanel.jsx`** (new)
- "Your Taste Vector" section: shows the stored data fields (NOT the raw 384-dim vector — just the schema: archetype, radar_scores, goal, created_at, spotify_connected)
- "What We Store vs What We Don't" table:
  - Store: archetype, radar scores, goal, completion records
  - Don't Store: raw quiz answers, exact listening history, personal identity
- Export button: `api.exportData(sessionId)` → downloads JSON file
- Delete button: confirmation dialog → `api.deleteData(sessionId)` → clears session → redirects to "/"
- DPDP Act 2023 reference note

**`frontend/src/components/common/Sidebar.jsx`** (rewrite nav items)
```
Nav items (shown after onboarding):
  🧬 Taste DNA    → /dna/:sessionId
  🌱 Growth Path  → /path/:sessionId
  📊 Analytics    → /analytics/:sessionId
  🔒 My Data      → /data/:sessionId
```

**`frontend/src/pages/Landing.jsx`** (new)
- Clean, compelling hero: tagline from context.md
- "Every platform optimizes for your attention. We optimize for your growth."
- 3 feature pills: Taste DNA | Growth Paths | Privacy-first
- Single CTA: "Discover Your Taste DNA →" → navigates to `/onboard`
- Indian cultural visual references in copy

---

### Knowledge Base

**`knowledge-base/content.json`** (60+ items, 70%+ Indian content)

Distribution:
- Music: 15 items — Prateek Kuhad, Arijit Singh (indie), AR Rahman, Nucleya, Bombay Jayashri, Shankar-Ehsaan-Loy, Siddhant, King, Anuv Jain, Ilaiyaraaja, Shreya Ghoshal (classical cross), Parikrama, Indian Ocean, Lagaan OST, Sitar meditations
- Films: 12 items — Masaan, Pather Panchali, Lootera, Udaan, Dil Chahta Hai, The Lunchbox, Kapoor & Sons, Ship of Theseus, Gangs of Wasseypur, Parched, Taare Zameen Par, Manto
- Books/Articles: 10 items — Arundhati Roy (God of Small Things), Amitav Ghosh, Rabindranath Tagore (Gitanjali), Chetan Bhagat (entry-point), Jhumpa Lahiri, Pankaj Mishra essay, Paul Graham essays, Design for Real Life, Austin Kleon (Show Your Work)
- Art/Design: 8 items — Sabyasachi lookbook, Raw Mango editorial, Zarina Hashmi prints, Thukral & Tagra installation, Indian illustration collectives (Aeon Studios), Aneesh Bhat, typography essay on Devanagari
- Creators/YouTube: 8 items — Nikhil Kamath (business), Tanmay Bhat, Dhruv Rathee (context), Kurzgesagt (knowledge), TED-Ed, Mark Rober (STEM), Indian sci comm channels, NativeBabu
- Exercises/Prompts: 10 items — "Write a letter to your 10-years-later self", "Describe your ideal morning in sensory detail", "Sketch your mood as a landscape", "Make a playlist for someone you want to understand", "Write 3 things this song reminds you of", creative prompts for each growth goal

Each item follows the schema from context.md (id, title, creator, domain, sub_domain, engagement_type, mood_tags, growth_tags, region, language, time_minutes, description, external_link, content_type).

---

### Prompts

**`prompts/taste-embedding.md`**
- How to analyze quiz answer patterns (domain selections, emotional language, specificity of choices) into taste signals
- Maps to: introspection_depth, aesthetic_sensitivity, cultural_rootedness, ambition_orientation, consumption_breadth
- Output format: structured JSON with 5 domain scores and 3 dominant signals

**`prompts/archetype-generation.md`**
- Input: taste signals object
- Generates: archetype name (creative, Indian-resonant), vibe_summary (2-3 lines, second-person, emotionally accurate), markers (5-7 tags), radar_scores (0-1 for 5 domains), optional cross_platform_insight
- Archetype name style guide: evocative, not genre labels. "Chai Minimalist" not "Classical Music Fan". "Desi Renaissance Soul" not "Multi-genre Listener".
- Example outputs provided for each of 8 archetypes

**`prompts/path-generation.md`**
- Input: user taste signals + mood + goal + time_available + candidate content items
- Task: select 3-5 items, sequence as Absorb→Create→Reflect, write 1-sentence "why you'll love it" and 1-sentence "why it grows you" per item
- Constraints: respect time_available, first item always Absorb, at least one Create or Reflect item, Indian content preferred where taste aligns

**`prompts/analytics-insights.md`**
- Input: user stats (domain_breakdown, goal_alignment_pct, completion_pattern, items_done_types)
- Task: generate exactly 1-2 sentences, observational not prescriptive, neutral tone, note a non-obvious pattern
- Example: "You mark Reflect items done at 2x the rate of Absorb items — you may be a processor who needs to make sense of things before moving on."

---

## PHASE EXECUTION ORDER

### Phase 0 — Archive + Scaffold (no new logic)
1. Create `_archive/` with subdirectories
2. Move all listed files to `_archive/`
3. Create final directory structure (empty files as placeholders)
4. Confirm structure matches plan

### Phase 1 — Backend Core
1. Write `backend/lib/db.py` (in-memory adapter)
2. Write `backend/lib/ai.py` (mock adapter with Indian archetypes)
3. Write `backend/lib/vector_ops.py` (migrated)
4. Write all 6 `backend/functions/*.py` handlers
5. Write `backend/main.py` (FastAPI app wiring handlers)
6. Write `backend/requirements.txt`
7. Test: `uvicorn backend.main:app --reload` + curl each endpoint

### Phase 2 — Knowledge Base + Prompts
1. Write `knowledge-base/content.json` (60+ items)
2. Write all 4 prompt files in `/prompts/`
3. Verify path generation uses real knowledge-base items

### Phase 3 — Frontend Restructure
1. Create new component directories
2. Move/rename migrated components
3. Rewrite `App.jsx` with React Router (5 routes)
4. Rewrite `services/api.js`
5. Rewrite `data/onboardingQuestions.js` (Indian-first questions)
6. Wire `OnboardingPage.jsx` → API → navigate
7. Wire `DNACard.jsx` → API → render real data
8. Build `GrowthPath.jsx` (new)
9. Wire `Analytics.jsx` (from Dashboard.jsx) → real API
10. Build `DataPanel.jsx` (new)
11. Build `Landing.jsx` (new)
12. Rewrite `Sidebar.jsx` nav items
13. Archive old frontend files

### Phase 4 — Integration + Root Config
1. Write root `package.json` with `npm run dev`
2. Update `.env.example`
3. Write `backend/template.yaml` (SAM)
4. Update `README.md` (setup instructions)
5. End-to-end test: `npm run dev` → complete all 5 features

### Phase 5 — Polish
1. Loading states on all API calls
2. Error handling (API down, 404 session)
3. Smooth navigation flow (sessionId preserved through all routes)
4. Mobile responsive check

---

## SWAP-TO-AWS INSTRUCTIONS (for later)

To switch from mock → real Bedrock:
```bash
# .env
USE_MOCK=false
ANTHROPIC_API_KEY=sk-ant-...  # only needed for local Anthropic SDK testing
AWS_REGION=ap-south-1
```
Then in `backend/lib/ai.py`: the `_bedrock_*` functions call Bedrock using boto3 with the prompts from `/prompts/`. The `USE_MOCK=false` flag routes to those functions. Zero changes to handlers, routes, or frontend.

To switch from in-memory → DynamoDB:
```bash
# .env
USE_DYNAMODB=true
AWS_REGION=ap-south-1
DYNAMODB_TABLE_SESSIONS=taste_profiles
DYNAMODB_TABLE_COMPLETIONS=path_completions
```
Then in `backend/lib/db.py`: the `_dynamodb_*` functions are called. Zero changes to handlers.

SAM deploy:
```bash
sam build && sam deploy --guided
```
Template creates: Lambda function, API GW HTTP API, DynamoDB tables, IAM roles, Bedrock permissions.

---

## COMPLETE FILE MANIFEST (final state, 47 files)

```
/workspace/moodmash/
├── package.json                                      NEW
├── .env.example                                      UPDATED
├── README.md                                         UPDATED
├── context.md                                        KEEP
│
├── frontend/
│   ├── package.json                                  KEEP
│   ├── vite.config.js                                KEEP
│   ├── tailwind.config.js                            KEEP
│   ├── index.html                                    KEEP
│   └── src/
│       ├── main.jsx                                  KEEP
│       ├── index.css                                 KEEP
│       ├── App.jsx                                   REWRITE
│       ├── components/
│       │   ├── Onboarding/
│       │   │   ├── OnboardingPage.jsx                MIGRATE+REWIRE
│       │   │   ├── QuestionScreen.jsx                MIGRATE (no change)
│       │   │   ├── OptionTile.jsx                    MIGRATE (no change)
│       │   │   └── ProgressBar.jsx                   MIGRATE (no change)
│       │   ├── DNACard/
│       │   │   └── DNACard.jsx                       MIGRATE+REWIRE
│       │   ├── GrowthPath/
│       │   │   └── GrowthPath.jsx                    NEW
│       │   ├── Analytics/
│       │   │   └── Analytics.jsx                     MIGRATE+REWIRE
│       │   ├── DataPanel/
│       │   │   └── DataPanel.jsx                     NEW
│       │   └── common/
│       │       ├── Sidebar.jsx                       REWRITE (nav items)
│       │       ├── ErrorBoundary.jsx                 MIGRATE (no change)
│       │       └── ui/ (Button, Input, Modal, Loader) MIGRATE (no change)
│       ├── pages/
│       │   ├── Landing.jsx                           NEW
│       │   └── NotFound.jsx                          MIGRATE (no change)
│       ├── services/
│       │   └── api.js                                REWRITE
│       ├── data/
│       │   └── onboardingQuestions.js                REWRITE (Indian-first)
│       ├── hooks/
│       │   └── index.js                              KEEP
│       └── utils/                                    KEEP
│
├── backend/
│   ├── main.py                                       NEW
│   ├── requirements.txt                              NEW
│   ├── template.yaml                                 NEW
│   ├── lib/
│   │   ├── ai.py                                     NEW
│   │   ├── db.py                                     NEW
│   │   └── vector_ops.py                             MIGRATED
│   └── functions/
│       ├── onboard.py                                NEW
│       ├── generate_dna.py                           NEW
│       ├── get_path.py                               NEW
│       ├── path_feedback.py                          NEW
│       ├── analytics.py                              NEW
│       └── data_control.py                           NEW
│
├── knowledge-base/
│   └── content.json                                  NEW (60+ items)
│
├── prompts/
│   ├── taste-embedding.md                            NEW
│   ├── archetype-generation.md                       NEW
│   ├── path-generation.md                            NEW
│   └── analytics-insights.md                         NEW
│
├── docs/                                             KEEP (no changes)
│
└── _archive/
    ├── design-docs/     ← 30 root-level *.md files
    ├── python-api/      ← old backend/api/
    ├── python-src/      ← old backend/src/
    ├── python-infra/    ← old backend/infrastructure/
    ├── python-scripts/  ← old backend/scripts/
    ├── docker/          ← docker-compose files, Dockerfiles
    └── old-frontend/    ← FeedPage, FeedCard, old pages
```

---

## QUESTIONS RESOLVED

- **Express vs FastAPI**: FastAPI ✅ (user confirmed)
- **AI responses**: Mock/hardcoded for now, `USE_MOCK=true` flag ✅
- **Frontend structure**: Restructure to context.md 5-feature flow ✅
- **Dev workflow**: `npm run dev` from root (concurrently) — no Docker required ✅
- **Lambda-deployable**: FastAPI → Mangum adapter → SAM template ✅

---

*Review this plan. Reply "go" to proceed with execution in phase order.*
