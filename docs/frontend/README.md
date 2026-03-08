# Frontend Documentation

## Overview

The VibeGraph frontend is a React-based single-page application built with Vite, providing an adaptive quiz experience and personalized content recommendations. The application features a modern, responsive design using Tailwind CSS and Framer Motion for animations.

## Architecture

### Technology Stack

- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **State Management**: Redux Toolkit
- **Routing**: React Router v6
- **Animations**: Framer Motion
- **Charts**: Recharts
- **UI Components**: Radix UI primitives

### Project Structure

```
frontend/
├── src/
│   ├── components/       # Reusable UI components
│   │   ├── onboarding/  # Quiz and onboarding flow
│   │   ├── ui/          # Base UI primitives
│   │   └── ...          # Feature-specific components
│   ├── services/        # API service layer
│   ├── pages/           # Route-level page components
│   ├── layouts/         # Layout wrapper components
│   ├── contexts/        # React context providers
│   ├── hooks/           # Custom React hooks
│   ├── utils/           # Utility functions
│   ├── styles/          # Global styles
│   └── data/            # Static data and constants
├── public/              # Static assets
└── docs/                # Component documentation
```

## Key Features

### 1. Adaptive Quiz System

The onboarding flow guides users through a multi-phase adaptive quiz:
- **Section 1**: Foundational questions about taste preferences
- **Section 2**: Adaptive follow-up questions based on Section 1 responses
- **Processing**: AI-powered profile generation
- **Results**: Taste DNA archetype display

See [Onboarding Components](./components/onboarding.md) for detailed documentation.

### 2. API Service Layer

Centralized API communication layer that handles:
- HTTP request/response management
- Authentication token handling
- Error handling and retry logic
- Request/response transformation

See [API Services](./services/api.md) for detailed documentation.

### 3. Component Library

Modular, reusable components following atomic design principles:
- **Atoms**: Basic UI elements (Button, Input, Card)
- **Molecules**: Composite components (FeedCard, Modal)
- **Organisms**: Complex feature components (Navbar, Sidebar)
- **Templates**: Page layouts

See [Components Documentation](./components/) for individual component docs.

## Development

### Environment Setup

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables:
```bash
cp .env.example .env
```

Required environment variables:
- `VITE_API_BASE_URL`: Backend API endpoint (default: http://localhost:8000)

3. Start development server:
```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

Output will be in the `dist/` directory.

### Docker Development

Build and run in Docker container:
```bash
docker build -t vibegraph-frontend .
docker run -p 3000:3000 vibegraph-frontend
```

## API Integration

The frontend communicates with the backend through a centralized API service layer located in `src/services/`. All API calls use the `apiRequest` helper function which handles:

- Base URL configuration from environment variables
- Authentication token injection from localStorage
- Content-Type headers
- Error parsing and handling
- Response JSON parsing

### API Modules

- **authAPI**: User authentication (login, signup, logout)
- **userAPI**: User profile management
- **recommendationsAPI**: Personalized content recommendations
- **vibeSpacesAPI**: Community spaces management
- **contentAPI**: Content search and saving
- **notificationsAPI**: User notifications

See [API Service Documentation](./services/api.md) for complete API reference.

## Component Documentation

### Core Components

- [Onboarding System](./components/onboarding.md) - Adaptive quiz flow
- [Feed System](./FEED_STRUCTURE.md) - Content feed and cards
- [Navigation](./components/navbar.md) - Top navigation bar
- [Sidebar](./components/sidebar.md) - Side navigation panel

### UI Components

- [Button](./components/button.md) - Button variants and usage
- [Card](./components/card.md) - Card container component
- [Input](./components/input.md) - Form input fields
- [Modal](./components/modal.md) - Modal dialog component
- [Loader](./components/loader.md) - Loading indicators

## State Management

The application uses Redux Toolkit for global state management:

- **User State**: Authentication status, user profile
- **UI State**: Modal visibility, sidebar state
- **Content State**: Feed items, saved content
- **Notifications State**: User notifications

## Routing

React Router v6 is used for client-side routing:

- `/` - Home/Feed page
- `/onboarding` - Quiz onboarding flow
- `/profile` - User profile page
- `/spaces` - Vibe spaces discovery
- `/saved` - Saved content
- `/settings` - User settings

Protected routes require authentication and redirect to login if not authenticated.

## Styling

### Tailwind CSS

The application uses Tailwind CSS for utility-first styling. Custom theme configuration is in `tailwind.config.js`.

### Design System

See [Design System Documentation](./DESIGN_SYSTEM.md) for:
- Color palette
- Typography scale
- Spacing system
- Component variants
- Animation patterns

## Testing

### Unit Tests

```bash
npm run test
```

### E2E Tests

```bash
npm run test:e2e
```

## Performance Optimization

- **Code Splitting**: Route-based lazy loading
- **Image Optimization**: Lazy loading and responsive images
- **Bundle Size**: Tree shaking and minification
- **Caching**: Service worker for offline support

## Accessibility

The application follows WCAG 2.1 Level AA guidelines:
- Semantic HTML
- ARIA labels and roles
- Keyboard navigation
- Screen reader support
- Color contrast compliance

## Browser Support

- Chrome/Edge (last 2 versions)
- Firefox (last 2 versions)
- Safari (last 2 versions)
- Mobile browsers (iOS Safari, Chrome Android)

## Related Documentation

- [Backend API Documentation](../backend/README.md)
- [Infrastructure Documentation](../infrastructure/)
- [API Contracts](../api/API_CONTRACTS.md)
- [Deployment Guide](../infrastructure/DEPLOYMENT.md)

## Contributing

When adding new components:
1. Create component in appropriate directory
2. Add documentation in `docs/frontend/components/`
3. Include props, state, and usage examples
4. Add unit tests
5. Update this README if adding new features

## Support

For issues or questions, see the main project README or contact the development team.
