import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from '@contexts/AuthContext';
import { ThemeProvider } from '@contexts/ThemeContext';
import ProtectedRoute from '@components/ProtectedRoute';
import AuthLayout from '@layouts/AuthLayout';
import DashboardLayout from '@layouts/DashboardLayout';

// Pages
import Login from '@pages/Login';
import Signup from '@pages/Signup';
import Dashboard from '@pages/Dashboard';
import Profile from '@pages/Profile';
import Notifications from '@pages/Notifications';
import DiscoverList from '@pages/DiscoverList';
import NotFound from '@pages/NotFound';

function App() {
  return (
    <BrowserRouter>
      <ThemeProvider>
        <AuthProvider>
          <Routes>
            {/* Public Routes */}
            <Route element={<AuthLayout />}>
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
            </Route>

            {/* Protected Routes */}
            <Route
              element={
                <ProtectedRoute>
                  <DashboardLayout />
                </ProtectedRoute>
              }
            >
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/discover" element={<DiscoverList />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/settings" element={<Profile />} />
              <Route path="/notifications" element={<Notifications />} />
              
              {/* Category pages - using DiscoverList as placeholder */}
              <Route path="/books" element={<DiscoverList />} />
              <Route path="/music" element={<DiscoverList />} />
              <Route path="/fashion" element={<DiscoverList />} />
              <Route path="/films" element={<DiscoverList />} />
              <Route path="/art" element={<DiscoverList />} />
              <Route path="/spaces" element={<DiscoverList />} />
              <Route path="/messages" element={<DiscoverList />} />
            </Route>

            {/* Default redirect */}
            <Route path="/" element={<Navigate to="/dashboard" replace />} />

            {/* 404 */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </AuthProvider>
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
