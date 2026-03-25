# MoodMash - Judge Flow Guide

## Quick Start for Judges

**URL**: http://localhost:3000

**Time Required**: 5-7 minutes for complete flow

---

## Flow 1: Onboarding → DNA Card

### Step 1: Landing Page
- Judge lands on the app
- Sees value proposition: "Every platform optimizes for your attention. We optimize for your growth."
- Clicks **"Discover Your Taste DNA"** button

### Step 2: Onboarding Quiz (15 questions)
Questions are designed around Indian cultural content:

**Music Questions:**
- "Pick songs you vibe with" (Prateek Kuhad, AR Rahman, Ritviz, etc.)
- "What do you listen to at 3 AM?" (Lo-fi beats, Sufi, Indie acoustic)
- "Music that makes you feel alive" (Electronic, Folk fusion, Hip-hop)

**Film Questions:**
- "Films that hit different" (Masaan, Ship of Theseus, Tumbbad)
- "What kind of stories pull you in?" (Character-driven, Experimental, Regional)
- "Documentaries you'd watch" (Social issues, Art & culture, Science)

**Books Questions:**
- "Book covers that attract you" (Poetry, Essays, Fiction)
- "What do you read to grow?" (Philosophy, Biographies, Self-help)

**Art & Culture:**
- "Art that speaks to you" (Street art, Digital art, Traditional)
- "Creators you follow" (Musicians, Filmmakers, Writers)

**Interaction:**
- Swipe/select multiple options per question
- Progress bar shows completion
- Can go back to previous questions

### Step 3: Goal Selection
After 15 questions, judge selects their north star:
- "Build something that matters"
- "Get technically excellent"
- "Find what makes me happy"
- "Start something of my own"
- "Understand where I come from"
- "Just inspire me and see what emerges"

### Step 4: DNA Card Generation
AI generates a personalized Taste DNA card with:

**Archetype Name** (one of 8 Indian archetypes):
- Midnight Philosopher
- Desi Renaissance Soul
- Chai Minimalist
- Chaos Creative
- Analog Futurist
- Rhythm Seeker
- The Storyteller
- Digital Nomad

**Vibe Summary:**
- 2-3 sentence description of their taste personality
- Written in relatable, Indian youth language

**Radar Chart:**
- 5 domains: Music, Films, Books, Art, Creators
- Visual representation of taste distribution

**Taste Markers:**
- 5-7 specific tags (e.g., "introspective", "experimental", "rooted")

**Share Button:**
- Copies archetype name and vibe summary to clipboard
- Shows "Copied!" confirmation

**Next Steps:**
- Primary CTA: **"Get Your First Path"**
- Secondary links: "Explore Feed" | "Data Controls"

---

## Flow 2: Mindful Path (Tonight's Path)

### Step 1: Path Setup
After DNA card, judge clicks **"Get Your First Path"**

### Step 2: Mood Selection
Judge selects current mood:
- **focused** - For deep work or concentration
- **exploratory** - For discovering new things
- **melancholic** - For introspective moments
- **energized** - For high-energy activities
- **calm** - For relaxation and unwinding

### Step 3: Time Selection
Judge selects available time:
- **15min** - Quick break
- **30min** - Short session
- **60min** - Full hour
- **90min** - Deep dive

### Step 4: Path Generation
AI returns "Tonight's Path" with 3-5 items across domains:

**Each Item Shows:**

1. **Title & Creator**
   - e.g., "cold/mess" by Prateek Kuhad

2. **Domain Tag**
   - Music, Film, Literature, Art

3. **Engagement Type Badge** (color-coded):
   - 🎧 **Absorb** (blue) - Listen, watch, read
   - ✏️ **Create** (amber) - Make something
   - 💭 **Reflect** (purple) - Journal, think

4. **Time Estimate**
   - e.g., "4min", "15min", "30min"

5. **Why You'll Love It**
   - One-line AI explanation of personal fit
   - e.g., "Gentle indie track perfect for reflective evenings"

6. **Why It Grows You**
   - One-line AI explanation of growth value
   - e.g., "Builds emotional awareness through honest lyrics"

7. **Action Buttons:**
   - ✓ **Done** - Mark as completed
   - ⏭ **Skip** - Not interested
   - 🔖 **Save** - Save for later

**Example Path (calm / 30min):**
1. Song while working: "Kasoor" by Prateek Kuhad (4min, Absorb)
2. Short film to relax: "Ahalya" (14min, Absorb)
3. Poem to reflect: "Where the Mind is Without Fear" (2min, Reflect)
4. Journal prompt: "What made you feel alive today?" (10min, Create)

### Step 5: Path Completion
- Judge interacts with items (Done/Skip/Save)
- Feedback is recorded for future personalization
- Link to **"View Analytics"** at bottom

---

## Flow 3: Data Control Panel

### Access
- From DNA card: Click "Data Controls" link
- From sidebar: Click "My Data"

### What's Shown

**1. Your Taste Vector (Anonymized)**
- Archetype name
- Domain scores (Music: 0.85, Films: 0.72, etc.)
- Visual representation of taste distribution

**2. What We Store vs What We Don't**

**We Store:**
- Anonymized taste vector
- Archetype
- Goal
- Path completions

**We Don't Store:**
- Quiz answers (discarded after DNA generation)
- Spotify raw data
- Personal info
- Browsing history

**3. Action Buttons:**

**Export My Data:**
- Downloads JSON file with all stored data
- Filename: `moodmash-data-{session_id}.json`
- Includes: archetype, radar scores, interactions

**Delete My Data:**
- Shows confirmation modal with warning
- Permanently deletes all data
- Redirects to landing page
- Cannot be undone

**4. Legal Reference:**
- "Aligned with India's Digital Personal Data Protection Act, 2023"

---

## Flow 4: Feed (Instagram Explore Style)

### Access
- From DNA card: Click "Explore Feed"
- From sidebar: Click "Feed"

### What's Shown

**For Guests (No Session):**
- 12 random content cards from knowledge base
- Banner: "Complete your taste onboarding to get personalized recommendations"
- CTA: "Start Onboarding"

**For Logged-In Users:**
- 18 personalized content cards
- Smart scoring based on:
  - Taste DNA markers
  - Growth alignment
  - Archetype preferences
- Header: "Your Feed - Content curated based on your taste DNA"

**Card Layout (Instagram-style Grid):**
- 3 columns on desktop
- 2 columns on tablet
- 1 column on mobile
- Responsive masonry-style layout

**Each Card Shows:**
1. **Domain Icon** (top section)
   - Music: 🎵 icon
   - Film: 🎬 icon
   - Literature: 📖 icon
   - Art: 🎨 icon

2. **Engagement Type Badge**
   - Color-coded (Absorb/Create/Reflect)

3. **Domain Label**
   - Small uppercase text

4. **Title & Creator**
   - Bold title
   - Creator name below

5. **Description**
   - 2-line truncated description
   - Hover to see full text

6. **Mood Tags**
   - Up to 3 tags (e.g., "introspective", "calm", "melancholic")

**Interactions:**
- Hover: Card lifts slightly, background lightens
- Click: Opens external link (if available)
- View toggle: Switch between grid and list view

---

## Complete Judge Flow (5-7 minutes)

### Minute 0-2: Onboarding
1. Land on app (0:00)
2. Click "Discover Your Taste DNA" (0:05)
3. Answer 15 questions (0:10 - 2:00)
4. Select goal (2:00 - 2:15)
5. Wait for DNA generation (2:15 - 2:30)

### Minute 2-3: DNA Card
1. View archetype and vibe summary (2:30 - 2:45)
2. See radar chart and taste markers (2:45 - 3:00)
3. Click "Share" to test copy functionality (3:00 - 3:05)

### Minute 3-5: Growth Path
1. Click "Get Your First Path" (3:05)
2. Select mood (e.g., "calm") (3:10)
3. Select time (e.g., "30min") (3:15)
4. Click "Get My Path" (3:20)
5. View 3-5 curated items (3:25 - 4:30)
6. Test Done/Skip/Save buttons (4:30 - 4:45)

### Minute 5-6: Feed
1. Click "Explore Feed" from DNA card (4:45)
2. Scroll through personalized cards (4:50 - 5:30)
3. Toggle between grid and list view (5:30 - 5:40)
4. Click a card to see interaction (5:40 - 5:50)

### Minute 6-7: Data Controls
1. Navigate to "My Data" from sidebar (5:50)
2. View taste vector visualization (5:55 - 6:10)
3. See "What We Store vs Don't Store" table (6:10 - 6:25)
4. Click "Export as JSON" to test download (6:25 - 6:35)
5. Click "Delete All Data" to see confirmation modal (6:35 - 6:45)
6. Cancel deletion (6:45 - 6:50)

---

## Key Features to Highlight

### 1. No Sign-Up Required
- Instant start, no email/password
- Session-based (stored in browser)
- Privacy-first approach

### 2. Indian Cultural Context
- All content is India-specific
- Archetypes designed for Indian youth
- Questions reference Indian creators, films, music

### 3. AI-Powered Personalization
- Taste DNA generated from quiz answers
- Growth paths tailored to mood + time + archetype
- Feed ranked by relevance to taste markers

### 4. Intentional Growth
- Every recommendation explains WHY (enjoyment + growth)
- Engagement types: Absorb, Create, Reflect
- Balances entertainment with personal development

### 5. Full Data Transparency
- Clear "What We Store vs Don't Store" table
- One-click data export
- One-click data deletion
- DPDP Act 2023 compliant

### 6. Beautiful, Minimal UI
- Dark theme with subtle animations
- Monospace font for technical feel
- Instagram-style feed layout
- Responsive across devices

---

## Technical Notes

### Backend
- FastAPI with 8 endpoints
- Mock AI (deterministic responses)
- In-memory database
- 65-item knowledge base

### Frontend
- React 18 + Vite
- Tailwind CSS
- Recharts for radar visualization
- Lucide icons

### Data Flow
```
Quiz Answers → Taste Analyzer → AI → DNA Card
DNA + Mood + Time → Path Engine → AI → Growth Path
DNA + Knowledge Base → Scoring Algorithm → Feed
```

---

## Success Criteria

The judge should be able to:
- ✅ Complete onboarding in under 2 minutes
- ✅ See a personalized DNA card with archetype
- ✅ Generate a growth path with 3-5 items
- ✅ View personalized feed with 18 cards
- ✅ Export their data as JSON
- ✅ See clear data transparency controls

---

## Troubleshooting

### If DNA card doesn't load:
- Check browser console for errors
- Verify backend is running on port 8000
- Try refreshing the page

### If feed is empty:
- Check that knowledge-base/content.json exists in frontend/public
- Verify frontend can access /knowledge-base/content.json
- Check browser network tab for 404 errors

### If path generation fails:
- Verify session_id is in sessionStorage
- Check backend logs for errors
- Try generating a new DNA card

---

**Built with ❤️ for India's youth**
