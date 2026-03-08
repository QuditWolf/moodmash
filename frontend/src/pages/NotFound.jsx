import { Link } from 'react-router-dom';
import { Home, Search } from 'lucide-react';
import { Button } from '@components';
import './NotFound.css';

const NotFound = () => {
  return (
    <div className="not-found-page">
      <div className="not-found-content">
        <div className="not-found-animation">
          <div className="not-found-circle"></div>
          <div className="not-found-circle"></div>
          <div className="not-found-circle"></div>
        </div>

        <h1 className="not-found-title">404</h1>
        <h2 className="not-found-subtitle">Lost in the vibe space</h2>
        <p className="not-found-description">
          The page you're looking for doesn't exist in our aesthetic universe.
          Let's get you back on track.
        </p>

        <div className="not-found-actions">
          <Link to="/dashboard">
            <Button variant="gradient" size="lg" leftIcon={<Home size={20} />}>
              Go to Dashboard
            </Button>
          </Link>
          <Link to="/discover">
            <Button variant="outline" size="lg" leftIcon={<Search size={20} />}>
              Explore Discover
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
