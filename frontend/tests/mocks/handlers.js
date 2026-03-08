/**
 * MSW request handlers for mocking VibeGraph API endpoints.
 * 
 * These handlers intercept API calls during testing and return mock responses.
 */

import { http, HttpResponse } from 'msw'

const API_BASE_URL = 'http://localhost:8000'

export const handlers = [
  // POST /quiz/section1/start
  http.post(`${API_BASE_URL}/quiz/section1/start`, () => {
    return HttpResponse.json({
      sessionId: 'mock-session-123',
      questions: [
        {
          id: 'q1',
          title: 'What type of books do you enjoy?',
          category: 'Books',
          options: ['Fiction', 'Non-fiction', 'Poetry', 'Technical'],
          multiSelect: true
        },
        {
          id: 'q2',
          title: 'How do you discover new music?',
          category: 'Music',
          options: ['Streaming recommendations', 'Friends', 'Radio', 'Concerts'],
          multiSelect: false
        },
        {
          id: 'q3',
          title: 'What draws you to a film?',
          category: 'Films',
          options: ['Story', 'Visuals', 'Acting', 'Director'],
          multiSelect: true
        },
        {
          id: 'q4',
          title: 'How do you prefer to learn?',
          category: 'Learning',
          options: ['Reading', 'Watching', 'Doing', 'Discussing'],
          multiSelect: false
        },
        {
          id: 'q5',
          title: 'What motivates your creative work?',
          category: 'Creativity',
          options: ['Expression', 'Problem-solving', 'Connection', 'Exploration'],
          multiSelect: true
        }
      ],
      expiresAt: Date.now() + 3600000
    })
  }),

  // POST /quiz/section2/generate
  http.post(`${API_BASE_URL}/quiz/section2/generate`, () => {
    return HttpResponse.json({
      questions: [
        {
          id: 'q6',
          title: 'Based on your interests, which appeals more?',
          category: 'Books',
          options: ['Deep analysis', 'Broad exploration'],
          multiSelect: false
        },
        {
          id: 'q7',
          title: 'When consuming content, you prefer:',
          category: 'General',
          options: ['Curated recommendations', 'Serendipitous discovery'],
          multiSelect: false
        },
        {
          id: 'q8',
          title: 'Your ideal creative project involves:',
          category: 'Creativity',
          options: ['Solo work', 'Collaboration', 'Both equally'],
          multiSelect: false
        },
        {
          id: 'q9',
          title: 'You value content that is:',
          category: 'General',
          options: ['Challenging', 'Accessible', 'Experimental'],
          multiSelect: true
        },
        {
          id: 'q10',
          title: 'Your taste evolution is driven by:',
          category: 'General',
          options: ['Intentional exploration', 'Natural drift', 'External influence'],
          multiSelect: false
        }
      ]
    })
  }),

  // POST /quiz/complete
  http.post(`${API_BASE_URL}/quiz/complete`, () => {
    return HttpResponse.json({
      embeddingId: 'emb-123',
      tasteDNA: {
        archetype: 'The Explorer',
        traits: [
          {
            name: 'Curiosity',
            score: 8.5,
            description: 'High curiosity and openness to new experiences'
          },
          {
            name: 'Depth',
            score: 7.2,
            description: 'Preference for deep, meaningful content'
          },
          {
            name: 'Intentionality',
            score: 6.8,
            description: 'Balanced approach to content discovery'
          }
        ],
        categories: [
          {
            category: 'Books',
            preferences: ['Philosophy', 'Science Fiction', 'Essays'],
            intensity: 8
          },
          {
            category: 'Music',
            preferences: ['Jazz', 'Classical', 'Experimental'],
            intensity: 6
          },
          {
            category: 'Films',
            preferences: ['Art House', 'Documentary', 'Foreign'],
            intensity: 7
          }
        ],
        description: 'You are an Explorer archetype with high curiosity and a preference for depth over breadth.'
      }
    })
  }),

  // GET /profile/dna/:userId
  http.get(`${API_BASE_URL}/profile/dna/:userId`, () => {
    return HttpResponse.json({
      tasteDNA: {
        archetype: 'The Explorer',
        traits: [
          {
            name: 'Curiosity',
            score: 8.5,
            description: 'High curiosity and openness'
          }
        ],
        categories: [
          {
            category: 'Books',
            preferences: ['Philosophy', 'Science Fiction'],
            intensity: 8
          }
        ],
        description: 'An explorer archetype'
      }
    })
  }),

  // GET /profile/path/:userId
  http.get(`${API_BASE_URL}/profile/path/:userId`, () => {
    return HttpResponse.json({
      path: {
        absorb: [
          {
            id: 'abs-1',
            title: 'Read "Thinking, Fast and Slow"',
            description: 'Explore cognitive biases',
            category: 'Books',
            estimatedTime: '8 hours',
            difficulty: 'intermediate'
          }
        ],
        create: [
          {
            id: 'cre-1',
            title: 'Write a reflective essay',
            description: 'Document your learning journey',
            category: 'Writing',
            estimatedTime: '2 hours',
            difficulty: 'beginner'
          }
        ],
        reflect: [
          {
            id: 'ref-1',
            title: 'Journal about your taste evolution',
            description: 'Track how your preferences change',
            category: 'Reflection',
            estimatedTime: '30 minutes',
            difficulty: 'beginner'
          }
        ],
        generatedAt: Date.now()
      }
    })
  }),

  // GET /profile/matches/:userId
  http.get(`${API_BASE_URL}/profile/matches/:userId`, () => {
    return HttpResponse.json({
      matches: [
        {
          userId: 'user-456',
          username: 'tastemate1',
          similarity: 0.89,
          sharedTraits: ['Curiosity', 'Depth'],
          archetype: 'The Curator'
        },
        {
          userId: 'user-789',
          username: 'tastemate2',
          similarity: 0.82,
          sharedTraits: ['Intentionality'],
          archetype: 'The Explorer'
        }
      ]
    })
  }),

  // Error handler for testing error states
  http.post(`${API_BASE_URL}/quiz/error`, () => {
    return HttpResponse.json(
      { message: 'Internal server error' },
      { status: 500 }
    )
  })
]
