# PROJECT CONTEXT — [ProductName]

> **"Every platform optimizes for your attention. We optimize for your growth — through the content you already love."**

This document is the single source of truth for what we're building, why, and how. Use it as context for every coding decision.

---

## WHAT IS THIS PROJECT?

An AI-powered personal taste engine for India's youth that:

1. **Ingests your digital life** (Spotify history, Instagram exports, YouTube exports, + a taste quiz) and builds a **unified cross-domain taste identity** across music, books, films, fashion, art, and creators.
2. **Generates a shareable "Taste DNA" card** — an AI-created archetype with name, visual radar chart, and personality summary. This is the viral hook (think Spotify Wrapped for your entire identity).
3. **Creates progressive Growth Paths** — not playlists. Structured journeys that blend **Absorb → Create → Reflect** steps, fusing entertainment with personal growth toward user-stated goals.
4. **Provides a personal analytics dashboard** — showing users their own consumption patterns across platforms, dopamine loops, goal alignment scores, and taste evolution over time. The user controls their algorithm, not the other way around.
5. **Matches users with taste-aligned growth buddies** — anonymized, privacy-respecting, matched on taste + goals + consumption style.
6. **Is privacy-first by design** — raw data is processed into anonymized taste embeddings and immediately discarded. Users can view, export, and delete their data at any time.

### The Core Insight

India's 300M+ young internet users spend 4+ hours daily on fragmented platforms that optimize for attention, not growth. Their taste is split across 10 apps (Spotify, Instagram, YouTube, Netflix, etc.) and no one connects those signals into a unified understanding of WHO they are or WHERE they're going. Their rest time and growth time are completely disconnected.

We fix this by building the unified taste graph that no single platform can build alone, then using it to guide intentional consumption where entertainment IS development.

---

## HACKATHON CONTEXT

- **Event:** AI for Bharat Hackathon (AWS + Hack2skill + YourStory)
- **Team:** Smooth Landing (4 members)
- **Round:** Prototype Development (final round)
- **Timeline:** ~3 days
- **Constraint:** Must use AWS services (especially Bedrock, Personalize)
- **Evaluation order:** PPT → Demo Video → Working Prototype → GitHub Review

### What Judges Care About

1. **Is the AI real?** Bedrock must do actual generative work, not just sit in a diagram.
2. **Is it valuable for Indian youth?** Indian content, Indian personas, Indian problem framing.
3. **Is the architecture sound?** AWS-native, serverless, scalable patterns.
4. **Is the privacy story genuine?** Can you explain what's stored vs. what isn't?
5. **Does the prototype work?** Judges will click the link and try it.

---

## MVP SCOPE — WHAT WE'RE ACTUALLY BUILDING

### Must-Build Features

#### Feature 1: Taste Onboarding (Two Input Paths)

**Path A: Quick Quiz (3 minutes)**
- 15-20 swipe/select questions across 5 domains (music, books, films, fashion/art, goals)
- Questions are emotionally resonant, NOT genre checkboxes
  - "Pick the album cover that feels like your Sunday morning"
  - "Which book title would you pick up without reading the description?"
  - "You're decorating your room — which vibe?"
  - "Pick the film still that makes you feel something"
- Content in questions is **Indian-first** (AR Rahman + Radiohead, Arundhati Roy + Murakami, Sabyasachi + minimalism)
- Ends with North Star goal selection: creative career / tech skills / wellness / entrepreneurship / cultural roots / "just inspire me"

**Path B: Connect Spotify**
- OAuth flow with Spotify API
- Pull: top artists, top tracks, listening history, genre distribution
- Parse into structured taste signals
- User can do Path A + Path B together for richer profiling

**Path C (Stretch): Upload Data Exports**
- Instagram: user uploads their JSON data export → we parse saves, engagement patterns
- YouTube: user uploads watch history JSON → we parse viewing patterns
- These are file upload + parse flows, not API integrations

**Output:** All inputs (quiz answers + platform data) are sent to Bedrock to generate a unified taste embedding.

#### Feature 2: Taste DNA Card Generation

**Input:** Taste embedding from onboarding

**Bedrock generates:**
- **Archetype name:** Creative, memorable names like "Midnight Philosopher", "Desi Renaissance Soul", "Chaos Creative", "Analog Futurist"
- **Vibe summary:** 2-3 line AI description — "You chase depth over trend. Your playlists have more feelings than most people's journals."
- **Cross-platform insight** (if Spotify connected): "Your Spotify says indie-melancholic. Your quiz says minimalist design lover. You're a pattern-seeker who relaxes through aesthetics."
- **Top taste markers:** 5-7 defining tags across domains
- **Radar chart data:** Scores across 5 domains for visual display

**Frontend renders:**
- Visually stunning card with archetype, summary, radar chart, markers
- Share button (copies link or generates shareable image)
- This card is the **viral engine** — people share identity

#### Feature 3: Growth Path Recommendations

**Input:** Taste embedding + mood selection + time available + goal

**Path structure — each item has an engagement type:**
- **🎧 Absorb** — listen, watch, read (passive but intentional)
- **✏️ Create** — sketch, write, record, build something inspired by what you absorbed
- **💭 Reflect** — journal prompt, self-assessment, connect the dots

**Output:** 3-5 sequenced items from the content knowledge base, each with:
- Title + creator
- Domain tag (music / film / article / exercise / reflection)
- Engagement type (Absorb / Create / Reflect)
- "Why you'll love it" (taste match explanation)
- "Why it grows you" (goal alignment explanation)
- External link (where to consume it)

**Completion tracking per item:**
- ✅ Done / ⏭️ Skipped / 🔖 Saved for Later
- Optional reaction: "hit different" / "meh" / "not for me"
- This feeds back into future recommendations

**Technical:** Bedrock Agent with RAG over the content knowledge base in S3. Personalize for ranking (or Bedrock-only ranking as fallback).

#### Feature 4: Analytics Dashboard (Simplified for MVP)

- **Taste radar over time** (even if "over time" is just current session for MVP)
- **Spotify breakdown** (if connected): top genres, listening pattern summary, cross-referenced with quiz answers
- **Completed paths count + items consumed/created/reflected**
- **Goal alignment indicator:** "X% of your consumption this session aligned with your stated goal"
- **Pattern insight:** One AI-generated observation about the user's taste/consumption

**Full vision (show in PPT, not required in MVP):**
- Cross-platform time map
- Dopamine audit (passive vs. intentional consumption ratio)
- Taste evolution tracking over weeks
- Weekly "Growth Pulse" reports

#### Feature 5: Privacy Data Control Panel

- "Your Taste Vector (Anonymized)" — visual representation
- "What We Store vs. What We Don't" — clear comparison
- Export My Data button → downloads taste vector as JSON
- Delete My Data button → clears from DynamoDB
- DPDP Act 2023 reference

### Nice-to-Have (Only If Time Permits)

#### Feature 6: Taste-Matched Buddies (Lite)
- Display 3-5 anonymized profiles with similarity scores
- Matched on 3 dimensions: taste overlap + goal alignment + consumption style
- No chat, no accounts — just the matching display

### Explicitly NOT Building

- User accounts / login (session-based only)
- Full communities / vibe spaces
- Moodboard creation
- Events
- Real-time features
- Mobile app (web only, mobile-responsive)

---

## TECHNICAL ARCHITECTURE

### Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React (Vite) | Web UI — onboarding, DNA card, paths, analytics, data panel |
| Hosting | AWS Amplify | Frontend deployment |
| API | Amazon API Gateway + AWS Lambda | Serverless REST endpoints |
| AI — Embeddings | Amazon Bedrock (Titan Embeddings) | Generate taste embedding vectors from multi-source inputs |
| AI — Generative | Amazon Bedrock (Claude) | Archetype generation, path creation (RAG), analytics insights |
| AI — Ranking | Amazon Personalize | Rank content candidates by predicted engagement |
| Data — Users | Amazon DynamoDB | Taste vectors, session data, completion records |
| Data — Content | Amazon S3 | Content knowledge base (JSON), generated assets |
| Data Ingestion | Lambda + Spotify API | OAuth flow + parse listening data |
| Dev Workflow | Kiro | Spec-driven development |

### API Endpoints

```
POST /api/onboard          — Submit quiz answers → returns session_id + taste_embedding_id
POST /api/connect-spotify  — OAuth callback → pull Spotify data → enrich embedding
POST /api/upload-export    — Upload Instagram/YouTube JSON → parse → enrich embedding
GET  /api/dna/:id          — Get DNA card data (archetype, summary, radar, markers)
POST /api/path             — Get growth path (mood, time, goal → sequenced items)
POST /api/path/:id/feedback — Submit completion/reaction for a path item
GET  /api/analytics/:id    — Get analytics dashboard data
GET  /api/data/:id         — Export user data (taste vector JSON)
DELETE /api/data/:id       — Delete all user data
```

### AI Pipeline Flows

**Flow 1: Onboarding → Embedding**
```
User quiz answers + Spotify data (optional)
  → Lambda: normalize all inputs into structured taste signals
  → Bedrock Titan: generate unified taste embedding vector
  → Store embedding in DynamoDB (discard raw inputs — privacy)
  → Return: session_id + embedding_id
```

**Flow 2: Embedding → DNA Card**
```
Taste embedding from DynamoDB
  → Bedrock Claude: generate archetype name + vibe summary + markers
  → If Spotify connected: generate cross-platform insight
  → Return: JSON with all card data + radar chart scores
  → Frontend renders the visual card
```

**Flow 3: Path Generation**
```
Taste embedding + mood + time_available + goal
  → Bedrock Agent: query S3 knowledge base via RAG
  → Retrieve candidate items matching taste + mood + goal
  → Personalize (or Bedrock fallback): rank candidates
  → Bedrock Claude: sequence items as Absorb→Create→Reflect flow
  → Bedrock Claude: generate per-item explanations (why you'll love it + why it grows you)
  → Return: ordered list of 3-5 items with full metadata
```

**Flow 4: Analytics**
```
Taste embedding + connected platform data + completion history
  → Lambda: compute taste radar scores, goal alignment %, completion stats
  → Bedrock Claude: generate 1-2 pattern insights in natural language
  → Return: JSON with all analytics data
```

### Privacy Pipeline (Critical — This Is Our Differentiator)

```
1. User provides raw data (quiz answers, Spotify history, uploads)
2. Lambda processes into taste embedding vector
3. Raw data is IMMEDIATELY DISCARDED — never written to persistent storage
4. Only the anonymized embedding vector is stored in DynamoDB
5. All recommendations computed on vectors, not personal data
6. Taste matching uses cosine similarity on anonymized vectors
7. User can view, export, or delete their vector at any time
```

**Principle:** "We know what you'll love without knowing who you are."

### DynamoDB Table Design

```
Table: taste_profiles
  PK: session_id (string)
  embedding_vector: list<number>    — the anonymized taste embedding
  archetype: string                 — generated archetype name
  goal: string                      — user's stated growth goal
  radar_scores: map                 — {music: 0.8, books: 0.6, films: 0.9, fashion: 0.4, art: 0.7}
  created_at: string (ISO 8601)
  spotify_connected: boolean
  TTL: number                       — auto-expire sessions after 7 days

Table: path_completions
  PK: session_id (string)
  SK: path_item_id (string)
  status: string                    — "done" | "skipped" | "saved"
  reaction: string                  — "hit_different" | "meh" | "not_for_me" | null
  completed_at: string (ISO 8601)
```

### Content Knowledge Base Schema (S3)

Each item in `/knowledge-base/content.json`:

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
  "description": "Gentle indie track perfect for reflective evenings",
  "external_link": "https://open.spotify.com/...",
  "content_type": "listen"
}
```

Engagement types: `absorb` (listen/watch/read), `create` (make something), `reflect` (think/journal/assess)

Domain distribution target: ~200-300 items total
- Music: 40-50 (Indian genres: classical, indie, Bollywood, regional, EDM, hip-hop)
- Books/Articles: 40-50 (Indian authors, essays, design writing, startup stories)
- Films/Series: 40-50 (Satyajit Ray, Zoya Akhtar, indie Indian, documentaries)
- Fashion/Art/Design: 30-40 (Indian designers, contemporary art, design studios)
- YouTube/Creators/Skills: 30-40 (Indian tech creators, cultural docs, skill tutorials)
- Exercises/Prompts: 20-30 (creative exercises, journal prompts, design challenges)

---

## PROJECT STRUCTURE

```
/
├── frontend/                     # React (Vite) app
│   ├── src/
│   │   ├── components/
│   │   │   ├── Onboarding/       # Swipe quiz UI + Spotify connect
│   │   │   ├── DNACard/          # Taste DNA card display + share
│   │   │   ├── GrowthPath/       # Path display with Absorb/Create/Reflect
│   │   │   ├── Analytics/        # Dashboard with charts + insights
│   │   │   ├── DataPanel/        # Privacy data control
│   │   │   └── common/           # Shared UI components
│   │   ├── hooks/                # Custom React hooks
│   │   ├── services/             # API client functions
│   │   ├── utils/                # Helpers, constants
│   │   └── App.jsx               # Main app with routing
│   ├── public/
│   └── package.json
│
├── backend/                      # Lambda functions
│   ├── functions/
│   │   ├── onboard/              # Process quiz → generate embedding
│   │   ├── connect-spotify/      # Spotify OAuth + data pull
│   │   ├── upload-export/        # Parse Instagram/YouTube exports
│   │   ├── generate-dna/         # Create archetype via Bedrock
│   │   ├── get-path/             # RAG pipeline for growth paths
│   │   ├── path-feedback/        # Store completion/reaction
│   │   ├── analytics/            # Compute dashboard data
│   │   └── data-control/         # Export + delete user data
│   ├── lib/                      # Shared utilities (Bedrock client, DynamoDB helpers)
│   └── template.yaml             # SAM/CloudFormation template
│
├── knowledge-base/               # Content catalog
│   ├── content.json              # All 200+ curated items
│   └── README.md                 # Schema docs + curation guidelines
│
├── prompts/                      # All Bedrock prompt templates
│   ├── taste-embedding.md        # How to analyze multi-source inputs into taste signals
│   ├── archetype-generation.md   # DNA card: archetype name + summary + markers
│   ├── path-generation.md        # Growth path: item selection + sequencing + explanations
│   ├── analytics-insights.md     # Pattern observation generation
│   └── README.md                 # Prompt engineering notes + iteration log
│
├── docs/                         # Documentation
│   ├── architecture.md           # System architecture diagram description
│   ├── api-contracts.md          # Full API specification
│   └── privacy-design.md         # Privacy pipeline documentation
│
├── CONTEXT.md                    # THIS FILE — project context for AI assistants
└── README.md                     # Project overview for GitHub
```

---

## DESIGN PRINCIPLES

### Product Principles

1. **Direction over discovery.** We don't help you find more content. We help you know what to DO with your time.
2. **Productive rest.** Entertainment and growth are fused, not separated. The user thinks they're relaxing; they're actually developing.
3. **Identity over recommendations.** The viral hook is "who you are" (Taste DNA), not "what you should watch."
4. **User agency over algorithmic control.** The analytics dashboard exists so the user sees their own patterns and makes conscious choices. We're a tool, not a trap.
5. **Indian-first.** Content, personas, cultural references, regional understanding — all built for India's youth first.

### Technical Principles

1. **Privacy by design, not by policy.** Raw data is architecturally unable to persist. It's not that we promise not to store it — it's that the system discards it before it could be stored.
2. **AI does real work.** Every Bedrock call has a specific, demonstrable purpose. No decorative AI.
3. **Serverless everything.** Lambda + API Gateway + DynamoDB + S3. No servers to manage. Scales to zero, scales to millions.
4. **Prompt engineering is product engineering.** The `/prompts` directory is as important as the `/frontend` directory. The quality of Bedrock outputs IS the product quality.
5. **Honest MVP.** No fake data, no fake engagement metrics, no features that don't work. What we demo is what works.

### UI/UX Principles

1. **The DNA card must be beautiful enough to share.** If it doesn't look stunning, the viral loop dies.
2. **Growth paths must feel like an experience, not a search results page.** Sequenced, visually distinct (Absorb/Create/Reflect have different visual treatments), with clear explanations.
3. **Analytics should empower, not shame.** "Here's your pattern" not "you wasted 47 hours." Neutral, insightful, actionable.
4. **Mobile-first responsive.** Indian youth are mobile-first. Test on mobile before desktop.
5. **Fast.** Onboarding must feel snappy. DNA card generation can have a loading state (AI is thinking) but should feel intentional, not slow.

---

## IMPORTANT IMPLEMENTATION NOTES

### Bedrock Usage

- Use **Titan Embeddings** for taste vector generation (this is the core embedding model)
- Use **Claude on Bedrock** for all generative tasks (archetype naming, path explanations, analytics insights)
- For RAG: use Bedrock Knowledge Bases with the S3 content catalog, or implement manual RAG with embedding similarity search
- All Bedrock calls go through Lambda — never call Bedrock directly from frontend

### Spotify Integration

- Use Spotify Web API: `/v1/me/top/artists`, `/v1/me/top/tracks`, `/v1/me/player/recently-played`
- OAuth 2.0 PKCE flow (since we're a web app)
- Scopes needed: `user-top-read`, `user-read-recently-played`
- Parse into: top 5 genres, top 10 artists, listening time distribution, mood indicators
- After parsing, discard raw Spotify data — only keep the derived taste signals that feed into the embedding

### Personalize Fallback

- Amazon Personalize requires training data and time to set up. If it's not ready in time:
- **Fallback:** Use Bedrock to rank content items by taste similarity (embed content items + cosine similarity with user embedding)
- In PPT: mention Personalize as the production ranking layer. In MVP: Bedrock-only ranking is acceptable.

### Content Knowledge Base

- Stored as a single JSON file in S3 (or split by domain if large)
- 200-300 items, 70%+ Indian content
- Each item tagged with: domain, engagement_type (absorb/create/reflect), mood_tags, growth_tags, region, language, time_minutes
- For RAG: items are embedded using Titan Embeddings and stored alongside their metadata
- Exercises and reflection prompts are content items too — tagged with `engagement_type: "create"` or `"reflect"`

### Session Management

- No user accounts for MVP. Use session IDs (UUID generated on first visit, stored in browser cookie/state).
- Session auto-expires after 7 days (DynamoDB TTL).
- All data tied to session_id, not any PII.

---

## WHAT SUCCESS LOOKS LIKE

When a judge clicks our prototype link:

1. They land on a clean, compelling landing page that communicates the value in 5 seconds.
2. They start the onboarding quiz — questions feel fresh, emotionally engaging, Indian-cultural.
3. Optionally they connect Spotify — and see their real data being pulled in (wow moment).
4. They get their Taste DNA card — the archetype name makes them smile, the summary feels accurate, they want to share it.
5. They request a Growth Path — the items feel curated, not random. The Absorb→Create→Reflect structure feels intentional. The explanations show the AI understands them.
6. They mark items as done — they see it reflected.
7. They check the analytics — even basic, it shows them something they didn't know about their own taste.
8. They check the data panel — they see exactly what's stored, and can delete it. They think "this is how it should be."
9. They go to the PPT — the architecture makes sense, the privacy story is credible, the Bharat angle is genuine.
10. They think: "This team actually built something meaningful in 3 days."
