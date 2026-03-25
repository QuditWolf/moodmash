import { useNavigate } from 'react-router-dom'
import { ArrowRight, Sparkles, Zap, Shield } from 'lucide-react'

const Landing = () => {
  const navigate = useNavigate()

  // Check if user already has a session
  const sessionId = sessionStorage.getItem('session_id')
  
  // If they have a session, show them a different CTA
  const handleCTA = () => {
    if (sessionId) {
      navigate(`/dna/${sessionId}`)
    } else {
      navigate('/onboard')
    }
  }

  return (
    <div className="min-h-screen bg-background relative overflow-hidden">
      {/* Animated gradient background */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl animate-pulse"></div>
        <div className="absolute top-0 right-1/4 w-96 h-96 bg-red-500 rounded-full mix-blend-multiply filter blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
        <div className="absolute bottom-0 left-1/2 w-96 h-96 bg-cyan-500 rounded-full mix-blend-multiply filter blur-3xl animate-pulse" style={{ animationDelay: '2s' }}></div>
      </div>

      <div className="relative z-10 min-h-screen flex flex-col items-center justify-center px-6">
        {/* Logo with glow */}
        <div className="mb-12">
          <h1 className="text-32 font-bold bg-gradient-to-r from-red-500 via-purple-500 to-cyan-500 bg-clip-text text-transparent">
            MoodMash
          </h1>
        </div>

        {/* Hero */}
        <div className="max-w-4xl text-center space-y-8">
          <h2 className="text-40 sm:text-48 font-bold leading-tight">
            Every platform optimizes for your{' '}
            <span className="bg-gradient-to-r from-red-500 to-purple-500 bg-clip-text text-transparent">
              attention
            </span>
            .
            <br />
            We optimize for your{' '}
            <span className="bg-gradient-to-r from-cyan-500 to-purple-500 bg-clip-text text-transparent">
              growth
            </span>
            .
          </h2>

          <p className="text-18 text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            An AI-powered taste engine that understands who you are across music,
            films, books, art — and turns it into intentional growth.
          </p>
        </div>

        {/* Feature pills with vibrant colors */}
        <div className="flex flex-wrap justify-center gap-4 mt-12">
          <div className="flex items-center gap-3 px-6 py-3 rounded-full glass">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
              <Sparkles className="w-4 h-4 text-white" strokeWidth={2} />
            </div>
            <span className="text-14 font-semibold text-foreground">Taste DNA</span>
          </div>
          <div className="flex items-center gap-3 px-6 py-3 rounded-full glass">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-500 to-blue-500 flex items-center justify-center">
              <Zap className="w-4 h-4 text-white" strokeWidth={2} />
            </div>
            <span className="text-14 font-semibold text-foreground">Growth Paths</span>
          </div>
          <div className="flex items-center gap-3 px-6 py-3 rounded-full glass">
            <div className="w-8 h-8 rounded-full bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center">
              <Shield className="w-4 h-4 text-white" strokeWidth={2} />
            </div>
            <span className="text-14 font-semibold text-foreground">Privacy-first</span>
          </div>
        </div>

        {/* CTA with gradient */}
        <button
          onClick={handleCTA}
          className="mt-16 flex items-center gap-3 px-10 py-5 rounded-full text-16 font-bold bg-gradient-to-r from-red-600 to-red-500 hover:from-red-500 hover:to-red-400 text-white shadow-2xl hover:shadow-red-500/50 hover:scale-105 transition-all duration-300 glow"
        >
          {sessionId ? 'View Your DNA' : 'Discover Your Taste DNA'}
          <ArrowRight className="w-5 h-5" strokeWidth={2.5} />
        </button>

        {/* Footer note */}
        <p className="mt-16 text-13 text-muted-foreground">
          Built for India's youth • Your data stays yours
        </p>
      </div>
    </div>
  )
}

export default Landing
