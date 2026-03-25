# MoodMash Troubleshooting Guide

## Frontend Shows Blank Page

### Quick Fixes

1. **Hard Refresh Browser**
   - Chrome/Firefox: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
   - This clears the cache and reloads

2. **Check Test Page**
   - Visit: http://localhost:3000/test.html
   - If you see "MoodMash Test Page", the server is working
   - If blank, the server isn't running

3. **Open Browser Console**
   - Press `F12` or right-click → Inspect
   - Go to Console tab
   - Look for red error messages
   - Common errors:
     - "Failed to fetch" → Backend not running
     - "Module not found" → Missing dependency
     - "Unexpected token" → Syntax error

4. **Check Network Tab**
   - Press `F12` → Network tab
   - Reload page
   - Look for failed requests (red)
   - Check if `main.jsx` loads successfully

### Detailed Diagnostics

#### Step 1: Verify Servers Are Running

```bash
# Check if processes are running
ps aux | grep -E "(uvicorn|vite)"

# Should see:
# - uvicorn backend.main:app
# - vite (in frontend directory)
```

#### Step 2: Test Backend

```bash
curl http://localhost:8000/health
# Should return: {"status":"ok","mock_mode":true}
```

#### Step 3: Test Frontend Server

```bash
curl http://localhost:3000/test.html
# Should return HTML content
```

#### Step 4: Check for Port Conflicts

```bash
# Check what's on port 3000
lsof -i :3000

# Check what's on port 8000
lsof -i :8000
```

### Common Issues

#### Issue: "Cannot GET /"

**Cause**: Frontend server not running or crashed

**Fix**:
```bash
cd frontend
npm run dev
```

#### Issue: Black Screen, No Errors

**Cause**: CSS not loading or background/text color issue

**Fix**:
1. Open browser DevTools (F12)
2. Go to Elements tab
3. Check if `<div id="root">` has content inside
4. If empty, check Console for React errors
5. If has content but invisible, check CSS:
   ```javascript
   // In browser console:
   document.body.style.background = 'white'
   document.body.style.color = 'black'
   ```

#### Issue: "Module not found" Errors

**Cause**: Missing dependencies

**Fix**:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### Issue: "Failed to fetch" in Console

**Cause**: Backend not running or CORS issue

**Fix**:
1. Check backend is running: `curl http://localhost:8000/health`
2. If not running:
   ```bash
   source venv/bin/activate
   PYTHONPATH=. uvicorn backend.main:app --reload --port 8000
   ```

#### Issue: Page Loads But Components Don't Render

**Cause**: React Router or component import errors

**Fix**:
1. Check browser console for errors
2. Verify all component files exist:
   ```bash
   ls frontend/src/pages/Landing.jsx
   ls frontend/src/components/Onboarding/OnboardingPage.jsx
   ls frontend/src/components/DNACard/DNACard.jsx
   ```

### Browser-Specific Issues

#### Chrome/Chromium
- Clear site data: DevTools → Application → Clear storage
- Disable extensions that might interfere
- Try incognito mode

#### Firefox
- Clear cache: Ctrl+Shift+Delete → Check "Cache" → Clear
- Disable tracking protection for localhost
- Try private window

#### Safari
- Clear cache: Develop → Empty Caches
- Enable Develop menu: Preferences → Advanced → Show Develop menu

### Environment Issues

#### Wrong Node Version

```bash
node --version
# Should be 18.x or higher

# If wrong version, install nvm and use correct version:
nvm install 18
nvm use 18
```

#### Wrong Python Version

```bash
python3 --version
# Should be 3.10 or higher
```

#### Missing Environment Variables

```bash
# Check if .env exists
cat .env

# Should contain:
# USE_MOCK=true
# USE_DYNAMODB=false
# VITE_API_URL=http://localhost:8000

# Check frontend .env
cat frontend/.env

# Should contain:
# VITE_API_URL=http://localhost:8000
```

### Nuclear Option: Complete Reset

If nothing works, do a complete reset:

```bash
# 1. Stop all processes
pkill -f uvicorn
pkill -f vite

# 2. Clean everything
rm -rf venv
rm -rf frontend/node_modules
rm -rf frontend/package-lock.json
rm -rf node_modules
rm -rf package-lock.json

# 3. Reinstall
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..
npm install

# 4. Restart
./start.sh
```

### Still Not Working?

1. **Check the logs**:
   - Backend terminal: Look for Python errors
   - Frontend terminal: Look for Vite errors
   - Browser console: Look for JavaScript errors

2. **Test individual components**:
   ```bash
   # Test backend
   python3 test_api.py
   
   # Test frontend build
   cd frontend && npm run build
   ```

3. **Verify file structure**:
   ```bash
   # Check all required files exist
   ls frontend/src/App.jsx
   ls frontend/src/main.jsx
   ls frontend/index.html
   ls backend/main.py
   ```

4. **Check for syntax errors**:
   ```bash
   # Check Python syntax
   python3 -m py_compile backend/main.py
   
   # Check JavaScript syntax (build will fail if syntax error)
   cd frontend && npm run build
   ```

### Getting Help

If you're still stuck, gather this information:

1. **Browser console errors** (screenshot or copy text)
2. **Backend terminal output** (last 50 lines)
3. **Frontend terminal output** (last 50 lines)
4. **Network tab** (any failed requests)
5. **Your OS and browser version**

Then check:
- README.md for setup instructions
- STATUS.md for current state
- TESTING.md for test procedures

---

## Quick Reference

### Restart Everything
```bash
./start.sh
```

### Check Status
```bash
# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000/test.html

# Test API
python3 test_api.py
```

### View Logs
```bash
# Backend logs: Check terminal running uvicorn
# Frontend logs: Check terminal running vite
# Browser logs: F12 → Console
```

### Common URLs
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Test Page: http://localhost:3000/test.html
