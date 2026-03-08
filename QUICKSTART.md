# MoodMash - Quick Start Guide

## 🚀 Start in 30 Seconds

```bash
./start.sh
```

Then open: **http://localhost:3000**

---

## 📋 What You'll See

1. **Landing Page** → Click "Discover Your Taste DNA"
2. **Quiz** → Answer 15 questions + select goal
3. **DNA Card** → Your AI-generated archetype
4. **Growth Path** → Select mood + time → Get curated items
5. **Analytics** → See your patterns
6. **Data Panel** → Export or delete your data

---

## ✅ Verify It's Working

```bash
python3 test_api.py
```

Should show:
```
✓ Health check passed
✓ Onboard passed
✓ DNA generation passed
✓ Growth path passed
✓ Analytics passed
✅ All API tests passed!
```

---

## 🔗 URLs

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## 🛑 Stop Servers

Press `Ctrl+C` in the terminal running `./start.sh`

Or manually:
```bash
pkill -f uvicorn
pkill -f vite
```

---

## 📚 More Info

- **Full Setup**: See README.md
- **Testing Guide**: See TESTING.md
- **Deployment**: See DEPLOYMENT.md
- **Current Status**: See STATUS.md

---

## 🐛 Quick Fixes

**Servers won't start?**
```bash
source venv/bin/activate
pip install -r backend/requirements.txt
cd frontend && npm install
```

**Port already in use?**
```bash
# Kill processes on ports 3000 and 8000
lsof -ti:3000 | xargs kill -9
lsof -ti:8000 | xargs kill -9
```

**Frontend shows errors?**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

---

**That's it! You're ready to go! 🎉**
