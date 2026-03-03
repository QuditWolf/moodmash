// API Base URL from environment variables
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// Helper function to handle API requests
const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  // Add auth token if available
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(url, config);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'API request failed');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    throw error;
  }
};

// Authentication APIs
export const authAPI = {
  login: async (email, password) => {
    return apiRequest('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
  },

  signup: async (email, password, name) => {
    return apiRequest('/auth/signup', {
      method: 'POST',
      body: JSON.stringify({ email, password, name }),
    });
  },

  logout: async () => {
    return apiRequest('/auth/logout', {
      method: 'POST',
    });
  },

  getCurrentUser: async () => {
    return apiRequest('/auth/me');
  },
};

// User APIs
export const userAPI = {
  updateProfile: async (updates) => {
    return apiRequest('/users/profile', {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  },

  uploadAvatar: async (file) => {
    const formData = new FormData();
    formData.append('avatar', file);

    return apiRequest('/users/avatar', {
      method: 'POST',
      body: formData,
      headers: {}, // Remove Content-Type to let browser set it with boundary
    });
  },
};

// Recommendations API
export const recommendationsAPI = {
  getPersonalized: async (category = null, limit = 20) => {
    const params = new URLSearchParams();
    if (category) params.append('category', category);
    params.append('limit', limit);

    return apiRequest(`/recommendations?${params.toString()}`);
  },

  getSimilar: async (itemId) => {
    return apiRequest(`/recommendations/similar/${itemId}`);
  },
};

// Vibe Spaces API
export const vibeSpacesAPI = {
  getAll: async () => {
    return apiRequest('/spaces');
  },

  getById: async (spaceId) => {
    return apiRequest(`/spaces/${spaceId}`);
  },

  join: async (spaceId) => {
    return apiRequest(`/spaces/${spaceId}/join`, {
      method: 'POST',
    });
  },

  leave: async (spaceId) => {
    return apiRequest(`/spaces/${spaceId}/leave`, {
      method: 'POST',
    });
  },
};

// Content API
export const contentAPI = {
  search: async (query, filters = {}) => {
    const params = new URLSearchParams({ q: query, ...filters });
    return apiRequest(`/content/search?${params.toString()}`);
  },

  save: async (itemId) => {
    return apiRequest('/content/save', {
      method: 'POST',
      body: JSON.stringify({ itemId }),
    });
  },

  getSaved: async () => {
    return apiRequest('/content/saved');
  },
};

// Notifications API
export const notificationsAPI = {
  getAll: async () => {
    return apiRequest('/notifications');
  },

  markAsRead: async (notificationId) => {
    return apiRequest(`/notifications/${notificationId}/read`, {
      method: 'PUT',
    });
  },

  markAllAsRead: async () => {
    return apiRequest('/notifications/read-all', {
      method: 'PUT',
    });
  },
};

export default {
  auth: authAPI,
  user: userAPI,
  recommendations: recommendationsAPI,
  vibeSpaces: vibeSpacesAPI,
  content: contentAPI,
  notifications: notificationsAPI,
};
