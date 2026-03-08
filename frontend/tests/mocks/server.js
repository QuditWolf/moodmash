/**
 * Mock Service Worker (MSW) server configuration.
 * 
 * This sets up API mocking for testing without hitting real endpoints.
 */

import { setupServer } from 'msw/node'
import { handlers } from './handlers'

// Setup MSW server with default handlers
export const server = setupServer(...handlers)
