import { motion } from 'framer-motion';
import { 
  Layers,
  Compass, 
  Grid3x3,
  Sparkles,
  User,
  BookOpen, 
  Music, 
  Film,
  Palette,
  Settings
} from 'lucide-react';
import './Sidebar.css';

const Sidebar = () => {
  const mainLinks = [
    { icon: Layers, label: 'Feed', active: true },
    { icon: Compass, label: 'Explore', active: false },
    { icon: Grid3x3, label: 'Moodboards', active: false },
    { icon: Sparkles, label: 'Vibes', active: false },
    { icon: User, label: 'Profile', active: false },
  ];

  const categoryLinks = [
    { icon: BookOpen, label: 'Books' },
    { icon: Music, label: 'Music' },
    { icon: Film, label: 'Films' },
    { icon: Palette, label: 'Art' },
  ];

  return (
    <motion.aside 
      className="sidebar"
      initial={{ x: -300 }}
      animate={{ x: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="sidebar-content">
        <div className="sidebar-logo">
          <h2>VibeGraph</h2>
        </div>
        
        <nav className="sidebar-nav">
          <div className="sidebar-section">
            {mainLinks.map((link) => (
              <button
                key={link.label}
                className={`sidebar-link ${link.active ? 'active' : ''}`}
              >
                <link.icon size={20} />
                <span>{link.label}</span>
              </button>
            ))}
          </div>

          <div className="sidebar-section">
            <h4 className="sidebar-section-title">Categories</h4>
            {categoryLinks.map((link) => (
              <button
                key={link.label}
                className="sidebar-link"
              >
                <link.icon size={20} />
                <span>{link.label}</span>
              </button>
            ))}
          </div>
        </nav>

        <div className="sidebar-footer">
          <button className="sidebar-link">
            <Settings size={20} />
            <span>Settings</span>
          </button>
        </div>
      </div>
    </motion.aside>
  );
};

export default Sidebar;
