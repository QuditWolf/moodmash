// VibeGraph Backend API Service
// Handles all communication with the VibeGraph serverless backend

import { getLogger } from '../utils/logger';

const logger = getLogger('VibeGraphAPI');

// API Base URL from environment variables
const API_BASE_URL = import.meta.env.VITE_VIBEGRAPH_API_URL || 'http://localhost:3000';

/**
 * Helper function to handle API requests with authentication
 * @param {string} endpoint - API endpoint path
 * @param {object} options - Fetch options
 * @returns {Promise<object>} - Parsed JSON response
 */
const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`;
  const startTime = performance.now();
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  // Add authentication token from localStorage if available
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    logger.debug(`API Request: ${options.method || 'GET'} ${endpoint}`, {
      url,
      method: options.method || 'GET',
    });

    const response = await fetch(url, config);
    const duration = performance.now() - startTime;
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ message: 'API request failed' }));
      
      // Log API error
      logger.logApiError(
        options.method || 'GET',
        endpoint,
        new Error(error.message || 'API request failed'),
        {
          status: response.status,
          duration_ms: Math.round(duration),
        }
      );
      
      throw new Error(error.message || 'API request failed');
    }
    
    // Log successful API request
    logger.logApiRequest(
      options.method || 'GET',
      endpoint,
      response.status,
      Math.round(duration)
    );
    
    return await response.json();
  } catch (error) {
    const duration = performance.now() - startTime;
    
    // Log network or parsing error
    if (!error.message.includes('API request failed')) {
      logger.logApiError(
        options.method || 'GET',
        endpoint,
        error,
        {
          duration_ms: Math.round(duration),
          error_type: 'NetworkError',
        }
      );
    }
    
    throw error;
  }
};

// Quiz API methods
export const quizAPI = {
  /**
   * Start Section 1 of the adaptive quiz
   * @param {string} userId - Optional user ID for authenticated users
   * @returns {Promise<{sessionId: string, questions: Array, expiresAt: number}>}
   */
  startSection1: async (userId = null) => {
    return apiRequest('/quiz/section1/start', {
      method: 'POST',
      body: JSON.stringify({ userId }),
    });
  },

  /**
   * Generate adaptive Section 2 questions based on Section 1 answers
   * @param {string} sessionId - Session ID from Section 1
   * @param {Array} section1Answers - Array of answer objects with questionId and selectedOptions
   * @returns {Promise<{questions: Array}>}
   */
  generateSection2: async (sessionId, section1Answers) => {
    return apiRequest('/quiz/section2/generate', {
      method: 'POST',
      body: JSON.stringify({ sessionId, section1Answers }),
    });
  },

  /**
   * Complete the quiz and generate taste profile
   * @param {string} sessionId - Session ID
   * @param {string} userId - User ID
   * @param {object} allAnswers - Object containing section1 and section2 answer arrays
   * @returns {Promise<{embeddingId: string, tasteDNA: object}>}
   */
  completeQuiz: async (sessionId, userId, allAnswers) => {
    return apiRequest('/quiz/complete', {
      method: 'POST',
      body: JSON.stringify({ sessionId, userId, allAnswers }),
    });
  },
};

// Profile API methods
export const profileAPI = {
  /**
   * Get user's taste DNA profile
   * @param {string} userId - User ID
   * @returns {Promise<{tasteDNA: object}>}
   */
  getTasteDNA: async (userId) => {
    return apiRequest(`/profile/dna/${userId}`);
  },

  /**
   * Get user's personalized growth path
   * @param {string} userId - User ID
   * @returns {Promise<{path: object}>}
   */
  getGrowthPath: async (userId) => {
    return apiRequest(`/profile/path/${userId}`);
  },

  /**
   * Get taste matches for user
   * @param {string} userId - User ID
   * @param {number} limit - Maximum number of matches to return (default: 10, max: 50)
   * @returns {Promise<{matches: Array}>}
   */
  getMatches: async (userId, limit = 10) => {
    return apiRequest(`/profile/matches/${userId}?limit=${limit}`);
  },

  /**
   * Get behavioral analytics for user
   * @param {string} userId - User ID
   * @returns {Promise<{analytics: object}>}
   */
  getAnalytics: async (userId) => {
    return apiRequest(`/profile/analytics/${userId}`);
  },
};

// Export combined API object
export const vibeGraphAPI = {
  quiz: quizAPI,
  profile: profileAPI,
};

export default vibeGraphAPI;
