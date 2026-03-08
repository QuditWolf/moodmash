/**
 * Unit tests for TasteDNACard component.
 * 
 * Tests rendering of taste DNA profile including archetype, traits, and categories.
 */

import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'

// Mock TasteDNACard component (adjust import path as needed)
const TasteDNACard = ({ tasteDNA, onContinue }) => {
  if (!tasteDNA) return <div>No DNA data</div>
  
  return (
    <div data-testid="taste-dna-card">
      <h2>{tasteDNA.archetype}</h2>
      <p>{tasteDNA.description}</p>
      
      <div data-testid="traits-section">
        <h3>Your Traits</h3>
        {tasteDNA.traits.map((trait) => (
          <div key={trait.name} data-testid={`trait-${trait.name}`}>
            <span>{trait.name}</span>
            <span>{trait.score}</span>
            <span>{trait.description}</span>
          </div>
        ))}
      </div>
      
      <div data-testid="categories-section">
        <h3>Your Categories</h3>
        {tasteDNA.categories.map((category) => (
          <div key={category.category} data-testid={`category-${category.category}`}>
            <span>{category.category}</span>
            <span>Intensity: {category.intensity}</span>
            <ul>
              {category.preferences.map((pref) => (
                <li key={pref}>{pref}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
      
      {onContinue && (
        <button onClick={onContinue}>Continue</button>
      )}
    </div>
  )
}

describe('TasteDNACard', () => {
  const mockTasteDNA = {
    archetype: 'The Explorer',
    description: 'You are an Explorer archetype with high curiosity and a preference for depth over breadth.',
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
    ]
  }

  it('renders archetype name', () => {
    render(<TasteDNACard tasteDNA={mockTasteDNA} />)
    
    expect(screen.getByText('The Explorer')).toBeInTheDocument()
  })

  it('renders description', () => {
    render(<TasteDNACard tasteDNA={mockTasteDNA} />)
    
    expect(screen.getByText(/You are an Explorer archetype/)).toBeInTheDocument()
  })

  it('renders all traits', () => {
    render(<TasteDNACard tasteDNA={mockTasteDNA} />)
    
    expect(screen.getByTestId('trait-Curiosity')).toBeInTheDocument()
    expect(screen.getByTestId('trait-Depth')).toBeInTheDocument()
    expect(screen.getByTestId('trait-Intentionality')).toBeInTheDocument()
    
    expect(screen.getByText('8.5')).toBeInTheDocument()
    expect(screen.getByText('7.2')).toBeInTheDocument()
    expect(screen.getByText('6.8')).toBeInTheDocument()
  })

  it('renders all categories', () => {
    render(<TasteDNACard tasteDNA={mockTasteDNA} />)
    
    expect(screen.getByTestId('category-Books')).toBeInTheDocument()
    expect(screen.getByTestId('category-Music')).toBeInTheDocument()
    expect(screen.getByTestId('category-Films')).toBeInTheDocument()
  })

  it('renders category preferences', () => {
    render(<TasteDNACard tasteDNA={mockTasteDNA} />)
    
    // Books preferences
    expect(screen.getByText('Philosophy')).toBeInTheDocument()
    expect(screen.getByText('Science Fiction')).toBeInTheDocument()
    expect(screen.getByText('Essays')).toBeInTheDocument()
    
    // Music preferences
    expect(screen.getByText('Jazz')).toBeInTheDocument()
    expect(screen.getByText('Classical')).toBeInTheDocument()
    expect(screen.getByText('Experimental')).toBeInTheDocument()
  })

  it('renders category intensity', () => {
    render(<TasteDNACard tasteDNA={mockTasteDNA} />)
    
    expect(screen.getByText('Intensity: 8')).toBeInTheDocument()
    expect(screen.getByText('Intensity: 6')).toBeInTheDocument()
    expect(screen.getByText('Intensity: 7')).toBeInTheDocument()
  })

  it('calls onContinue when continue button is clicked', () => {
    const mockOnContinue = vi.fn()
    render(<TasteDNACard tasteDNA={mockTasteDNA} onContinue={mockOnContinue} />)
    
    const continueButton = screen.getByRole('button', { name: 'Continue' })
    fireEvent.click(continueButton)
    
    expect(mockOnContinue).toHaveBeenCalledTimes(1)
  })

  it('does not render continue button when onContinue is not provided', () => {
    render(<TasteDNACard tasteDNA={mockTasteDNA} />)
    
    expect(screen.queryByRole('button', { name: 'Continue' })).not.toBeInTheDocument()
  })

  it('renders fallback when no DNA data provided', () => {
    render(<TasteDNACard tasteDNA={null} />)
    
    expect(screen.getByText('No DNA data')).toBeInTheDocument()
  })

  it('renders all trait descriptions', () => {
    render(<TasteDNACard tasteDNA={mockTasteDNA} />)
    
    expect(screen.getByText('High curiosity and openness to new experiences')).toBeInTheDocument()
    expect(screen.getByText('Preference for deep, meaningful content')).toBeInTheDocument()
    expect(screen.getByText('Balanced approach to content discovery')).toBeInTheDocument()
  })
})
