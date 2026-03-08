import { useState } from 'react';
import { Camera, Mail, User as UserIcon } from 'lucide-react';
import { Card, Button, Input, FileUpload } from '@components';
import { useAuth } from '@contexts/AuthContext';
import './Profile.css';

const Profile = () => {
  const { user, updateProfile } = useAuth();
  const [editing, setEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    bio: '',
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      await updateProfile(formData);
      setEditing(false);
    } catch (error) {
      console.error('Failed to update profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const vibeProfile = {
    dominantVibes: ['Soft rebellion', 'Dark academia minimal', 'Ethereal calm'],
    tasteGraphStrength: 87,
    categories: [
      { name: 'Books', score: 92 },
      { name: 'Music', score: 85 },
      { name: 'Fashion', score: 78 },
      { name: 'Films', score: 90 },
      { name: 'Art', score: 81 },
    ],
  };

  return (
    <div className="profile-page">
      <h1>Profile & Settings</h1>

      <div className="profile-grid">
        {/* Profile Info */}
        <Card variant="elevated">
          <div className="profile-header">
            <div className="profile-avatar-container">
              <div className="profile-avatar">
                {user?.avatar ? (
                  <img src={user.avatar} alt={user.name} />
                ) : (
                  <UserIcon size={48} />
                )}
              </div>
              <button className="avatar-upload-btn">
                <Camera size={16} />
              </button>
            </div>
            
            {!editing && (
              <Button variant="outline" onClick={() => setEditing(true)}>
                Edit Profile
              </Button>
            )}
          </div>

          {editing ? (
            <form onSubmit={handleSubmit} className="profile-form">
              <Input
                name="name"
                label="Full Name"
                value={formData.name}
                onChange={handleChange}
                leftIcon={<UserIcon size={18} />}
                required
              />
              
              <Input
                name="email"
                type="email"
                label="Email"
                value={formData.email}
                onChange={handleChange}
                leftIcon={<Mail size={18} />}
                required
              />

              <div className="input-wrapper">
                <label className="input-label">Bio</label>
                <textarea
                  name="bio"
                  value={formData.bio}
                  onChange={handleChange}
                  placeholder="Tell us about your aesthetic..."
                  className="profile-textarea"
                  rows="4"
                />
              </div>

              <div className="profile-actions">
                <Button
                  type="button"
                  variant="ghost"
                  onClick={() => setEditing(false)}
                >
                  Cancel
                </Button>
                <Button type="submit" variant="primary" loading={loading}>
                  Save Changes
                </Button>
              </div>
            </form>
          ) : (
            <div className="profile-info">
              <div className="profile-field">
                <span className="field-label">Name</span>
                <span className="field-value">{user?.name}</span>
              </div>
              <div className="profile-field">
                <span className="field-label">Email</span>
                <span className="field-value">{user?.email}</span>
              </div>
              <div className="profile-field">
                <span className="field-label">Member Since</span>
                <span className="field-value">January 2026</span>
              </div>
            </div>
          )}
        </Card>

        {/* Vibe Profile */}
        <Card variant="elevated">
          <h3 className="card-title">Your Vibe Profile</h3>
          
          <div className="vibe-score">
            <div className="vibe-score-circle">
              <svg viewBox="0 0 100 100">
                <circle cx="50" cy="50" r="40" className="vibe-score-bg" />
                <circle 
                  cx="50" 
                  cy="50" 
                  r="40" 
                  className="vibe-score-progress"
                  style={{
                    strokeDasharray: `${vibeProfile.tasteGraphStrength * 2.51}, 251`,
                  }}
                />
              </svg>
              <div className="vibe-score-value">{vibeProfile.tasteGraphStrength}</div>
            </div>
            <div>
              <h4>Taste Graph Strength</h4>
              <p>Your aesthetic identity is well-defined</p>
            </div>
          </div>

          <div className="dominant-vibes">
            <h4>Dominant Vibes</h4>
            <div className="vibe-tags">
              {vibeProfile.dominantVibes.map((vibe) => (
                <span key={vibe} className="vibe-tag">{vibe}</span>
              ))}
            </div>
          </div>

          <div className="category-scores">
            <h4>Category Scores</h4>
            {vibeProfile.categories.map((category) => (
              <div key={category.name} className="category-score">
                <div className="category-info">
                  <span>{category.name}</span>
                  <span>{category.score}</span>
                </div>
                <div className="category-bar">
                  <div 
                    className="category-bar-fill"
                    style={{ width: `${category.score}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Profile;
