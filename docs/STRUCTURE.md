# VibeGraph Project Structure

```
vibegraph-app/
│
├── 📄 Configuration Files
│   ├── package.json              # Dependencies and scripts
│   ├── vite.config.js            # Vite configuration + path aliases
│   ├── index.html                # HTML entry point
│   ├── .env.example              # Environment variables template
│   ├── .gitignore                # Git ignore rules
│   ├── README.md                 # Full documentation
│   └── QUICKSTART.md             # Quick start guide
│
└── 📁 src/                       # Source code
    │
    ├── 🎨 styles/
    │   └── index.css             # Global styles, CSS variables, utilities
    │
    ├── 🧩 components/            # Reusable UI Components
    │   ├── Button/
    │   │   ├── Button.jsx        # Button component (6 variants)
    │   │   └── Button.css        # Button styles
    │   ├── Input/
    │   │   ├── Input.jsx         # Input component with icons
    │   │   └── Input.css         # Input styles
    │   ├── Card/
    │   │   ├── Card.jsx          # Card component (4 variants)
    │   │   └── Card.css          # Card styles
    │   ├── Modal/
    │   │   ├── Modal.jsx         # Modal dialog component
    │   │   └── Modal.css         # Modal styles
    │   ├── Loader/
    │   │   ├── Loader.jsx        # Loading spinner
    │   │   └── Loader.css        # Loader styles
    │   ├── EmptyState/
    │   │   ├── EmptyState.jsx    # Empty state placeholder
    │   │   └── EmptyState.css    # EmptyState styles
    │   ├── Navbar/
    │   │   ├── Navbar.jsx        # Top navigation bar
    │   │   └── Navbar.css        # Navbar styles
    │   ├── Sidebar/
    │   │   ├── Sidebar.jsx       # Side navigation menu
    │   │   └── Sidebar.css       # Sidebar styles
    │   ├── FileUpload/
    │   │   ├── FileUpload.jsx    # Drag & drop file upload
    │   │   └── FileUpload.css    # FileUpload styles
    │   ├── ProtectedRoute.jsx    # Route guard for auth
    │   └── index.js              # Component exports
    │
    ├── 📄 pages/                 # Page Components
    │   ├── Login.jsx             # Login page
    │   ├── Signup.jsx            # Signup page
    │   ├── Auth.css              # Shared auth styles
    │   ├── Dashboard.jsx         # Main dashboard
    │   ├── Dashboard.css         # Dashboard styles
    │   ├── Profile.jsx           # User profile & settings
    │   ├── Profile.css           # Profile styles
    │   ├── Notifications.jsx     # Notifications feed
    │   ├── Notifications.css     # Notifications styles
    │   ├── DiscoverList.jsx      # Discovery/list page
    │   ├── DiscoverList.css      # DiscoverList styles
    │   ├── NotFound.jsx          # 404 page
    │   └── NotFound.css          # NotFound styles
    │
    ├── 🎭 layouts/               # Layout Wrappers
    │   ├── AuthLayout.jsx        # Auth pages layout
    │   ├── AuthLayout.css        # Auth layout styles
    │   ├── DashboardLayout.jsx   # Dashboard layout
    │   └── DashboardLayout.css   # Dashboard layout styles
    │
    ├── 🔄 contexts/              # State Management
    │   ├── AuthContext.jsx       # Authentication state
    │   └── ThemeContext.jsx      # Theme (dark/light mode)
    │
    ├── 🔌 services/              # API Integration
    │   └── api.js                # API client & endpoints
    │       ├── authAPI           # Login, signup, logout
    │       ├── userAPI           # Profile, avatar
    │       ├── recommendationsAPI # Get recommendations
    │       ├── vibeSpacesAPI     # Vibe spaces management
    │       ├── contentAPI        # Search, save content
    │       └── notificationsAPI  # Notifications
    │
    ├── 🛠️ utils/                 # Utility Functions
    │   └── helpers.js            # Helper functions
    │       ├── Date formatting
    │       ├── String utilities
    │       ├── Number formatting
    │       ├── Validation
    │       ├── Array utilities
    │       ├── Storage utilities
    │       └── Misc utilities
    │
    ├── 🎣 hooks/                 # Custom React Hooks
    │   └── index.js              # Custom hooks
    │       ├── useMediaQuery     # Responsive breakpoints
    │       ├── useLocalStorage   # Persistent state
    │       ├── useDebounce       # Debounced values
    │       ├── useClickOutside   # Click outside detection
    │       ├── useAsync          # Async operations
    │       ├── useToggle         # Boolean toggle
    │       └── More...
    │
    ├── App.jsx                   # Main app with routing
    └── main.jsx                  # Entry point


📊 Component Hierarchy
────────────────────────

App
├── ThemeProvider
│   └── AuthProvider
│       └── BrowserRouter
│           ├── AuthLayout (Public)
│           │   ├── Login
│           │   └── Signup
│           │
│           └── DashboardLayout (Protected)
│               ├── Navbar
│               ├── Sidebar
│               └── Pages
│                   ├── Dashboard
│                   ├── Profile
│                   ├── Notifications
│                   ├── DiscoverList
│                   └── NotFound


🎨 Design System
─────────────────

Colors:
├── Primary: #FF6B9D (Pink gradient)
├── Secondary: #4ECDC4 (Teal)
├── Accent: #FFE66D (Yellow)
└── Accent Purple: #A78BFA

Typography:
├── Display: Instrument Serif
├── Body: Inter
└── Mono: JetBrains Mono

Components:
├── Buttons: 6 variants (primary, secondary, outline, ghost, gradient)
├── Cards: 4 variants (default, elevated, outline, glass)
├── Inputs: With icons, validation, helper text
└── All responsive, animated, dark-mode ready


🔐 Authentication Flow
───────────────────────

1. User visits app
2. ProtectedRoute checks auth
3. If not authenticated → redirect to /login
4. User logs in → AuthContext updates
5. Redirect to /dashboard
6. All routes now accessible


🌐 Routing Structure
─────────────────────

Public Routes:
├── /login        → Login page
└── /signup       → Signup page

Protected Routes:
├── /dashboard    → Main dashboard
├── /discover     → Discovery page
├── /profile      → User profile
├── /settings     → Settings (uses Profile)
├── /notifications → Notifications
├── /spaces       → Vibe Spaces
├── /books        → Books category
├── /music        → Music category
├── /fashion      → Fashion category
├── /films        → Films category
├── /art          → Art category
├── /messages     → Messages
└── *             → 404 page


📦 Build Process
─────────────────

Development:
npm run dev → Vite dev server → localhost:3000

Production:
npm run build → dist/ folder → Deploy anywhere


🚀 Deployment Ready For:
──────────────────────────

├── AWS Amplify
├── Netlify
├── Vercel
├── CloudFront + S3
└── Any static hosting
```
