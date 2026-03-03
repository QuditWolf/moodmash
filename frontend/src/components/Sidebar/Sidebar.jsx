import { NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  Home, 
  Compass, 
  Users, 
  BookOpen, 
  Music, 
  Shirt, 
  Film,
  Palette,
  MessageCircle,
  Settings,
  LogOut
} from 'lucide-react';
import { useAuth } from '@contexts/AuthContext';
import './Sidebar.css';

const Sidebar = () => {
  const { logout } = useAuth();

  const mainLinks = [
    { to: '/dashboard', icon: Home, label: 'Dashboard' },
    { to: '/discover', icon: Compass, label: 'Discover' },
    { to: '/spaces', icon: Users, label: 'Vibe Spaces' },
  ];

  const categoryLinks = [
    { to: '/books', icon: BookOpen, label: 'Books' },
    { to: '/music', icon: Music, label: 'Music' },
    { to: '/fashion', icon: Shirt, label: 'Fashion' },
    { to: '/films', icon: Film, label: 'Films' },
    { to: '/art', icon: Palette, label: 'Art' },
  ];

  const bottomLinks = [
    { to: '/messages', icon: MessageCircle, label: 'Messages' },
    { to: '/settings', icon: Settings, label: 'Settings' },
  ];

  const handleLogout = async () => {
    await logout();
    window.location.href = '/login';
  };

  return (
    <motion.aside 
      className="sidebar"
      initial={{ x: -300 }}
      animate={{ x: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="sidebar-content">
        <nav className="sidebar-nav">
          <div className="sidebar-section">
            {mainLinks.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) => 
                  `sidebar-link ${isActive ? 'active' : ''}`
                }
              >
                <link.icon size={20} />
                <span>{link.label}</span>
              </NavLink>
            ))}
          </div>

          <div className="sidebar-section">
            <h4 className="sidebar-section-title">Categories</h4>
            {categoryLinks.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) => 
                  `sidebar-link ${isActive ? 'active' : ''}`
                }
              >
                <link.icon size={20} />
                <span>{link.label}</span>
              </NavLink>
            ))}
          </div>
        </nav>

        <div className="sidebar-footer">
          {bottomLinks.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) => 
                `sidebar-link ${isActive ? 'active' : ''}`
              }
            >
              <link.icon size={20} />
              <span>{link.label}</span>
            </NavLink>
          ))}
          
          <button className="sidebar-link" onClick={handleLogout}>
            <LogOut size={20} />
            <span>Logout</span>
          </button>
        </div>
      </div>
    </motion.aside>
  );
};

export default Sidebar;
