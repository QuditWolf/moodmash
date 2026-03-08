import { motion } from 'framer-motion';
import { TrendingUp, Users, Sparkles, Heart } from 'lucide-react';
import { Card, Button } from '@components';
import { useAuth } from '@contexts/AuthContext';
import './Dashboard.css';

const Dashboard = () => {
  const { user } = useAuth();

  const stats = [
    { label: 'Vibe Score', value: '92', icon: Sparkles, color: 'primary' },
    { label: 'Connections', value: '234', icon: Users, color: 'secondary' },
    { label: 'Saved Items', value: '156', icon: Heart, color: 'accent' },
    { label: 'Growth', value: '+12%', icon: TrendingUp, color: 'success' },
  ];

  const vibeSpaces = [
    { name: 'Soft Rebellion', members: 1240, image: '🌸' },
    { name: 'Dark Academia Minimal', members: 892, image: '📚' },
    { name: 'Futuristic Nostalgia', members: 2103, image: '🌌' },
  ];

  const recentActivity = [
    { type: 'book', title: 'The Remains of the Day', author: 'Kazuo Ishiguro', vibe: 'Melancholic elegance' },
    { type: 'music', title: 'Clair de Lune', artist: 'Debussy', vibe: 'Ethereal calm' },
    { type: 'film', title: 'Lost in Translation', director: 'Sofia Coppola', vibe: 'Urban loneliness' },
  ];

  return (
    <div className="dashboard-page">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <div className="dashboard-header">
          <div>
            <h1>Welcome back, {user?.name || 'there'}!</h1>
            <p className="dashboard-subtitle">Here's what's happening in your aesthetic universe</p>
          </div>
          <Button variant="gradient">Discover More</Button>
        </div>

        {/* Stats Grid */}
        <div className="stats-grid">
          {stats.map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card variant="elevated" hoverable>
                <div className="stat-card">
                  <div className={`stat-icon stat-icon-${stat.color}`}>
                    <stat.icon size={24} />
                  </div>
                  <div className="stat-content">
                    <p className="stat-label">{stat.label}</p>
                    <h3 className="stat-value">{stat.value}</h3>
                  </div>
                </div>
              </Card>
            </motion.div>
          ))}
        </div>

        {/* Main Content Grid */}
        <div className="dashboard-grid">
          {/* Your Vibe Spaces */}
          <Card variant="default">
            <div className="section-header">
              <h3>Your Vibe Spaces</h3>
              <Button variant="ghost" size="sm">View All</Button>
            </div>
            <div className="vibe-spaces">
              {vibeSpaces.map((space) => (
                <div key={space.name} className="vibe-space-item">
                  <div className="vibe-space-avatar">{space.image}</div>
                  <div className="vibe-space-info">
                    <h4>{space.name}</h4>
                    <p>{space.members.toLocaleString()} members</p>
                  </div>
                  <Button variant="outline" size="sm">Join</Button>
                </div>
              ))}
            </div>
          </Card>

          {/* Recent Activity */}
          <Card variant="default">
            <div className="section-header">
              <h3>Recent Activity</h3>
              <Button variant="ghost" size="sm">See More</Button>
            </div>
            <div className="activity-list">
              {recentActivity.map((item, index) => (
                <div key={index} className="activity-item">
                  <div className={`activity-icon activity-${item.type}`}>
                    {item.type === 'book' && '📖'}
                    {item.type === 'music' && '🎵'}
                    {item.type === 'film' && '🎬'}
                  </div>
                  <div className="activity-content">
                    <h4>{item.title}</h4>
                    <p>{item.author || item.artist || item.director}</p>
                    <span className="activity-vibe">{item.vibe}</span>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Recommendation Section */}
        <Card variant="glass" className="recommendation-card">
          <div className="recommendation-content">
            <div className="recommendation-text">
              <Sparkles size={32} className="recommendation-icon" />
              <div>
                <h3>AI-Powered Recommendations</h3>
                <p>Based on your taste graph, we've curated new discoveries across books, music, fashion, and art that match your unique aesthetic.</p>
              </div>
            </div>
            <Button variant="primary" size="lg">Explore Recommendations</Button>
          </div>
        </Card>
      </motion.div>
    </div>
  );
};

export default Dashboard;
