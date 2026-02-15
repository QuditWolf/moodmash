# VibeGraph - Quick Start Guide

## 🚀 Get Up and Running in 3 Minutes

### Step 1: Extract and Navigate
```bash
# Extract the vibegraph-app folder
cd vibegraph-app
```

### Step 2: Install Dependencies
```bash
npm install
```

### Step 3: Run the App
```bash
npm run dev
```

Open your browser to `http://localhost:3000` and you're ready to go! 🎉

## 📱 Test the Application

### Default Login Credentials (Mock Auth)
- **Email**: Any valid email format (e.g., `demo@vibegraph.com`)
- **Password**: Any password (8+ characters)

The app currently uses mock authentication stored in localStorage. You can log in with any credentials to explore the UI.

## 🎯 What's Included

### Pages (All Fully Functional UI)
- ✅ Login & Signup with animations
- ✅ Dashboard with stats and activity
- ✅ Profile with vibe analytics
- ✅ Notifications feed
- ✅ Discover page (grid/list views)
- ✅ 404 page

### Components (All Ready to Use)
- Button (6 variants)
- Input (with icons & validation)
- Card (4 variants)
- Modal (responsive, animated)
- Navbar (with theme toggle)
- Sidebar (with navigation)
- FileUpload (drag & drop)
- Loader & EmptyState

### Features
- 🌓 Dark mode (toggle in navbar)
- 📱 Fully responsive
- 🎨 Smooth animations
- 🔒 Protected routes
- 🎯 Type-safe routing
- 💾 State management (Context API)

## 🎨 Customization Tips

### Change Colors
Edit `src/styles/index.css`:
```css
:root {
  --color-primary: #FF6B9D;    /* Your brand color */
  --color-secondary: #4ECDC4;  /* Secondary color */
}
```

### Add a New Page
1. Create file in `src/pages/YourPage.jsx`
2. Add route in `src/App.jsx`
3. Add navigation link in `src/components/Sidebar/Sidebar.jsx`

### Modify Components
All components are in `src/components/` - each has its own folder with:
- Component file (.jsx)
- Styles file (.css)

## 🔌 Backend Integration (Next Steps)

### Environment Setup
Copy `.env.example` to `.env` and configure:
```env
VITE_API_BASE_URL=your-api-url
VITE_AWS_REGION=us-east-1
VITE_AWS_USER_POOL_ID=your-pool-id
```

### API Integration
All API endpoints are defined in `src/services/api.js`:
- Authentication APIs
- User management
- Recommendations
- Vibe spaces
- Content
- Notifications

Replace mock data with real API calls!

## 📦 Build for Production

```bash
npm run build
```

Output will be in `dist/` folder, ready to deploy to:
- AWS Amplify
- Netlify
- Vercel
- Any static hosting

## 🎓 File Structure Overview

```
src/
├── components/      → Reusable UI components
├── pages/          → Page components
├── layouts/        → Layout wrappers
├── contexts/       → State management
├── services/       → API integration
├── utils/          → Helper functions
├── hooks/          → Custom React hooks
└── styles/         → Global CSS
```

## 💡 Pro Tips

1. **Start with Dashboard**: The dashboard page shows most components in action
2. **Check DevTools**: React DevTools to inspect component state
3. **Mobile First**: Test on mobile - everything is responsive
4. **Dark Mode**: Toggle in top navbar to see both themes
5. **API Ready**: All API integration points are marked with TODO comments

## 🐛 Common Issues

**Port already in use?**
```bash
# Change port in vite.config.js
server: { port: 3001 }
```

**Dependencies not installing?**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📚 Learn More

- Check `README.md` for full documentation
- Browse component files for props and usage
- Explore `src/services/api.js` for backend integration
- Review `src/hooks/index.js` for custom hooks

---

**Need help?** The codebase is well-commented and organized. Start exploring! 🚀
