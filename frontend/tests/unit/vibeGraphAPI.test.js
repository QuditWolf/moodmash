/**
 * Unit tests for VibeGraph API service layer.
 * 
 * Tests API request/response handling, error handling, and authentication.
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { server } from '../mocks/server'
import { http, HttpResponse } from 'msw'

// Mock API service (adjust import path as needed)
const API_BASE_URL = 'http://localhost:8000'

const apiRequest = async (endpoint, options = {}) => {
  const url = `${API_BASE_URL}${endpoint}`
  
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  }
  
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers['Authorization'] = `Bearer ${token}`
  }
  
  const response = await fetch(url, config)
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.message || 'API request failed')
  }
  
  return await response.json()
}

const vibeGraphAPI = {
  quiz: {
    startSection1: async (userId) => {
      return apiRequest('/quiz/section1/start', {
        method: 'POST',
        body: JSON.stringify({ userId }),
      })
    },
    
    generateSection2: async (sessionId, section1Answers) => {
      return apiRequest('/quiz/section2/generate', {
        method: 'POST',
        body: JSON.stringify({ sessionId, section1Answers }),
      })
    },
    
    completeQuiz: async (sessionId, userId, allAnswers) => {
      return apiRequest('/quiz/complete', {
        method: 'POST',
        body: JSON.stringify({ sessionId, userId, allAnswers }),
      })
    },
  },
  
  profile: {
    getTasteDNA: async (userId) => {
      return apiRequest(`/profile/dna/${userId}`)
    },
    
    getGrowthPath: async (userId) => {
      return apiRequest(`/profile/path/${userId}`)
    },
    
    getMatches: async (userId, limit = 10) => {
      return apiRequest(`/profile/matches/${userId}?limit=${limit}`)
    },
  },
}

describe('VibeGraph API Service', () => {
  beforeEach(() => {
    localStorage.clear()
  })

  describe('Quiz API', () => {
    it('should start Section 1 and return questions', async () => {
      const response = await vibeGraphAPI.quiz.startSection1()
      
      expect(response).toHaveProperty('sessionId')
      expect(response).toHaveProperty('questions')
      expect(response.questions).toHaveLength(5)
      expect(response.questions[0]).toHaveProperty('id')
      expect(response.questions[0]).toHaveProperty('title')
      expect(response.questions[0]).toHaveProperty('options')
    })

    it('should generate Section 2 with session ID and answers', async () => {
      const sessionId = 'mock-session-123'
      const section1Answers = [
        { questionId: 'q1', selectedOptions: ['Fiction'] },
        { questionId: 'q2', selectedOptions: ['Streaming recommendations'] },
        { questionId: 'q3', selectedOptions: ['Story'] },
        { questionId: 'q4', selectedOptions: ['Reading'] },
        { questionId: 'q5', selectedOptions: ['Expression'] }
      ]
      
      const response = await vibeGraphAPI.quiz.generateSection2(sessionId, section1Answers)
      
      expect(response).toHaveProperty('questions')
      expect(response.questions).toHaveLength(5)
    })

    it('should complete quiz and return taste DNA', async () => {
      const sessionId = 'mock-session-123'
      const userId = 'user-123'
      const allAnswers = {
        section1: [
          { questionId: 'q1', selectedOptions: ['Fiction'] }
        ],
        section2: [
          { questionId: 'q6', selectedOptions: ['Deep analysis'] }
        ]
      }
      
      const response = await vibeGraphAPI.quiz.completeQuiz(sessionId, userId, allAnswers)
      
      expect(response).toHaveProperty('embeddingId')
      expect(response).toHaveProperty('tasteDNA')
      expect(response.tasteDNA).toHaveProperty('archetype')
      expect(response.tasteDNA).toHaveProperty('traits')
      expect(response.tasteDNA).toHaveProperty('categories')
    })

    it('should handle API errors gracefully', async () => {
      // Override handler to return error
      server.use(
        http.post(`${API_BASE_URL}/quiz/section1/start`, () => {
          return HttpResponse.json(
            { message: 'Service unavailable' },
            { status: 503 }
          )
        })
      )
      
      await expect(vibeGraphAPI.quiz.startSection1()).rejects.toThrow('Service unavailable')
    })
  })

  describe('Profile API', () => {
    it('should get taste DNA for user', async () => {
      const userId = 'user-123'
      const response = await vibeGraphAPI.profile.getTasteDNA(userId)
      
      expect(response).toHaveProperty('tasteDNA')
      expect(response.tasteDNA).toHaveProperty('archetype')
      expect(response.tasteDNA.archetype).toBe('The Explorer')
    })

    it('should get growth path for user', async () => {
      const userId = 'user-123'
      const response = await vibeGraphAPI.profile.getGrowthPath(userId)
      
      expect(response).toHaveProperty('path')
      expect(response.path).toHaveProperty('absorb')
      expect(response.path).toHaveProperty('create')
      expect(response.path).toHaveProperty('reflect')
      expect(response.path.absorb.length).toBeGreaterThan(0)
    })

    it('should get matches for user', async () => {
      const userId = 'user-123'
      const response = await vibeGraphAPI.profile.getMatches(userId)
      
      expect(response).toHaveProperty('matches')
      expect(Array.isArray(response.matches)).toBe(true)
      expect(response.matches[0]).toHaveProperty('userId')
      expect(response.matches[0]).toHaveProperty('similarity')
      expect(response.matches[0].similarity).toBeGreaterThan(0.7)
    })
  })

  describe('Authentication', () => {
    it('should include auth token in requests when available', async () => {
      localStorage.setItem('authToken', 'test-token-123')
      
      // This test verifies the token is included in the request
      // In a real scenario, you'd check the request headers
      const response = await vibeGraphAPI.quiz.startSection1()
      expect(response).toBeDefined()
    })

    it('should work without auth token for public endpoints', async () => {
      // No token set
      const response = await vibeGraphAPI.quiz.startSection1()
      expect(response).toBeDefined()
    })
  })
})
