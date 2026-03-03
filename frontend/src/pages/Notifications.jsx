import { Bell, Heart, MessageCircle, Users, Sparkles } from 'lucide-react';
import { Card, Button, EmptyState } from '@components';
import './Notifications.css';

const Notifications = () => {
  const notifications = [
    {
      id: 1,
      type: 'like',
      icon: Heart,
      user: 'Sarah Chen',
      message: 'liked your moodboard "Midnight in Paris"',
      time: '2 hours ago',
      unread: true,
    },
    {
      id: 2,
      type: 'comment',
      icon: MessageCircle,
      user: 'Alex Rivera',
      message: 'commented on your book recommendation',
      content: 'This looks amazing! Adding to my list.',
      time: '5 hours ago',
      unread: true,
    },
    {
      id: 3,
      type: 'follow',
      icon: Users,
      user: 'Maya Patel',
      message: 'started following you',
      time: '1 day ago',
      unread: false,
    },
    {
      id: 4,
      type: 'match',
      icon: Sparkles,
      message: 'New vibe match! Your taste aligns 94% with "Ethereal Minimalism" space',
      time: '2 days ago',
      unread: false,
    },
    {
      id: 5,
      type: 'like',
      icon: Heart,
      user: 'Jordan Lee',
      message: 'saved your fashion aesthetic board',
      time: '3 days ago',
      unread: false,
    },
  ];

  const getIconColor = (type) => {
    switch (type) {
      case 'like': return 'var(--color-error)';
      case 'comment': return 'var(--color-primary)';
      case 'follow': return 'var(--color-secondary)';
      case 'match': return 'var(--color-accent-purple)';
      default: return 'var(--color-text-secondary)';
    }
  };

  return (
    <div className="notifications-page">
      <div className="notifications-header">
        <div>
          <h1>Notifications</h1>
          <p className="notifications-subtitle">Stay updated with your aesthetic community</p>
        </div>
        <Button variant="outline">Mark all as read</Button>
      </div>

      {notifications.length > 0 ? (
        <div className="notifications-list">
          {notifications.map((notification) => (
            <Card 
              key={notification.id} 
              variant="default" 
              className={`notification-item ${notification.unread ? 'unread' : ''}`}
              hoverable
            >
              <div className="notification-content">
                <div 
                  className="notification-icon"
                  style={{ background: getIconColor(notification.type) }}
                >
                  <notification.icon size={20} color="white" />
                </div>
                
                <div className="notification-body">
                  <p className="notification-message">
                    {notification.user && (
                      <strong>{notification.user}</strong>
                    )}
                    {' '}
                    {notification.message}
                  </p>
                  
                  {notification.content && (
                    <p className="notification-excerpt">"{notification.content}"</p>
                  )}
                  
                  <span className="notification-time">{notification.time}</span>
                </div>

                {notification.unread && (
                  <div className="notification-unread-dot"></div>
                )}
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <EmptyState
          icon={<Bell size={48} />}
          title="No notifications yet"
          description="When someone interacts with your content, you'll see it here"
        />
      )}
    </div>
  );
};

export default Notifications;
