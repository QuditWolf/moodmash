import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Moon, Sun, Bell, User } from 'lucide-react';
import { useTheme } from '@contexts/ThemeContext';
import { useAuth } from '@contexts/AuthContext';
import './Navbar.css';

const Navbar = () => {
  const { theme, toggleTheme } = useTheme();
  const { user } = useAuth();

  return (
    <motion.nav 
      className="navbar"
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="navbar-content">
        <Link to="/" className="navbar-logo">
          <span className="logo-gradient">Vibe</span>
          <span>Graph</span>
        </Link>

        <div className="navbar-actions">
          <motion.button
            className="navbar-icon-btn"
            onClick={toggleTheme}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {theme === 'dark' ? <Sun size={20} /> : <Moon size={20} />}
          </motion.button>

          {user && (
            <>
              <Link to="/notifications" className="navbar-icon-btn">
                <Bell size={20} />
                <span className="notification-badge">3</span>
              </Link>

              <Link to="/profile" className="navbar-avatar">
                {user.avatar ? (
                  <img src={user.avatar} alt={user.name} />
                ) : (
                  <User size={20} />
                )}
              </Link>
            </>
          )}
        </div>
      </div>
    </motion.nav>
  );
};

export default Navbar;
