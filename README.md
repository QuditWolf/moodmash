# MoodMash — AI-Powered Taste Engine for India's Youth

> **"Every platform optimizes for your attention. We optimize for your growth — through the content you already love."**

An AI-powered personal taste engine that ingests your digital life (quiz responses, Spotify history) and builds a unified cross-domain taste identity across music, books, films, fashion, art, and creators. It generates a shareable "Taste DNA" card and creates progressive Growth Paths that blend Absorb → Create → Reflect steps.

---

## For Judges: Quick Start

**Time Required**: 5-7 minutes
**No sign-up needed**

### The 4 Flows to Test:

1. **Onboarding → DNA Card** (2-3 min)
   - Answer 15 questions about Indian music, films, books, art
   - Get AI-generated Taste DNA with unique archetype
   - See radar chart across 5 domains

2. **Mindful Path** (2-3 min)
   - Select mood + time available
   - Get "Tonight's Path" with 3-5 curated items
   - Each item explains WHY you'll love it + WHY it grows you

3. **Feed** (1-2 min)
   - Instagram-style grid of personalized content
   - 18 cards ranked by your taste DNA
   - Hover effects and interactions

4. **Data Controls** (1-2 min)
   - View your anonymized taste vector
   - See "What We Store vs Don't Store"
   - Export/delete your data

**See [JUDGE_QUICK_REFERENCE.md](JUDGE_QUICK_REFERENCE.md) for detailed testing guide.**

---

## Features

1. **Taste Onboarding** — 15 emotionally resonant questions across 5 domains (music, films, visual, creative, consumption)
2. **Taste DNA Card** — AI-generated archetype with name, vibe summary, radar chart, and taste markers
3. **Growth Paths** — Curated 3-5 item journeys with Absorb/Create/Reflect engagement types
4. **Analytics Dashboard** — Goal alignment scores, domain breakdown, and AI-generated insights
5. **Privacy Data Control** — Export and delete your data, DPDP Act 2023 compliant

## Architecture

- **Frontend**: React 18 + Vite + Tailwind CSS + Recharts
- **Backend**: FastAPI (Python) + Uvicorn
- **AI**: Mock adapter (swappable to AWS Bedrock)
- **Database**: In-memory (swappable to DynamoDB)
- **Content**: 65+ curated items (70%+ Indian content)

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   cd moodmash
   ```

2. **Set up Python virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

4. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

5. **Install root dependencies (for concurrent dev servers)**
   ```bash
   npm install
   ```

6. **Create .env file**
   ```bash
   cp .env.example .env
   ```

### Running the Application

**Option 1: Run both servers with one command (recommended)**
```bash
npm run dev
```

This starts:
- Frontend on http://localhost:3000
- Backend on http://localhost:8000

**Option 2: Run servers separately**

Terminal 1 (Backend):
```bash
source venv/bin/activate
PYTHONPATH=. uvicorn backend.main:app --reload --port 8000
```

Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```

### Testing the API

Run the test script to verify all endpoints:
```bash
python3 test_api.py
```

Expected output:
```
✓ Health check passed
✓ Onboard passed
✓ DNA generation passed
✓ Growth path passed
✓ Analytics passed
All API tests passed!
```

## Project Structure

```
moodmash/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/       # UI components
│   │   │   ├── Onboarding/   # Quiz flow
│   │   │   ├── DNACard/      # Taste DNA display
│   │   │   ├── GrowthPath/   # Path recommendations
│   │   │   ├── Analytics/    # Dashboard
│   │   │   ├── DataPanel/    # Privacy controls
│   │   │   └── common/       # Shared components
│   │   ├── pages/            # Route pages
│   │   ├── services/         # API client
│   │   └── data/             # Quiz questions
│   └── package.json
│
├── backend/                  # FastAPI backend
│   ├── functions/            # API handlers
│   │   ├── onboard.py
│   │   ├── generate_dna.py
│   │   ├── get_path.py
│   │   ├── path_feedback.py
│   │   ├── analytics.py
│   │   └── data_control.py
│   ├── lib/                  # Shared utilities
│   │   ├── ai.py             # AI adapter (mock/Bedrock)
│   │   ├── db.py             # DB adapter (in-memory/DynamoDB)
│   │   ├── archetypes.py     # 8 Indian archetypes
│   │   ├── path_engine.py    # Path generation logic
│   │   └── taste_analyzer.py # Quiz analysis
│   ├── main.py               # FastAPI app
│   └── requirements.txt
│
├── knowledge-base/           # Content catalog
│   └── content.json          # 65+ curated items
│
├── prompts/                  # AI prompt templates
│   ├── dna.prompt.md
│   ├── path.prompt.md
│   └── analytics.prompt.md
│
└── test_api.py               # API test script
```

## User Flow

1. **Landing** (`/`) → Clean hero with value prop + CTA
2. **Onboarding** (`/onboard`) → 15 questions + goal selection
3. **Taste DNA** (`/dna/:id`) → Archetype card with radar chart
4. **Growth Path** (`/path/:id`) → Mood/time selector → curated items
5. **Analytics** (`/analytics/:id`) → Goal alignment + domain breakdown
6. **Data Panel** (`/data/:id`) → Export/delete data controls

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/api/onboard` | Submit quiz answers → get session_id |
| GET | `/api/dna/:id` | Get taste DNA card data |
| POST | `/api/path` | Generate growth path |
| POST | `/api/path/:id/feedback` | Submit item feedback |
| GET | `/api/analytics/:id` | Get analytics data |
| GET | `/api/data/:id` | Export user data |
| DELETE | `/api/data/:id` | Delete user data |

## Testing

### Manual Testing Flow

1. Visit http://localhost:3000
2. Click "Discover Your Taste DNA"
3. Answer 15 quiz questions
4. Select your north star goal
5. View your generated Taste DNA card
6. Click "Enter Growth Path"
7. Select mood and time available
8. Get your curated path
9. Mark items as Done/Skip/Save
10. View Analytics
11. Check Data Panel

### API Testing

```bash
# Test health
curl http://localhost:8000/health

# Test onboard
curl -X POST http://localhost:8000/api/onboard \
  -H "Content-Type: application/json" \
  -d '{"quiz_answers": {"music_album": ["Prateek Kuhad"]}, "goal": "Build something"}'

# Test DNA (replace SESSION_ID)
curl http://localhost:8000/api/dna/SESSION_ID
```

## Switching to AWS

### Enable Bedrock AI

1. Update `.env`:
   ```
   USE_MOCK=false
   AWS_REGION=ap-south-1
   ```

2. Configure AWS credentials:
   ```bash
   aws configure
   ```

3. The `backend/lib/ai.py` will automatically route to Bedrock

### Enable DynamoDB

1. Update `.env`:
   ```
   USE_DYNAMODB=true
   DYNAMODB_TABLE_SESSIONS=taste_profiles
   DYNAMODB_TABLE_COMPLETIONS=path_completions
   ```

2. Create tables using `backend/template.yaml` (SAM)

## Design Principles

1. **Direction over discovery** — We help you know what to DO with your time
2. **Productive rest** — Entertainment and growth are fused
3. **Identity over recommendations** — The viral hook is "who you are"
4. **User agency** — You see your patterns and make conscious choices
5. **Indian-first** — Content, personas, cultural references built for India

## Privacy

- Raw quiz answers are hashed and discarded immediately
- Only anonymized taste vectors are stored
- No PII, no tracking, no surveillance
- Users can export and delete all data
- Aligned with India's DPDP Act 2023

## Environment Variables

```bash
# Backend
USE_MOCK=true                    # Use mock AI (true) or Bedrock (false)
USE_DYNAMODB=false               # Use in-memory (false) or DynamoDB (true)
AWS_REGION=ap-south-1            # AWS region for Bedrock/DynamoDB

# Frontend
VITE_API_URL=http://localhost:8000  # Backend API URL
```

## Troubleshooting

### Backend won't start
```bash
# Ensure venv is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r backend/requirements.txt

# Check Python version
python --version  # Should be 3.10+
```

### Frontend won't start
```bash
# Clear node_modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### CORS errors
- Ensure backend is running on port 8000
- Check `frontend/vite.config.js` proxy settings
- Verify `.env` has correct `VITE_API_URL`

### API returns 404
- Check backend logs for errors
- Verify PYTHONPATH is set: `PYTHONPATH=. uvicorn backend.main:app`
- Ensure all handler files exist in `backend/functions/`

## Deployment

### Frontend (AWS Amplify)
```bash
cd frontend
npm run build
# Upload dist/ to Amplify
```

### Backend (AWS Lambda + API Gateway)
```bash
# Install SAM CLI
pip install aws-sam-cli

# Build and deploy
sam build
sam deploy --guided
```

## License

MIT License - see LICENSE file for details

## Acknowledgments

Built for the AI for Bharat Hackathon by Team Smooth Landing.

Special thanks to:
- Indian artists, musicians, filmmakers, and creators featured in our knowledge base
- The open-source community for amazing tools and libraries

---

**Made with love for India's youth**
