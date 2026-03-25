# MoodMash Testing Guide

This document provides comprehensive testing instructions for the MoodMash application.

## Quick Test

Run the automated API test:
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
✅ All API tests passed!
```

## Manual Testing Flow

### 1. Start the Application

```bash
# Option 1: Use the startup script
./start.sh

# Option 2: Use npm
npm run dev

# Option 3: Run servers separately
# Terminal 1:
source venv/bin/activate
PYTHONPATH=. uvicorn backend.main:app --reload --port 8000

# Terminal 2:
cd frontend && npm run dev
```

### 2. Landing Page Test

1. Open http://localhost:3000
2. Verify you see:
   - "MoodMash" logo
   - Hero text: "Every platform optimizes for your attention..."
   - Three feature pills: Taste DNA, Growth Paths, Privacy-first
   - "Discover Your Taste DNA" button
3. Click the CTA button
4. Should navigate to `/onboard`

### 3. Onboarding Test

**Quiz Questions (15 total)**

1. Answer at least one option per question
2. Verify progress bar updates (Question X of 15)
3. Verify "Next" button is disabled until you select at least one option
4. Test all 15 questions across 5 domains:
   - Music (3 questions)
   - Films & Stories (3 questions)
   - Visual World (3 questions)
   - Creative & Goals (3 questions)
   - Consumption Style (3 questions)

**Goal Selection**

1. After question 15, verify goal selection screen appears
2. Select one of 6 goals:
   - Build something that matters
   - Get technically excellent
   - Find what makes me happy
   - Start something of my own
   - Understand where I come from
   - Just inspire me and see what emerges
3. Click "Build My Taste DNA"
4. Verify loading state: "Building your Taste DNA..."
5. Should navigate to `/dna/:session_id`

### 4. Taste DNA Card Test

1. Verify DNA card displays:
   - Archetype name (e.g., "Midnight Philosopher", "Desi Renaissance Soul")
   - Vibe summary (2-3 lines of AI-generated text)
   - Taste markers (5-7 tags)
   - Radar chart with 5 domains (Music, Films, Books, Art, Creators)
2. Test "Share" button:
   - Click Share
   - Verify "Copied!" message appears
   - Paste clipboard content - should contain archetype + vibe summary
3. Click "Enter Growth Path"
4. Should navigate to `/path/:session_id`

### 5. Growth Path Test

**Path Generation**

1. Verify mood selector displays 5 options:
   - focused, exploratory, melancholic, energized, calm
2. Select a mood
3. Verify time selector displays 4 options:
   - 15min, 30min, 60min, 90min
4. Select a time
5. Click "Get My Path"
6. Verify loading state: "Curating your growth path..."
7. Verify 3-5 items are displayed

**Path Items**

For each item, verify:
1. Colored left border (blue=Absorb, amber=Create, purple=Reflect)
2. Title and creator
3. Engagement type badge (Absorb/Create/Reflect)
4. Domain tag
5. Time badge (e.g., "4min")
6. "Why you'll love it" text
7. "Why it grows you" text
8. Three action buttons: Done, Skip, Save

**Feedback Test**

1. Click "Done" on first item
2. Verify buttons disappear and "Marked as done" appears
3. Click "Skip" on second item
4. Verify "Skipped" appears
5. Click "Save" on third item
6. Verify "Saved for later" appears
7. Click "View Analytics" link at bottom
8. Should navigate to `/analytics/:session_id`

### 6. Analytics Test

Verify the following sections display:

**Domain Scores Radar**
1. Radar chart with 5 axes
2. Values should match your taste profile

**Goal Alignment**
1. Large percentage number (0-100%)
2. Progress bar matching the percentage
3. Should reflect ratio of completed items

**Stats Row**
1. Three cards: Done, Skipped, Saved
2. Numbers should match your feedback actions

**Domain Breakdown**
1. Bar chart showing which domains you've consumed
2. Bars should be proportional to item counts

**AI Pattern Insight**
1. 1-2 sentences of natural language observation
2. Should reference your completion patterns
3. Examples:
   - "You have not started your growth path yet..."
   - "You are crushing it — X items completed..."
   - "Solid progress with X items done..."

**Navigation**
1. Click "View Your Data" link
2. Should navigate to `/data/:session_id`

### 7. Data Panel Test

**Your Taste Vector**
1. Displays your archetype name
2. Shows domain scores in a grid

**What We Store vs Don't Store**
1. Left column: What we store
   - Anonymized taste vector
   - Archetype
   - Goal
   - Path completions
2. Right column: What we don't store
   - Quiz answers (discarded)
   - Spotify raw data
   - Personal info
   - Browsing history

**Export Test**
1. Click "Export as JSON"
2. Verify file downloads: `moodmash-data-{session_id}.json`
3. Open file and verify it contains:
   - radar_scores or domain_scores
   - archetype
   - Other session data

**Delete Test**
1. Click "Delete All Data"
2. Verify confirmation modal appears
3. Modal should show:
   - Warning icon
   - "Delete all data?" heading
   - Description of what will be deleted
   - Cancel and "Delete Forever" buttons
4. Click "Delete Forever"
5. Should navigate back to `/` (landing page)
6. Verify session is cleared (sidebar nav items should be disabled)

**Legal Reference**
1. Verify footer text: "Aligned with India's Digital Personal Data Protection Act, 2023"

### 8. Sidebar Navigation Test

**Desktop (width > 768px)**
1. Sidebar should be visible on left
2. Verify 4 nav items:
   - 🧬 Taste DNA
   - 🌱 Growth Path
   - 📊 Analytics
   - 🔒 My Data
3. Click each nav item
4. Verify active state (white background)
5. Verify navigation works

**Mobile (width < 768px)**
1. Sidebar should be hidden by default
2. Verify hamburger menu button in top-left
3. Click hamburger menu
4. Sidebar should slide in from left
5. Click outside sidebar
6. Sidebar should close
7. Click nav item
8. Sidebar should close and navigate

**Without Session**
1. Clear sessionStorage: `sessionStorage.clear()`
2. Refresh page
3. Nav items should be disabled (grayed out)
4. "Start Onboarding" link should appear

### 9. Error Handling Test

**Invalid Session ID**
1. Navigate to `/dna/invalid-session-id`
2. Should show error: "Session not found"
3. "Retry" button should reload page

**Network Error**
1. Stop backend server
2. Try to submit onboarding
3. Should show error message
4. "Try Again" button should retry

**Empty Path**
1. Request path with no matching content
2. Should handle gracefully (show message or empty state)

## API Testing

### Health Check
```bash
curl http://localhost:8000/health
```
Expected: `{"status":"ok","mock_mode":true}`

### Onboard
```bash
curl -X POST http://localhost:8000/api/onboard \
  -H "Content-Type: application/json" \
  -d '{
    "quiz_answers": {
      "music_album": ["Prateek Kuhad - cold/mess"],
      "music_3am": ["Lo-fi Hindustani beats"],
      "film_feel": ["Masaan (ghat scene)"]
    },
    "goal": "Build something that matters"
  }'
```
Expected: `{"session_id":"...", "status":"ok"}`

### Get DNA
```bash
# Replace SESSION_ID with actual session ID from onboard
curl http://localhost:8000/api/dna/SESSION_ID
```
Expected: JSON with archetype, vibe_summary, markers, radar_scores

### Generate Path
```bash
curl -X POST http://localhost:8000/api/path \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "SESSION_ID",
    "mood": "calm",
    "goal": "explore",
    "time_available": 30
  }'
```
Expected: JSON with path_id and items array

### Submit Feedback
```bash
curl -X POST http://localhost:8000/api/path/PATH_ID/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "SESSION_ID",
    "item_id": "music_001",
    "status": "done",
    "reaction": "done"
  }'
```
Expected: `{"ok":true}` or similar

### Get Analytics
```bash
curl http://localhost:8000/api/analytics/SESSION_ID
```
Expected: JSON with radar_scores, goal_alignment_pct, items_done, etc.

### Export Data
```bash
curl http://localhost:8000/api/data/SESSION_ID
```
Expected: JSON with user data

### Delete Data
```bash
curl -X DELETE http://localhost:8000/api/data/SESSION_ID
```
Expected: `{"deleted":true}` or similar

## Browser Testing

Test on:
- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Android)

## Performance Testing

1. Check page load times (should be < 2s)
2. Check API response times (should be < 500ms)
3. Check radar chart rendering (should be smooth)
4. Check navigation transitions (should be instant)

## Accessibility Testing

1. Test keyboard navigation (Tab, Enter, Escape)
2. Test screen reader compatibility
3. Verify color contrast ratios
4. Test with browser zoom (100%, 150%, 200%)

## Known Issues / Limitations

1. **Session persistence**: Sessions are in-memory only. Restarting backend clears all data.
2. **No authentication**: Anyone with a session ID can access that session.
3. **Mock AI**: Responses are deterministic, not truly AI-generated (until Bedrock is enabled).
4. **No Spotify integration**: Spotify connect is not implemented in MVP.
5. **Limited content**: Only 65 items in knowledge base (production would have 200-300+).

## Success Criteria

✅ All 5 features work end-to-end
✅ No console errors in browser
✅ No 500 errors from backend
✅ Data flows correctly through all endpoints
✅ UI is responsive on mobile and desktop
✅ Privacy controls work (export/delete)
✅ Navigation is smooth and intuitive

## Troubleshooting

### Frontend shows blank page
- Check browser console for errors
- Verify backend is running on port 8000
- Check network tab for failed API calls

### Backend returns 500 errors
- Check backend terminal for Python errors
- Verify all dependencies are installed
- Check PYTHONPATH is set correctly

### Radar chart not rendering
- Verify recharts is installed: `npm list recharts`
- Check browser console for errors
- Verify data format matches expected structure

### Session not persisting
- Check sessionStorage in browser DevTools
- Verify session_id is being set after onboarding
- Check if session_id is being passed to API calls

---

**Happy Testing! 🎉**

If you find any bugs, please document:
1. Steps to reproduce
2. Expected behavior
3. Actual behavior
4. Browser/OS
5. Console errors (if any)
