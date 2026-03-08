# MoodMash - Judge Quick Reference

## 🚀 Start Here
**URL**: http://localhost:3000  
**Time**: 5-7 minutes  
**No sign-up required**

---

## ✅ The 4 Flows to Test

### 1️⃣ Onboarding → DNA Card (2-3 min)
```
Landing → "Discover Your Taste DNA" 
→ 15 questions (Indian music/films/books/art)
→ Select goal
→ View DNA card with archetype + radar chart
→ Click "Share" to test
```

**What to Look For:**
- Questions feel relevant to Indian youth
- DNA card has unique archetype name
- Radar chart visualizes taste across 5 domains
- Share button copies to clipboard

---

### 2️⃣ Mindful Path (2-3 min)
```
DNA Card → "Get Your First Path"
→ Select mood (calm/focused/energized/etc.)
→ Select time (15/30/60/90 min)
→ View "Tonight's Path" with 3-5 items
→ Test Done/Skip/Save buttons
```

**What to Look For:**
- Each item shows "Why you'll love it" + "Why it grows you"
- Engagement types: Absorb (blue), Create (amber), Reflect (purple)
- Items span multiple domains (music, film, book, etc.)
- Feedback buttons work (Done/Skip/Save)

---

### 3️⃣ Feed (1-2 min)
```
DNA Card → "Explore Feed"
→ Scroll through Instagram-style grid
→ Toggle grid/list view
→ Click a card
```

**What to Look For:**
- 18 personalized cards (or 12 random if no session)
- Cards show: icon, title, creator, description, mood tags
- Grid layout (3 columns on desktop)
- Hover effects and interactions

---

### 4️⃣ Data Controls (1-2 min)
```
Sidebar → "My Data"
→ View taste vector
→ See "What We Store vs Don't Store"
→ Click "Export as JSON"
→ Click "Delete All Data" (test modal, then cancel)
```

**What to Look For:**
- Clear visualization of stored data
- Transparent table of what's stored vs not stored
- Export downloads JSON file
- Delete shows confirmation modal
- DPDP Act 2023 reference

---

## 🎯 Key Features to Highlight

### Indian Cultural Context
- All content is India-specific
- Archetypes: Midnight Philosopher, Desi Renaissance Soul, Chai Minimalist, etc.
- Questions reference: Prateek Kuhad, Masaan, Tumbbad, etc.

### AI-Powered Personalization
- Taste DNA from quiz answers
- Growth paths tailored to mood + time + archetype
- Feed ranked by relevance

### Intentional Growth
- Every item explains WHY (enjoyment + growth)
- Engagement types: Absorb, Create, Reflect
- Balances entertainment with development

### Privacy-First
- No sign-up required
- Session-based (browser only)
- Full data transparency
- One-click export/delete

---

## 🔍 What Makes This Different

| Traditional Platforms | MoodMash |
|----------------------|----------|
| Optimize for attention | Optimize for growth |
| Endless scrolling | Intentional paths |
| Opaque algorithms | Transparent data |
| Generic recommendations | Taste DNA-based |
| Time sink | Time-bounded (15-90min) |
| Entertainment only | Entertainment + growth |

---

## 📱 Navigation Map

```
Landing
  ↓
Onboarding (15 questions + goal)
  ↓
DNA Card ──→ Feed (explore)
  ↓         ↓
Growth Path → Analytics
  ↓
Data Controls
```

**Sidebar Always Available:**
- Feed
- Taste DNA
- Growth Path
- Analytics
- My Data

---

## 🎨 UI/UX Highlights

- **Dark theme** with subtle animations
- **Monospace font** for technical feel
- **Color-coded engagement types**:
  - Blue = Absorb (listen, watch, read)
  - Amber = Create (make something)
  - Purple = Reflect (journal, think)
- **Instagram-style feed** with hover effects
- **Responsive** across devices

---

## ⚡ Quick Test Checklist

- [ ] Complete onboarding (2 min)
- [ ] View DNA card with archetype
- [ ] Share DNA card (test clipboard)
- [ ] Generate growth path
- [ ] Mark items as Done/Skip/Save
- [ ] Explore feed (grid view)
- [ ] Toggle to list view
- [ ] Export data as JSON
- [ ] Test delete confirmation modal
- [ ] Navigate using sidebar

---

## 🐛 If Something Breaks

### Backend not responding?
```bash
curl http://localhost:8000/health
```

### Frontend not loading?
```bash
curl http://localhost:3000
```

### Restart everything:
```bash
./start.sh
```

---

## 📊 Success Metrics

The judge should experience:
- ✅ Smooth onboarding (no friction)
- ✅ Personalized DNA card (feels unique)
- ✅ Relevant growth path (makes sense for mood/time)
- ✅ Engaging feed (want to explore more)
- ✅ Clear data controls (trust the platform)

---

## 💡 Demo Tips

1. **Start fresh**: Clear sessionStorage for clean demo
2. **Answer authentically**: Better personalization
3. **Try different moods**: See how paths change
4. **Explore feed**: Scroll to see variety
5. **Show data controls**: Highlight transparency

---

**Built with ❤️ for India's youth**

**Tech Stack**: React + FastAPI + Tailwind + AI
