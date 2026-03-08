import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import { Loader2, LayoutGrid, List, Music, Film, BookOpen, Palette, Sparkles, Play } from 'lucide-react'

const Feed = () => {
  const navigate = useNavigate()
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [viewMode, setViewMode] = useState('grid') // 'grid' or 'list'
  const sessionId = sessionStorage.getItem('session_id')

  useEffect(() => {
    const loadFeed = async () => {
      if (!sessionId) {
        // No session, load sample content from knowledge base
        try {
          const response = await fetch('/knowledge-base/content.json')
          const allContent = await response.json()
          // Show a random sample of 12 items
          const shuffled = allContent.sort(() => 0.5 - Math.random())
          setItems(shuffled.slice(0, 12))
          setLoading(false)
          return
        } catch (err) {
          console.error('Error loading feed:', err)
          setLoading(false)
        }
      }
      
      // If user has a session, show personalized content
      try {
        // Get user's DNA to understand their taste
        const dnaResponse = await api.get(`/api/dna/${sessionId}`)
        const dna = dnaResponse.data
        
        // Load all content
        const response = await fetch('/knowledge-base/content.json')
        const allContent = await response.json()
        
        // Filter and score content based on user's taste
        const scoredItems = allContent.map(item => {
          let score = 0
          
          // Match mood tags with DNA vibe
          if (dna.taste_markers) {
            dna.taste_markers.forEach(marker => {
              if (item.mood_tags?.some(tag => 
                tag.toLowerCase().includes(marker.toLowerCase()) || 
                marker.toLowerCase().includes(tag.toLowerCase())
              )) {
                score += 3
              }
            })
          }
          
          // Match growth tags
          if (item.growth_tags?.includes('emotional_awareness')) score += 2
          if (item.growth_tags?.includes('creative_inspiration')) score += 2
          
          // Prefer certain domains based on archetype
          if (dna.archetype?.includes('Philosopher') && item.domain === 'literature') score += 2
          if (dna.archetype?.includes('Creative') && item.domain === 'art') score += 2
          if (dna.archetype?.includes('Rhythm') && item.domain === 'music') score += 2
          
          return { ...item, score }
        })
        
        // Sort by score and take top items
        const topItems = scoredItems
          .sort((a, b) => b.score - a.score)
          .slice(0, 18)
        
        setItems(topItems)
        setLoading(false)
      } catch (err) {
        console.error('Error loading personalized feed:', err)
        // Fallback to random content
        try {
          const response = await fetch('/knowledge-base/content.json')
          const allContent = await response.json()
          const shuffled = allContent.sort(() => 0.5 - Math.random())
          setItems(shuffled.slice(0, 12))
        } catch (fallbackErr) {
          console.error('Fallback failed:', fallbackErr)
        }
        setLoading(false)
      }
    }

    loadFeed()
  }, [sessionId])

  const getIconForDomain = (domain) => {
    switch (domain) {
      case 'music': return Music
      case 'film': return Film
      case 'literature': return BookOpen
      case 'art': return Palette
      default: return Sparkles
    }
  }

  const getGradientForDomain = (domain) => {
    switch (domain) {
      case 'music': return 'from-purple-600 to-pink-600'
      case 'film': return 'from-red-600 to-orange-600'
      case 'literature': return 'from-blue-600 to-cyan-600'
      case 'art': return 'from-green-600 to-emerald-600'
      default: return 'from-purple-600 to-blue-600'
    }
  }

  const getEngagementColor = (type) => {
    switch (type) {
      case 'absorb': return 'bg-blue-500/20 text-blue-300 border-blue-500/30'
      case 'create': return 'bg-amber-500/20 text-amber-300 border-amber-500/30'
      case 'reflect': return 'bg-purple-500/20 text-purple-300 border-purple-500/30'
      default: return 'bg-white/10 text-muted-foreground border-white/20'
    }
  }

  const getImageUrl = (item) => {
    // Use Unsplash for high-quality images based on domain and title
    const query = encodeURIComponent(`${item.title} ${item.creator} ${item.domain}`)
    return `https://source.unsplash.com/400x400/?${query}`
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <Loader2 className="w-8 h-8 text-purple-500 animate-spin" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background px-6 py-12">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-10">
          <div>
            <h1 className="text-32 font-bold text-foreground mb-2">
              {sessionId ? (
                <>
                  Your <span className="bg-gradient-to-r from-purple-500 to-pink-500 bg-clip-text text-transparent">Feed</span>
                </>
              ) : (
                <>
                  <span className="bg-gradient-to-r from-cyan-500 to-blue-500 bg-clip-text text-transparent">Discover</span>
                </>
              )}
            </h1>
            <p className="text-14 text-muted-foreground">
              {sessionId 
                ? 'Content curated based on your taste DNA' 
                : 'Explore curated content from across India'}
            </p>
          </div>
          
          {/* View Mode Toggle */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => setViewMode('grid')}
              className={`p-3 rounded-lg transition-all duration-300 ${
                viewMode === 'grid'
                  ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                  : 'glass text-muted-foreground hover:text-foreground'
              }`}
            >
              <LayoutGrid className="w-5 h-5" strokeWidth={2} />
            </button>
            <button
              onClick={() => setViewMode('list')}
              className={`p-3 rounded-lg transition-all duration-300 ${
                viewMode === 'list'
                  ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                  : 'glass text-muted-foreground hover:text-foreground'
              }`}
            >
              <List className="w-5 h-5" strokeWidth={2} />
            </button>
          </div>
        </div>

        {/* No session CTA */}
        {!sessionId && (
          <div className="mb-10 rounded-2xl p-8 glass relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-600/20 to-pink-600/20"></div>
            <div className="relative z-10">
              <p className="text-16 text-foreground mb-4 font-semibold">
                🎯 Get personalized recommendations
              </p>
              <p className="text-14 text-muted-foreground mb-6">
                Complete your taste onboarding to see content matched to your unique vibe
              </p>
              <button
                onClick={() => navigate('/onboard')}
                className="px-6 py-3 rounded-full text-14 font-bold bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:from-purple-500 hover:to-pink-500 transition-all duration-300 shadow-lg hover:shadow-purple-500/50"
              >
                Start Onboarding
              </button>
            </div>
          </div>
        )}

        {/* Feed Grid */}
        {items.length > 0 ? (
          <div className={
            viewMode === 'grid'
              ? 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6'
              : 'flex flex-col gap-6'
          }>
            {items.map((item) => {
              const Icon = getIconForDomain(item.domain)
              const gradient = getGradientForDomain(item.domain)
              return (
                <div
                  key={item.id}
                  className="group rounded-2xl overflow-hidden glass card-hover cursor-pointer relative"
                  onClick={() => {
                    if (item.external_link && item.external_link !== '#') {
                      window.open(item.external_link, '_blank')
                    }
                  }}
                >
                  {/* Card Image with real photo */}
                  <div className={`aspect-square bg-gradient-to-br ${gradient} relative overflow-hidden`}>
                    <img 
                      src={getImageUrl(item)} 
                      alt={item.title}
                      className="w-full h-full object-cover"
                      onError={(e) => {
                        // Fallback to gradient with icon if image fails
                        e.target.style.display = 'none'
                        e.target.nextElementSibling.style.display = 'flex'
                      }}
                    />
                    <div className="absolute inset-0 bg-gradient-to-br from-black/40 to-black/60 hidden items-center justify-center">
                      <Icon className="w-16 h-16 text-white/80" strokeWidth={1.5} />
                    </div>
                    
                    {/* Hover overlay */}
                    <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                      <Play className="w-12 h-12 text-white" strokeWidth={2} fill="white" />
                    </div>
                  </div>
                  
                  {/* Card Content */}
                  <div className="p-5">
                    {/* Engagement Type Badge */}
                    <div className="flex items-center gap-2 mb-3">
                      <span className={`text-11 px-3 py-1 rounded-full border font-bold uppercase tracking-wider ${getEngagementColor(item.engagement_type)}`}>
                        {item.engagement_type}
                      </span>
                      <span className="text-11 text-muted-foreground uppercase tracking-wider font-semibold">
                        {item.domain}
                      </span>
                    </div>
                    
                    {/* Title & Creator */}
                    <h3 className="text-16 font-bold text-foreground mb-1 line-clamp-2 group-hover:text-purple-400 transition-colors">
                      {item.title}
                    </h3>
                    <p className="text-13 text-muted-foreground mb-3 font-medium">
                      {item.creator}
                    </p>
                    
                    {/* Description */}
                    <p className="text-12 text-muted-foreground/80 line-clamp-2 mb-4 leading-relaxed">
                      {item.description}
                    </p>
                    
                    {/* Mood Tags */}
                    <div className="flex flex-wrap gap-2">
                      {item.mood_tags?.slice(0, 3).map((tag, idx) => (
                        <span
                          key={idx}
                          className="text-10 px-2 py-1 rounded-full bg-white/5 text-muted-foreground/80 font-medium"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        ) : (
          <div className="glass rounded-2xl p-12 text-center">
            <h2 className="text-24 font-bold text-foreground mb-3">
              No Content Available
            </h2>
            <p className="text-14 text-muted-foreground mb-6">
              We couldn't load any content right now. Please try again later.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Feed
