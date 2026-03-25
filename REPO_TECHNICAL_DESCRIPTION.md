# MoodMash — Complete Technical Description
*Generated 2026-03-25 for AI-assisted improvement instructions*

---

## 1. GIT INFORMATION

### Branch
Current branch: `prod_fast`
Other branches: `main`, `pr-3`, `remotes/origin/punyak`

### Last 10 Commits
```
503bbf9 hacky push to push to prod. inital test. requires cleanup and refactor
f6b981a Merge pull request #4 from QuditWolf/punyak
9612bbe Backend to be build
788296a merged frontend and punyak backend
ebedda2 Migration Needed | see docs/, *.md in root/
932cf85 Checkpoint before monorepo restructure
cccfe6e feat: add feed density modes (grid, visual, compact) with scroll reveal animations and smooth scrolling
a107e36 feat: add subtle image overlay gradient and hover action icons to feed cards
022bd39 feat: implement masonry feed layout
e4cb5c5 feat: make Taste DNA radar and bars data-driven using onboarding selections
```

Observation: Last commit message ("hacky push to push to prod. inital test. requires cleanup and refactor") explicitly flags unfinished state.

---

## 2. DIRECTORY TREE

```
moodmash/
├── .env                           # USE_MOCK=true, USE_DYNAMODB=false, VITE_API_URL=http://localhost:8000
├── .env.example                   # Root-level env example
├── .gitignore
│
├── CONTEXT.md                     # Full product/arch design doc (AI coding session artifact)
├── DEPLOYMENT.md                  # AWS deployment guide
├── JUDGE_FLOW.md                  # Testing guide for hackathon judges
├── JUDGE_QUICK_REFERENCE.md       # Quick reference for judges
├── PROJECT_SUMMARY.md             # Feature overview
├── QUICKSTART.md                  # 30-second start guide
├── README.md                      # Main project readme
├── SIMPLIFIED_STRUCTURE.md        # Architecture overview
├── STATUS.md                      # Current status / what's complete
├── TESTING.md                     # Testing guide
├── TROUBLESHOOTING.md             # Troubleshooting guide
│
├── backend/
│   ├── __init__.py
│   ├── main.py                    # FastAPI app (8 routes)
│   ├── package.json               # Leftover from old JS backend era (name: vibegraph-backend)
│   ├── pytest.ini
│   ├── requirements.txt           # fastapi, uvicorn, mangum, pydantic
│   ├── requirements-test.txt      # pytest, moto, boto3-stubs, hypothesis
│   ├── .env.example               # Old VibeGraph-branded env (AWS/Bedrock/DynamoDB config)
│   ├── functions/
│   │   ├── __init__.py
│   │   ├── analytics.py
│   │   ├── data_control.py
│   │   ├── generate_dna.py
│   │   ├── get_path.py
│   │   ├── onboard.py
│   │   └── path_feedback.py
│   └── lib/
│       ├── __init__.py
│       ├── ai.py                  # Mock AI adapter (USE_MOCK=true; live raises NotImplementedError)
│       ├── archetypes.py          # 8 Indian archetypes with keyword matching
│       ├── db.py                  # In-memory DB (USE_DYNAMODB=false; DynamoDB raises NotImplementedError)
│       ├── path_engine.py         # Text-based path scoring & sequencing
│       ├── taste_analyzer.py      # Quiz → domain scores + dimension scores
│       └── vector_ops.py          # normalize_vector(), cosine_similarity() (pure math, not currently called)
│
├── frontend/
│   ├── .env                       # VITE_API_URL= (empty — relies on Vite proxy)
│   ├── .env.example               # VITE_VIBEGRAPH_API_URL=http://localhost:8000
│   ├── .env.docker                # Docker env
│   ├── .dockerignore
│   ├── Dockerfile                 # Node20 builder → nginx:alpine, port 3000
│   ├── docker-entrypoint.sh
│   ├── index.html
│   ├── nginx.conf                 # Serves SPA on port 3000, gzip, SPA fallback
│   ├── package.json               # moodmash-app, React 18, Vite 5, Tailwind 3, Recharts, framer-motion
│   ├── package-lock.json
│   ├── postcss.config.js
│   ├── tailwind.config.js         # Dark mode class, custom CSS vars, IBM Plex Mono font
│   ├── vite.config.js             # Proxy /api → http://localhost:8000, port 3000
│   ├── vitest.config.js
│   └── src/
│       ├── App.jsx                # React Router: /, /onboard, /feed, /dna/:id, /path/:id, /analytics/:id, /data/:id
│       ├── App.css
│       ├── main.jsx
│       ├── index.css              # CSS vars, tailwind, glass/card-hover/glow utilities, custom text scale
│       ├── components/
│       │   ├── Analytics/
│       │   │   └── Analytics.jsx  # Radar chart + goal alignment + stats (calls api.getAnalytics)
│       │   ├── Card/
│       │   │   ├── Card.jsx
│       │   │   └── Card.css
│       │   ├── CompactCard.jsx
│       │   ├── DNACard/
│       │   │   └── DNACard.jsx    # Archetype card with RadarChart (calls api.getDNA)
│       │   ├── DataPanel/
│       │   │   └── DataPanel.jsx  # Export/delete data (calls api.exportData, api.deleteData)
│       │   ├── EmptyState/
│       │   ├── FileUpload/        # CSS + JSX present (not wired up in routing)
│       │   ├── GrowthPath/
│       │   │   └── GrowthPath.jsx # Mood/time selector → path items (calls api.getPath + api.submitFeedback)
│       │   ├── Navbar/
│       │   │   ├── Navbar.jsx
│       │   │   └── Navbar.css
│       │   ├── Onboarding/
│       │   │   ├── OnboardingPage.jsx  # 7-question flow + goal selection (calls api.onboard)
│       │   │   ├── OptionTile.jsx
│       │   │   ├── ProgressBar.jsx
│       │   │   ├── QuestionScreen.jsx
│       │   │   └── TasteDNACard.jsx    # Unused duplicate
│       │   ├── ProtectedRoute.jsx      # Exists but not used in App.jsx routing
│       │   ├── RevealOnScroll.jsx
│       │   ├── SectionHeader.jsx
│       │   ├── Sidebar.jsx             # Duplicate (see common/Sidebar.jsx)
│       │   ├── Sidebar/
│       │   │   ├── Sidebar.jsx
│       │   │   └── Sidebar.css
│       │   ├── common/
│       │   │   ├── Button/
│       │   │   ├── ErrorBoundary.jsx
│       │   │   ├── Input/
│       │   │   ├── Loader/
│       │   │   ├── Modal/
│       │   │   ├── Sidebar.jsx         # ACTIVE Sidebar used by App.jsx AppLayout
│       │   │   ├── avatar.jsx
│       │   │   ├── badge.jsx
│       │   │   ├── button.jsx
│       │   │   ├── card.jsx
│       │   │   └── separator.jsx
│       │   ├── onboarding/             # DUPLICATE of Onboarding/ (lowercase) — same files
│       │   ├── ui/
│       │   │   ├── avatar.jsx
│       │   │   ├── badge.jsx
│       │   │   ├── button.jsx
│       │   │   ├── card.jsx
│       │   │   └── separator.jsx
│       │   └── index.js
│       ├── data/
│       │   └── onboardingQuestions.js  # 7 questions + goalOptions + old generateTasteDNA() stub
│       ├── hooks/
│       │   └── index.js
│       ├── layouts/
│       │   ├── AuthLayout.jsx          # Exists but not used in App.jsx
│       │   ├── AuthLayout.css
│       │   ├── DashboardLayout.jsx     # Exists but not used in App.jsx
│       │   └── DashboardLayout.css
│       ├── pages/
│       │   ├── Dashboard.jsx           # Exists but not routed in App.jsx
│       │   ├── Dashboard.css
│       │   ├── DiscoverList.jsx        # Exists but not routed
│       │   ├── DiscoverList.css
│       │   ├── Feed.jsx                # Active — personalized or random content grid
│       │   ├── Feed.css
│       │   ├── Landing.jsx             # Active — hero + CTA
│       │   ├── NotFound.jsx
│       │   └── NotFound.css
│       ├── services/
│       │   ├── api.js                  # PRIMARY API client — maps to backend routes
│       │   └── vibeGraphAPI.js         # OLD/DEAD — targets /quiz/section1/start, /profile/dna/:userId etc.
│       ├── styles/
│       │   └── index.css
│       └── utils/
│           ├── helpers.js
│           └── logger.js
│
├── knowledge-base/                     # Content catalog (at ROOT, not frontend/public)
│   └── content.json                    # ~65 items, 1042 lines
│
├── frontend/public/knowledge-base/     # COPY of knowledge-base at frontend/public for browser fetch
│   ├── books.json
│   ├── catalog.schema.json
│   ├── content.json
│   ├── creators.json
│   ├── films.json
│   └── music.json
│
├── prompts/                            # AI prompt templates (not currently used by backend)
│   ├── adaptiveQuiz.prompt.md
│   ├── analytics.prompt.md
│   ├── dna.prompt.md
│   └── path.prompt.md
│
├── docs/                               # Extensive docs — mostly AI coding session artifacts
│   ├── DEPLOYMENT.md
│   ├── DEVELOPMENT.md
│   ├── FOLDER_STRUCTURE.md
│   ├── PROJECT_SUMMARY.md
│   ├── QUICKSTART.md
│   ├── README.md
│   ├── STRUCTURE.md
│   ├── TROUBLESHOOTING.md
│   ├── VALIDATION_CHECKLIST.md
│   ├── api/
│   │   ├── API_CONTRACTS.md
│   │   ├── README.md
│   │   ├── profile-endpoints.md
│   │   └── quiz-endpoints.md
│   ├── architecture/
│   │   ├── design.md
│   │   └── requirements.md
│   ├── backend/
│   │   ├── ARCHITECTURE.md
│   │   ├── DATA_FLOW.md
│   │   ├── EMBEDDING_STRATEGY.md
│   │   ├── README.md
│   │   └── api/main.md, handlers/*.md, services/*.md, utils/*.md  (many files)
│   ├── deployment/
│   │   └── AWS_MIGRATION.md
│   ├── dev-utils/
│   │   ├── no-need-to-run-again.sh
│   │   ├── prospective-readme.md
│   │   └── what-got-added.md
│   ├── frontend/
│   │   └── (15+ design system / component docs)
│   ├── infrastructure/
│   │   └── (10+ infra docs)
│   ├── integration/
│   │   ├── API_INTEGRATION_COMPLETE.md
│   │   └── DOCKER_INTEGRATION_COMPLETE.md
│   ├── reapplication/
│   │   └── (7 files about merging/reapplying AI coding session changes)
│   ├── tasks/
│   │   └── TASK_16..TASK_23 completion summaries
│   └── testing/
│       ├── QUICK_REFERENCE.md
│       └── README.md
│
└── _archive/                           # Old Makefile + design-docs (excluded from main tree)
```

---

## 3. CONFIG FILES (FULL CONTENT)

### backend/requirements.txt
```
fastapi==0.115.0
uvicorn[standard]==0.30.1
mangum==0.17.0
pydantic==2.9.0
python-multipart==0.0.9
```

### backend/requirements-test.txt
```
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
pytest-mock==3.12.0
moto==4.2.9
boto3-stubs[dynamodb,bedrock-runtime]==1.34.0
hypothesis==6.92.1
black==23.12.1
flake8==7.0.0
mypy==1.8.0
```

### frontend/package.json
```json
{
  "name": "moodmash-app",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest run --coverage"
  },
  "dependencies": {
    "@radix-ui/react-avatar": "^1.1.11",
    "@radix-ui/react-dropdown-menu": "^2.1.16",
    "@radix-ui/react-scroll-area": "^1.2.10",
    "@radix-ui/react-separator": "^1.1.8",
    "@radix-ui/react-slot": "^1.2.4",
    "class-variance-authority": "^0.7.1",
    "clsx": "^2.1.1",
    "framer-motion": "^11.0.5",
    "lucide-react": "^0.344.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "react-router-dom": "^6.22.0",
    "recharts": "^3.8.0",
    "tailwind-merge": "^3.5.0"
  }
}
```

### frontend/vite.config.js
```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@components': path.resolve(__dirname, './src/components'),
      '@pages': path.resolve(__dirname, './src/pages'),
      '@layouts': path.resolve(__dirname, './src/layouts'),
      '@hooks': path.resolve(__dirname, './src/hooks'),
      '@services': path.resolve(__dirname, './src/services'),
      '@utils': path.resolve(__dirname, './src/utils'),
      '@assets': path.resolve(__dirname, './src/assets'),
      '@styles': path.resolve(__dirname, './src/styles'),
      '@contexts': path.resolve(__dirname, './src/contexts'),
    },
  },
  server: {
    port: 3000,
    host: '0.0.0.0',
    proxy: {
      '/api': 'http://localhost:8000'
    }
  },
})
```

### frontend/tailwind.config.js
```js
export default {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        "border-hover": "hsl(var(--border-hover))",
        background: "hsl(var(--background))",
        surface: "hsl(var(--surface))",
        "surface-elevated": "hsl(var(--surface-elevated))",
        foreground: "hsl(var(--foreground))",
        "muted-foreground": "hsl(var(--muted-foreground))",
        "subtle-foreground": "hsl(var(--subtle-foreground))",
        accent: { DEFAULT: "hsl(var(--accent))" },
        card: { DEFAULT: "hsl(var(--card))", foreground: "hsl(var(--card-foreground))" },
      },
      borderRadius: { lg: "var(--radius)", md: "calc(var(--radius) - 2px)", sm: "calc(var(--radius) - 4px)" },
      fontFamily: { mono: ['IBM Plex Mono', 'JetBrains Mono', 'monospace'] },
      transitionTimingFunction: { 'premium': 'cubic-bezier(0.16, 1, 0.3, 1)' },
      transitionDuration: { '160': '160ms', '180': '180ms', '200': '200ms' },
      letterSpacing: { tighter: '-0.02em', tight: '-0.011em' },
      aspectRatio: { '4/5': '4 / 5' },
    },
  },
  plugins: [],
}
```

### Root .env (active)
```
USE_MOCK=true
USE_DYNAMODB=false
VITE_API_URL=http://localhost:8000
```

### frontend/.env (active)
```
VITE_API_URL=
```
Note: VITE_API_URL is intentionally empty. Frontend relies on Vite dev proxy (/api → localhost:8000). In production (Docker/nginx), the proxy doesn't exist and the empty BASE in api.js makes fetch calls go to same origin — which would fail unless backend is co-served. This is a known gap for prod deployment.

### backend/.env.example (old VibeGraph branding, full config)
References: AWS_REGION, DynamoDB tables (vibegraph-users, vibegraph-sessions, vibegraph-embedding-cache), Bedrock endpoints, CLAUDE_MODEL=anthropic.claude-3-5-sonnet-20241022-v2:0, TITAN_MODEL=amazon.titan-embed-text-v2:0, JWT, rate limiting, caching, retry config.

### frontend/.env.example (frontend, VibeGraph branded)
```
VITE_VIBEGRAPH_API_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
VITE_ENV=development
VITE_ENABLE_DARK_MODE=true
VITE_ENABLE_SOCIAL_FEATURES=true
VITE_LOG_LEVEL=info
VITE_ANALYTICS_ID=
VITE_SENTRY_DSN=
```

### docker-compose.yml
NOT PRESENT at root. The frontend has a Dockerfile. No root-level docker-compose found. References in docs mention Docker Compose but no active file exists.

---

## 4. BACKEND PYTHON FILES (FULL CONTENT)

### backend/main.py
FastAPI app. Imports all 6 function handlers. Defines Pydantic request models. Routes:
- GET /health → returns {status, mock_mode}
- POST /api/onboard → onboard.handler
- GET /api/dna/{session_id} → generate_dna.handler
- POST /api/path → get_path.handler
- POST /api/path/{path_id}/feedback → path_feedback.handler
- GET /api/analytics/{session_id} → analytics.handler
- GET /api/data/{session_id} → data_control.get_handler
- DELETE /api/data/{session_id} → data_control.delete_handler
Mangum import commented out (Lambda export disabled).
CORS: allow_origins=["*"]

### backend/lib/ai.py
Mock AI adapter. USE_MOCK env var controls routing.
- generate_taste_profile(quiz_answers) → calls archetypes.match_archetype, returns domain_scores, dominant_signals, archetype_key, style_tag
- generate_archetype(taste_signals) → returns archetype name, vibe_summary, markers, radar_scores, cross_platform_insight
- generate_growth_path(taste_signals, mood, goal, time_available, content_items) → filters content by mood/domain, filters by time, selects up to 5, sequences Absorb→Create→Reflect, fills why_love/why_grows templates
- generate_analytics_insight(stats) → template-based natural language insight based on completion rate
All live paths raise NotImplementedError("Live AI adapter not yet implemented")

### backend/lib/db.py
In-memory dict storage (_sessions, _feedback). USE_DYNAMODB env var gates DynamoDB path.
- put_session, get_session, put_path_feedback, get_path_feedback, delete_session, list_all_sessions
All DynamoDB paths raise NotImplementedError("DynamoDB adapter not yet implemented")

### backend/lib/archetypes.py
8 archetypes defined with full metadata:
- midnight_philosopher, desi_renaissance_soul, chai_minimalist, chaos_creative, analog_futurist, rhythm_seeker, the_storyteller, digital_nomad
Each has: name, vibe_summary, markers, radar_scores (5 domains: music/films/books/art/creators), cross_platform_insight, trigger_keywords (25-30 keywords each)
Functions: match_archetype(quiz_answers) → keyword scoring → returns best archetype key; get_archetype(key); all_archetype_keys()
Matching: flattens quiz answers to tokens, scores by substring match against trigger_keywords, deterministic hash tiebreaker.

### backend/lib/path_engine.py
Text-based path scoring (no embeddings).
- MOOD_TAG_MAP: maps mood names to lists of related tags
- GOAL_GROWTH_MAP: maps goal strings to lists of growth dimension tags
- WHY_LOVE_TEMPLATES: per-domain templates with {title}/{creator}/{mood} placeholders
- WHY_GROW_TEMPLATES: per-growth-dimension templates
- score_item(): weighted sum of mood tag matches + growth tag matches + domain_score * 1.5
- generate_path(): scores all items, selects within time budget (max 5), sequences absorb→create→reflect, annotates with why_love/why_grow

### backend/lib/taste_analyzer.py
Converts quiz answers to taste signals without embeddings.
- QUESTION_DOMAIN_MAP: maps question IDs to domains
- INTROSPECTION_SIGNALS, CULTURAL_SIGNALS, AMBITION_SIGNALS, AESTHETIC_SIGNALS: dict of specific option text → score (0.0-1.0)
- _compute_domain_scores(): counts answer volume per domain, normalizes
- _extract_dominant_signals(): top domain + introspection/ambition/cultural dimension signals
- analyze_quiz(): returns domain_scores, dominant_signals, introspection_depth, aesthetic_sensitivity, cultural_rootedness, ambition_orientation, consumption_breadth
NOTE: taste_analyzer.py is NOT CALLED by the current ai.py. ai.py calls archetypes.match_archetype directly. taste_analyzer.analyze_quiz() is orphaned code.

### backend/lib/vector_ops.py
```python
import math

def normalize_vector(vector):
    magnitude = math.sqrt(sum(x**2 for x in vector))
    if magnitude == 0:
        return vector
    return [x / magnitude for x in vector]

def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x**2 for x in a))
    mag_b = math.sqrt(sum(x**2 for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0
    return dot / (mag_a * mag_b)
```
NOTE: vector_ops.py is NOT CALLED anywhere in the active codebase. It is orphaned infrastructure for a future embeddings-based approach.

### backend/functions/onboard.py
- Validates quiz_answers (dict, min 1 key) and goal (non-empty str)
- Calls ai.generate_taste_profile(quiz_answers) → taste_signals
- Creates UUID session_id
- Hashes quiz_answers (sha256, for dedup) — raw answers NOT stored (privacy by design)
- Stores session: {taste_signals, goal, created_at, quiz_answers_hash}
- Returns {session_id, status: "ok"}

### backend/functions/generate_dna.py
- Gets session by session_id (404 if not found)
- If "dna" not in session: calls ai.generate_archetype(taste_signals), caches in session
- Returns {archetype, vibe_summary, markers, radar_scores, cross_platform_insight}

### backend/functions/get_path.py
- Validates session_id, mood (required)
- Loads content.json from knowledge-base/ (root-level path resolution via Path(__file__).parent.parent.parent / "knowledge-base" / "content.json")
- Falls back to session goal if not provided in request
- Calls ai.generate_growth_path(taste_signals, mood, goal, time_available, content_items)
- Returns {path_id (new UUID), items: [...]}

### backend/functions/path_feedback.py
- Validates session_id, item_id, status (must be "done"|"skipped"|"saved")
- Calls db.put_path_feedback(session_id, item_id, status, reaction)
- Returns {ok: True}

### backend/functions/analytics.py
- Counts items_done, items_skipped, items_saved from feedback
- Extracts domain from item_id prefix (e.g., "music-001" → "music")
- Computes goal_alignment_pct = items_done / total_interactions * 100
- Gets radar_scores from session dna or taste_signals
- Calls ai.generate_analytics_insight(stats) → pattern_insight string
- Returns {radar_scores, goal_alignment_pct, items_done, items_skipped, domain_breakdown, pattern_insight, spotify_connected: False}

### backend/functions/data_control.py
- get_handler: returns sanitized session data (goal, created_at, updated_at, taste_profile summary, dna summary, feedback_history) — no raw vectors/internal keys
- delete_handler: calls db.delete_session, returns {deleted: True}

### backend/__init__.py, functions/__init__.py, lib/__init__.py
Empty.

---

## 5. FRONTEND JSX/JS FILES (FULL CONTENT)

### frontend/src/main.jsx
```jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode><App /></React.StrictMode>
)
```

### frontend/src/App.jsx
React Router v6. Routes:
- / → Landing
- /onboard → OnboardingPage
- AppLayout (Sidebar + Outlet):
  - /feed → Feed
  - /dna/:id → DNACard
  - /path/:id → GrowthPath
  - /analytics/:id → Analytics
  - /data/:id → DataPanel
- * → NotFound

### frontend/src/services/api.js (PRIMARY — actively used)
```js
const BASE = import.meta.env.VITE_API_URL ?? ''

async function request(method, path, body) {
  const opts = { method, headers: { 'Content-Type': 'application/json' } }
  if (body) opts.body = JSON.stringify(body)
  const res = await fetch(`${BASE}${path}`, opts)
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`)
  return res.json()
}

export const api = {
  onboard:        (answers, goal) => request('POST', '/api/onboard', { quiz_answers: answers, goal }),
  getDNA:         (id) => request('GET', `/api/dna/${id}`),
  getPath:        (id, opts) => request('POST', '/api/path', { session_id: id, ...opts }),
  submitFeedback: (pathId, data) => request('POST', `/api/path/${pathId}/feedback`, data),
  getAnalytics:   (id) => request('GET', `/api/analytics/${id}`),
  exportData:     (id) => request('GET', `/api/data/${id}`),
  deleteData:     (id) => request('DELETE', `/api/data/${id}`),
}
```

### frontend/src/services/vibeGraphAPI.js (OLD/DEAD)
Targets entirely different API shape:
- /quiz/section1/start (POST)
- /quiz/section2/generate (POST)
- /quiz/complete (POST)
- /profile/dna/:userId (GET)
- /profile/path/:userId (GET)
- /profile/matches/:userId (GET)
- /profile/analytics/:userId (GET)
These endpoints DO NOT EXIST in the current backend. This file is a remnant from the VibeGraph era and is NOT imported anywhere in the active codebase.

### frontend/src/data/onboardingQuestions.js
7 questions (README/STATUS say 15, CONTEXT says 8, actual count is 7):
1. music_vibe — "Pick songs that match your vibe" (8 options: Prateek Kuhad, AR Rahman, etc.)
2. music_mood — "Your go-to music mood" (6 options)
3. film_picks — "Films that hit different" (8 options: Masaan, Dil Chahta Hai, etc.)
4. story_theme — "Stories you connect with" (6 options)
5. visual_style — "Your aesthetic vibe" (6 options)
6. creative_time — "In your free time, you..." (6 options)
7. books_interest — "Books that interest you" (6 options)
Wait — there's a 7th at ID content_changed: "Content that changed you" (6 options) — actual count is 7 questions.
Also exports: goalOptions array, generateTasteDNA() function (CLIENT-SIDE stub, not used in active flow — onboarding calls backend api.onboard instead).

### frontend/src/pages/Landing.jsx
Hero page. Checks sessionStorage for session_id. CTA routes to /onboard or /dna/:id.
Feature pills: Taste DNA, Growth Paths, Privacy-first.
Animated gradient blobs background.

### frontend/src/pages/Feed.jsx
Two modes:
1. No session: fetches /knowledge-base/content.json directly (browser fetch to public dir), shows 12 random items
2. With session: tries api.get(`/api/dna/${sessionId}`) — BUG: uses wrong api object (should be api.getDNA), then fetches content.json, scores items. Falls back to random 12 if error.
Grid/list toggle. Images from Unsplash source API (deprecated URL pattern). Cards click-through to external_link.

### frontend/src/components/Onboarding/OnboardingPage.jsx
State machine: 'questions' → 'goal' → 'submitting' | 'error'
Reads onboardingQuestions.js. Tracks answers as {questionId: [selectedOptions]}.
On submit: calls api.onboard(answers, selectedGoal) → stores session_id in sessionStorage → navigate to /dna/:session_id.

### frontend/src/components/Onboarding/QuestionScreen.jsx
Renders question title + option grid (2/3/4 cols responsive).
Progress bar at top. Next/Finish button (disabled until ≥1 option selected).

### frontend/src/components/DNACard/DNACard.jsx
Fetches api.getDNA(id) on mount.
Renders: archetype name (gradient text), vibe_summary, markers (tag chips), radar chart (Recharts), cross_platform_insight (if present).
Share button: copies "{archetype}\n\n{vibe_summary}" to clipboard.
CTA: "Get Your First Path" → /path/:id; "Data Controls" → /data/:id.

### frontend/src/components/GrowthPath/GrowthPath.jsx
Two phases: selection (mood + time) → path display.
Moods: focused, exploratory, melancholic, energized, calm.
Times: 15, 30, 60, 90 min.
Calls api.getPath(id, {mood, goal: 'general', time_available}).
NOTE: goal is hardcoded as 'general' — not passed from session.
For each path item: shows title, creator, engagement_type badge, domain tag, time_minutes, why_youll_love_it, why_it_grows_you.
Feedback buttons: Done/Skip/Save — calls api.submitFeedback.
Footer link to /analytics/:id.

### frontend/src/components/Analytics/Analytics.jsx
Fetches api.getAnalytics(id). Displays radar chart, goal alignment bar, done/skipped/saved counts, domain breakdown bars, AI pattern insight.

### frontend/src/components/DataPanel/DataPanel.jsx
Fetches api.exportData(id). Shows taste vector (archetype + domain scores), privacy transparency table, Export JSON button, Delete All Data button with modal confirmation.

### frontend/src/components/common/Sidebar.jsx (ACTIVE)
NavLink-based sidebar. Reads session_id from sessionStorage.
Nav items: Feed (always active), Taste DNA / Growth Path / Analytics / My Data (disabled without session).
Mobile: hamburger menu with overlay.

### frontend/src/index.css
CSS variables (dark background hsl 220 13% 9%), typography scale (text-11 through text-48), glass morphism utility (.glass), card-hover animation, glow utilities.

---

## 6. WHAT IS WORKING vs STUBBED/INCOMPLETE

### FULLY WORKING
- Onboarding flow: 7-question quiz → goal → POST /api/onboard → session_id
- Taste DNA card: GET /api/dna/:id → archetype + radar chart
- Growth Path: POST /api/path → scored & sequenced items; feedback submission
- Analytics: GET /api/analytics/:id → stats + insight text
- Data panel: export JSON + delete session
- Sidebar navigation with session-based gating
- In-memory backend (data persists only in process memory — gone on restart)
- Content loading from knowledge-base/content.json (65 items)
- Mock archetype matching (keyword scoring from quiz answers)
- Template-based "why you'll love it" / "why it grows you" generation

### STUBBED / INCOMPLETE
- **Live AI (Bedrock/Claude)**: All ai.py functions check `USE_MOCK` — if false, raise `NotImplementedError`. No real Bedrock integration exists.
- **DynamoDB**: All db.py functions check `USE_DYNAMODB` — if true, raise `NotImplementedError`.
- **taste_analyzer.py**: Fully implemented but NOT CALLED by current ai.py flow. Orphaned.
- **vector_ops.py**: Implemented but NOT CALLED anywhere. Orphaned.
- **Spotify OAuth**: Documented in CONTEXT.md, referenced everywhere, not implemented.
- **File upload (Instagram/YouTube exports)**: FileUpload component exists (not routed), no backend handler.
- **Taste-matched buddies**: In design docs only.
- **JWT authentication**: In .env.example, not implemented.
- **Session persistence**: In-memory only — all data lost on backend restart.
- **Feed personalization (with session)**: Feed.jsx attempts personalization but uses wrong api call (`api.get` instead of `api.getDNA`), so always falls back to random content.
- **external_link fields**: All content.json items have external_link: "#" — no real links.
- **Unsplash images in feed**: Uses deprecated `source.unsplash.com` URL pattern that no longer works — images will fail/fallback to gradient.
- **vibeGraphAPI.js**: Completely dead code targeting non-existent endpoints.
- **ProtectedRoute.jsx**: Exists, not used in routing.
- **AuthLayout.jsx, DashboardLayout.jsx**: Exist, not used in routing.
- **Dashboard.jsx, DiscoverList.jsx**: Pages that exist but have no routes in App.jsx.
- **FileUpload component**: Built, not connected.
- **backend/package.json**: Leftover JS artifact from old backend era, refers to `vibegraph-backend`.
- **prompts/*.prompt.md**: Prompt templates written but no backend code reads or uses them.

---

## 7. HOW FRONTEND AND BACKEND CONNECT

### Connection Method
Vite dev server proxies `/api` prefix to `http://localhost:8000`.
Frontend api.js uses `BASE = import.meta.env.VITE_API_URL ?? ''`.
In dev: VITE_API_URL is empty string, all requests go to `/api/...` → proxied to backend.
In prod (Docker): VITE_API_URL is still empty; nginx serves the SPA but there's no proxy to backend. This would cause all API calls to 404 unless backend is co-served or VITE_API_URL is set at build time.

### API Surface Alignment
frontend/src/services/api.js → backend/main.py routes:
| Frontend call | Backend route | Status |
|---|---|---|
| POST /api/onboard | POST /api/onboard | WORKS |
| GET /api/dna/:id | GET /api/dna/{session_id} | WORKS |
| POST /api/path | POST /api/path | WORKS |
| POST /api/path/:id/feedback | POST /api/path/{path_id}/feedback | WORKS |
| GET /api/analytics/:id | GET /api/analytics/{session_id} | WORKS |
| GET /api/data/:id | GET /api/data/{session_id} | WORKS |
| DELETE /api/data/:id | DELETE /api/data/{session_id} | WORKS |

### Dead API Client
vibeGraphAPI.js targets /quiz/section1/start, /quiz/section2/generate, /quiz/complete, /profile/* — none exist in backend. Not imported anywhere active.

### Knowledge Base Access
get_path.py resolves: `Path(__file__).parent.parent.parent / "knowledge-base" / "content.json"`
This resolves to the ROOT /knowledge-base/content.json when running from project root with PYTHONPATH=.
Feed.jsx fetches `/knowledge-base/content.json` from the browser — served from frontend/public/knowledge-base/content.json (a separate copy).
These are two separate copies of the content JSON. They may diverge.

### Session State
Session ID stored in browser `sessionStorage` (not localStorage — cleared on tab close).
All pages that need a session read it from sessionStorage and pass it in URL params or API calls.

---

## 8. AI/ML INTEGRATIONS AND STATUS

### Mock AI (Active)
- `USE_MOCK=true` (default, current .env)
- All AI work done in Python: keyword matching, template filling, score-based ranking
- No external API calls
- Deterministic (seeded random for path generation)
- Archetype matching: substring keyword scoring → 8 archetypes
- Path generation: mood tag + growth tag + domain score weighted scoring
- Analytics insight: template strings based on completion rate thresholds

### AWS Bedrock (Designed, Not Implemented)
- backend/lib/ai.py has `if not USE_MOCK: raise NotImplementedError("Live AI adapter not yet implemented")`
- CONTEXT.md describes intended use: Titan Embeddings (taste vector), Claude (archetype generation, path explanations, analytics)
- backend/.env.example has CLAUDE_MODEL and TITAN_MODEL defined
- No boto3 imports in current backend code
- requirements-test.txt lists `moto==4.2.9` and `boto3-stubs` for testing, but no production boto3 dependency in requirements.txt
- Prompt templates exist in /prompts/ but no backend code reads them

### AWS DynamoDB (Designed, Not Implemented)
- `USE_DYNAMODB=false` (default)
- db.py has `if USE_DYNAMODB: raise NotImplementedError("DynamoDB adapter not yet implemented")`
- Table schema documented in CONTEXT.md (taste_profiles, path_completions)

### Amazon Personalize (Mentioned in Docs Only)
- Referenced in CONTEXT.md as "production ranking layer"
- No code exists for it anywhere

### Vector Operations (Implemented, Not Called)
- vector_ops.py has cosine_similarity and normalize_vector
- taste_analyzer.py has multi-dimensional scoring
- Neither called by active code path
- Designed for embedding-based future implementation

### Unsplash API (Broken)
- Feed.jsx uses `https://source.unsplash.com/400x400/?${query}` URL pattern
- This is a deprecated Unsplash endpoint that no longer works
- Images fail and fall back to CSS gradient + hidden icon div

---

## 9. ROOT-LEVEL .md FILES

| File | First 3 lines |
|---|---|
| README.md | `# MoodMash — AI-Powered Taste Engine for India's Youth` / `> "Every platform optimizes for your attention. We optimize for your growth — through the content you already love."` / `An AI-powered personal taste engine that ingests your digital life...` |
| PROJECT_SUMMARY.md | `# MoodMash — Project Summary` / `> "Every platform optimizes for your attention..."` / `## 🎯 What Is MoodMash?` |
| STATUS.md | `# MoodMash - Current Status` / `**Last Updated**: Now` / `**Status**: ✅ READY FOR TESTING` |
| CONTEXT.md | `# PROJECT CONTEXT — [ProductName]` / `> "Every platform optimizes for your attention..."` / `This document is the single source of truth for what we're building, why, and how.` |
| DEPLOYMENT.md | `# MoodMash Deployment Guide` / (blank) / `This guide covers deploying MoodMash to production on AWS.` |
| JUDGE_FLOW.md | `# MoodMash - Judge Flow Guide` / (blank) / `## Quick Start for Judges` |
| JUDGE_QUICK_REFERENCE.md | `# MoodMash - Judge Quick Reference` / (blank) / `## 🚀 Start Here` |
| QUICKSTART.md | `# MoodMash - Quick Start Guide` / (blank) / `## 🚀 Start in 30 Seconds` |
| SIMPLIFIED_STRUCTURE.md | `# MoodMash - Simplified Structure` / (blank) / `## Overview` |
| TESTING.md | `# MoodMash Testing Guide` / (blank) / `This document provides comprehensive testing instructions for the MoodMash application.` |
| TROUBLESHOOTING.md | `# MoodMash Troubleshooting Guide` / (blank) / `## Frontend Shows Blank Page` |

---

## 10. AI CODING SESSION ARTIFACTS vs REAL DOCUMENTATION

### AI Coding Session Artifacts (generated, not hand-written)
- **docs/** directory entirely: contains 50+ markdown files that are clearly AI-generated documentation for a system that was designed but never fully built. Includes:
  - docs/backend/services/bedrockClient.md, claudeService.md, titanEmbeddingService.md, userService.md — services that don't exist in code
  - docs/backend/handlers/ — documents handlers like findMatches.md, generateEmbedding.md — don't exist
  - docs/reapplication/ — 7 files with titles like "CHANGES_TO_REAPPLY.md", "MERGE_AND_REAPPLY_GUIDE.md" — classic AI session management artifacts
  - docs/tasks/TASK_16..TASK_23 — AI task tracking output
  - docs/dev-utils/no-need-to-run-again.sh — script artifact
- **_archive/** directory: superseded design docs
- **.kiro/specs/vibegraph-backend-integration/** — Kiro (AI IDE) spec files with design.md, requirements.md, tasks.md for a Docker integration that was partially implemented
- **backend/.env.example**: branded "VibeGraph" (old name), has config for services that aren't implemented (JWT, rate limiting, embedding cache)
- **backend/package.json**: leftover from a JavaScript backend era — references `vibegraph-backend`, test scripts pointing to `tests/` directory that doesn't exist
- **frontend/src/services/vibeGraphAPI.js**: ghost of old architecture
- **CONTEXT.md**: the "[ProductName]" placeholder in line 1 reveals it's a template/AI-generated system prompt

### Real/Handwritten Documentation
- **README.md**: genuine — describes what actually works, has accurate quickstart
- **STATUS.md**: genuine — correctly lists what's working and known limitations
- **PROJECT_SUMMARY.md**: genuine product summary for judges
- **JUDGE_FLOW.md / JUDGE_QUICK_REFERENCE.md**: genuine judge guides for hackathon

### Naming Inconsistency Evidence (AI session artifact indicator)
- README says "15 questions", STATUS says "15 questions", PROJECT_SUMMARY says "8 questions", CONTEXT.md says "15-20 questions", actual code has 7 questions
- App is called "MoodMash" throughout but backend/package.json says "vibegraph-backend", .env.example has "vibegraph-" table names, docs reference "VibeGraph" — indicates multiple AI sessions with different naming conventions
- Multiple duplicate component directories: components/Onboarding/ AND components/onboarding/ (lowercase), components/Sidebar.jsx AND components/Sidebar/ AND components/common/Sidebar.jsx

---

## 11. KNOWLEDGE BASE CONTENT (STRUCTURE)

File: /knowledge-base/content.json (1042 lines, ~65 items)
Same schema in frontend/public/knowledge-base/content.json (browser-accessible copy)

Item schema:
```json
{
  "id": "music_001",
  "title": "cold/mess",
  "creator": "Prateek Kuhad",
  "domain": "music",
  "sub_domain": "indie acoustic",
  "engagement_type": "absorb",
  "mood_tags": ["introspective", "calm", "melancholic"],
  "growth_tags": ["emotional_awareness", "creative_inspiration"],
  "region": "pan-india",
  "language": "hindi-english",
  "time_minutes": 4,
  "description": "Gentle indie track perfect for reflective evenings...",
  "external_link": "#",
  "content_type": "listen"
}
```

Additional split files in frontend/public/knowledge-base/: books.json, creators.json, films.json, music.json (domain-split versions)

All external_link values are "#" — no real URLs.

---

## 12. KEY BUGS AND INCONSISTENCIES

1. **Feed.jsx personalization broken**: `const dnaResponse = await api.get(...)` — `api` object has no `.get` method, only named methods. Should be `api.getDNA(sessionId)`. This means the personalized feed never works; always falls back to random.

2. **GrowthPath goal hardcoded**: `goal: 'general'` passed to api.getPath — ignores the user's stated goal from onboarding.

3. **Content JSON duplication**: Two copies of content.json exist (root and frontend/public). Backend reads from root, frontend browser-fetches from public. These can diverge.

4. **VITE_API_URL empty in production**: frontend/.env has `VITE_API_URL=` (blank). In production Docker build, BASE will be empty string, API calls will go to same origin — needs backend co-serving or env var set at build.

5. **get_path.py reads content.json at ROOT**: path resolves 3 levels up from backend/functions/ which is correct for monorepo structure, but fragile — depends on CWD at startup.

6. **onboardingQuestions count mismatch**: Docs say 7, 8, or 15 questions. Actual: 7 questions shown to user (questions array has 7 items, but the final "goal" screen is a separate phase, making it effectively 8 steps total).

7. **feedback status mismatch**: GrowthPath.jsx sends `status: 'skip'` and `status: 'save'` but backend validates against `{"done", "skipped", "saved"}`. So skip and save feedback will 400.

8. **Unsplash images broken**: `source.unsplash.com` deprecated.

9. **taste_analyzer.py and vector_ops.py are orphaned**: Implemented but never called.

10. **vibeGraphAPI.js is dead code**: Imported by nobody, targets non-existent endpoints.

---

## 13. HACKATHON CONTEXT

- **Event**: AI for Bharat Hackathon (AWS + Hack2skill + YourStory)
- **Team**: Smooth Landing (4 members)
- **Round**: Prototype Development (final round, 3-day timeline)
- **Constraint**: Must use AWS services (Bedrock, Personalize)
- **Current AWS usage**: None in production code. Mock only.
- **Branch prod_fast**: Last commit is "hacky push to push to prod. inital test. requires cleanup and refactor"

---

## SUMMARY OF ACTUAL ARCHITECTURE STATE

```
User Browser
    │
    ├── React SPA (Vite, port 3000)
    │   ├── /onboard → 7 quiz questions → POST /api/onboard
    │   ├── /dna/:id → GET /api/dna/:id → archetype card
    │   ├── /path/:id → POST /api/path → growth items
    │   ├── /analytics/:id → GET /api/analytics/:id
    │   ├── /data/:id → GET/DELETE /api/data/:id
    │   └── /feed → browser fetch /knowledge-base/content.json (no backend)
    │
    └── FastAPI (uvicorn, port 8000)
        ├── In-memory dict storage (ephemeral)
        ├── Mock AI: keyword scoring + templates (no external calls)
        ├── Content: reads /knowledge-base/content.json at startup per request
        └── All live paths (Bedrock, DynamoDB) raise NotImplementedError
```

The app is a fully functional MVP with mock AI. It demonstrates all user flows end-to-end. The architecture is designed to swap in real AWS services but none are connected.
