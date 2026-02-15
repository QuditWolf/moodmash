# VibeGraph - Social Taste & Culture Platform

AI-powered platform for discovering your aesthetic identity through cultural connections across books, music, fashion, films, and art.

## 🎨 Project Overview

VibeGraph transforms passive recommendation into social cultural discovery by:

- **Cross-domain Taste Mapping**: Understanding aesthetic preferences across books, music, fashion, films, and art
- **AI-Powered Vibe Spaces**: Connecting users through shared cultural energy
- **Social Discovery**: Every recommendation becomes a social object for discussion and engagement
- **Taste Graph Analytics**: Building unified aesthetic profiles

## 🚀 Tech Stack

- **Framework**: React 18 + Vite
- **Routing**: React Router v6
- **Animation**: Framer Motion
- **Icons**: Lucide React
- **Styling**: Custom CSS with CSS Variables
- **State Management**: React Context API

## 📁 Project Structure

```
vibegraph-app/
├── src/
│   ├── components/         # Reusable UI components
│   │   ├── Button/
│   │   ├── Card/
│   │   ├── Input/
│   │   ├── Modal/
│   │   ├── Navbar/
│   │   ├── Sidebar/
│   │   ├── FileUpload/
│   │   ├── Loader/
│   │   ├── EmptyState/
│   │   ├── ProtectedRoute.jsx
│   │   └── index.js
│   ├── pages/              # Page components
│   │   ├── Login.jsx
│   │   ├── Signup.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Profile.jsx
│   │   ├── Notifications.jsx
│   │   ├── DiscoverList.jsx
│   │   └── NotFound.jsx
│   ├── layouts/            # Layout wrappers
│   │   ├── AuthLayout.jsx
│   │   └── DashboardLayout.jsx
│   ├── contexts/           # React Context providers
│   │   ├── AuthContext.jsx
│   │   └── ThemeContext.jsx
│   ├── services/           # API integration
│   │   └── api.js
│   ├── utils/              # Utility functions
│   │   └── helpers.js
│   ├── hooks/              # Custom React hooks
│   │   └── index.js
│   ├── styles/             # Global styles
│   │   └── index.css
│   ├── App.jsx             # Main app component
│   └── main.jsx            # Entry point
├── public/                 # Static assets
├── index.html              # HTML template
├── package.json
├── vite.config.js
├── .env.example
└── README.md
```

## 🛠️ Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn

### Installation

1. **Clone or extract the project**

2. **Navigate to project directory**
   ```bash
   cd vibegraph-app
   ```

3. **Install dependencies**
   ```bash
   npm install
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and configure your API endpoints and AWS settings.

5. **Start development server**
   ```bash
   npm run dev
   ```

6. **Open in browser**
   Navigate to `http://localhost:3000`

### Build for Production

```bash
npm run build
```

Preview production build:
```bash
npm run preview
```

## 🎯 Features

### Implemented (Placeholder UI)

✅ **Authentication System**
- Login/Signup pages with form validation
- Protected routes
- Auth context for state management

✅ **Dashboard**
- Stats overview (Vibe Score, Connections, Saved Items, Growth)
- Vibe Spaces preview
- Recent activity feed
- AI-powered recommendations section

✅ **Profile & Settings**
- User profile management
- Avatar upload placeholder
- Vibe profile visualization
- Category scores

✅ **Notifications**
- Notification feed
- Unread indicators
- Activity types (likes, comments, follows, matches)

✅ **Discovery/List View**
- Grid/List view toggle
- Search functionality
- Filter options
- Category-based browsing

✅ **Design System**
- Responsive layouts
- Dark mode support
- Smooth animations
- Consistent spacing and typography
- Reusable component library

### Ready for Integration

🔄 **API Integration Points**
- All API endpoints defined in `src/services/api.js`
- Ready to connect to AWS backend (AppSync, Lambda, DynamoDB)
- Environment variable configuration

🔄 **AWS Services (Future)**
- S3: User uploads & taste graph storage
- DynamoDB: User data & preferences
- Bedrock: AI recommendations
- Personalize: Recommendation engine
- AppSync/API Gateway: GraphQL/REST APIs

## 🎨 Design Philosophy

The UI uses a **refined, culturally-aware aesthetic**:

- **Typography**: Instrument Serif for display, Inter for body text
- **Colors**: Vibrant yet sophisticated palette with gradients
- **Animations**: Smooth Framer Motion transitions
- **Layout**: Clean, spacious, content-first design
- **Responsive**: Mobile-first approach

## 🔐 Authentication Flow

Current implementation uses **mock authentication** with localStorage. Replace with AWS Cognito:

1. Update `AuthContext.jsx` with Cognito SDK
2. Configure AWS credentials in `.env`
3. Update API service with proper auth headers

## 📝 Key Components

### Reusable Components

- **Button**: Multiple variants (primary, secondary, outline, ghost, gradient)
- **Input**: Form inputs with icons and validation
- **Card**: Flexible card component with variants
- **Modal**: Accessible modal dialogs
- **Loader**: Loading states (inline and full-screen)
- **EmptyState**: Placeholder for empty states

### Layout Components

- **AuthLayout**: Centered auth forms with animated background
- **DashboardLayout**: Sidebar + navbar layout
- **ProtectedRoute**: Route guard for authenticated pages

## 🎣 Custom Hooks

- `useMediaQuery`: Responsive breakpoints
- `useLocalStorage`: Persistent state
- `useDebounce`: Debounced values
- `useClickOutside`: Detect outside clicks
- `useAsync`: Async operation handling
- `useToggle`: Boolean state toggle
- `useWindowSize`: Window dimensions

## 🌐 Routing Structure

```
/ → /dashboard (redirect)
/login → Login page
/signup → Signup page
/dashboard → Main dashboard
/discover → Discovery page
/profile → User profile
/settings → Settings (uses Profile)
/notifications → Notifications
/spaces → Vibe Spaces
/books → Books category
/music → Music category
/fashion → Fashion category
/films → Films category
/art → Art category
/messages → Messages (placeholder)
* → 404 page
```

## 🚀 Next Steps

### Backend Integration

1. **Set up AWS Services**
   - Configure Cognito user pool
   - Set up DynamoDB tables
   - Deploy Lambda functions
   - Configure S3 buckets

2. **Replace Mock Data**
   - Connect API service to real endpoints
   - Implement real-time updates with AppSync
   - Add file upload to S3

3. **AI Integration**
   - Connect to AWS Bedrock for recommendations
   - Implement taste graph analysis
   - Add vibe matching algorithm

### Feature Development

1. **Social Features**
   - Comments and discussions
   - User-to-user messaging
   - Moodboard creation
   - Content sharing

2. **Content Management**
   - CRUD operations for content
   - Save/bookmark functionality
   - Collections and lists

3. **Advanced Features**
   - Real-time notifications
   - Search with filters
   - Advanced analytics
   - Recommendation explanations

## 🎨 Customization

### Themes

Edit CSS variables in `src/styles/index.css`:

```css
:root {
  --color-primary: #FF6B9D;
  --color-secondary: #4ECDC4;
  /* ... more variables */
}
```

### Components

All components are modular and accept props for customization. Check component files for available props.

## 📚 Resources

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Framer Motion](https://www.framer.com/motion/)
- [React Router](https://reactrouter.com)

## 🤝 Contributing

This is a starter template. Feel free to modify and extend it for your needs!

## 📄 License

MIT License - feel free to use this template for your projects.

---

**Built with ❤️ for the VibeGraph platform**
