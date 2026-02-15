import { Navigate } from 'react-router-dom';
import { useAuth } from '@contexts/AuthContext';
import { Loader } from '@components';

const ProtectedRoute = ({ children }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <Loader fullScreen text="Loading..." />;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default ProtectedRoute;
