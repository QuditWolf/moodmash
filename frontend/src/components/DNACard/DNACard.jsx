import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../../services/api'
import { Loader2, Share2, ArrowRight, Sparkles } from 'lucide-react'
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  ResponsiveContainer,
} from 'recharts'

const DNACard = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [dna, setDna] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [copied, setCopied] = useState(false)

  useEffect(() => {
    const fetchDNA = async () => {
      try {
        const data = await api.getDNA(id)
        setDna(data)
      } catch (err) {
        setError(err.message || 'Failed to load your Taste DNA.')
      } finally {
        setLoading(false)
      }
    }
    fetchDNA()
  }, [id])

  const handleShare = async () => {
    const text = `My Taste DNA: ${dna.archetype}\n\n${dna.vibe_summary}`
    try {
      await navigator.clipboard.writeText(text)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch {
      const textarea = document.createElement('textarea')
      textarea.value = text
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center px-6">
        <Loader2 className="w-8 h-8 text-purple-500 animate-spin mb-4" />
        <p className="text-14 text-muted-foreground">
          Building your Taste DNA...
        </p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center px-6">
        <p className="text-14 text-red-400 mb-6">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="px-6 py-3 rounded-full text-14 font-bold bg-gradient-to-r from-red-600 to-red-500 text-white hover:from-red-500 hover:to-red-400 transition-all duration-300"
        >
          Retry
        </button>
      </div>
    )
  }

  const radarScores = dna.radar_scores || {}
  const radarData = [
    { axis: 'Music', value: radarScores.music || 0 },
    { axis: 'Films', value: radarScores.films || 0 },
    { axis: 'Books', value: radarScores.books || 0 },
    { axis: 'Art', value: radarScores.art || 0 },
    { axis: 'Creators', value: radarScores.creators || 0 },
  ]

  const markers = dna.markers || []

  return (
    <div className="min-h-screen bg-background px-6 py-12 relative overflow-hidden">
      {/* Animated background */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl animate-pulse"></div>
        <div className="absolute top-1/3 right-1/4 w-96 h-96 bg-pink-500 rounded-full mix-blend-multiply filter blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
      </div>

      <div className="max-w-3xl mx-auto relative z-10">
        {/* Archetype Card */}
        <div className="rounded-3xl glass p-8 mb-6 relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-purple-600/20 via-pink-600/20 to-cyan-600/20"></div>
          <div className="relative z-10">
            <div className="flex items-center gap-2 mb-4">
              <Sparkles className="w-5 h-5 text-purple-400" />
              <p className="text-12 text-purple-400 font-bold uppercase tracking-wider">
                Your Archetype
              </p>
            </div>
            <h1 className="text-40 sm:text-48 font-bold bg-gradient-to-r from-purple-400 via-pink-400 to-cyan-400 bg-clip-text text-transparent mb-4 leading-tight">
              {dna.archetype}
            </h1>
            <p className="text-16 text-foreground/90 leading-relaxed">
              {dna.vibe_summary}
            </p>
          </div>
        </div>

        {/* Markers */}
        {markers.length > 0 && (
          <div className="rounded-3xl glass p-6 mb-6">
            <p className="text-12 text-cyan-400 font-bold uppercase tracking-wider mb-4">
              Taste Markers
            </p>
            <div className="flex flex-wrap gap-3">
              {markers.map((marker, i) => (
                <span
                  key={i}
                  className="px-4 py-2 text-13 font-semibold text-foreground rounded-full bg-gradient-to-r from-purple-600/30 to-pink-600/30 border border-purple-500/30"
                >
                  {marker}
                </span>
              ))}
            </div>
          </div>
        )}

        {/* Radar Chart */}
        <div className="rounded-3xl glass p-8 mb-6">
          <p className="text-12 text-pink-400 font-bold uppercase tracking-wider mb-6">
            Domain Radar
          </p>
          <div className="w-full h-80">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart data={radarData} cx="50%" cy="50%" outerRadius="70%">
                <PolarGrid stroke="rgba(168, 85, 247, 0.2)" strokeWidth={2} />
                <PolarAngleAxis
                  dataKey="axis"
                  tick={{ fill: 'rgba(255,255,255,0.8)', fontSize: 14, fontWeight: 600 }}
                />
                <Radar
                  name="Taste"
                  dataKey="value"
                  stroke="rgb(168, 85, 247)"
                  fill="rgb(168, 85, 247)"
                  fillOpacity={0.4}
                  strokeWidth={3}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4">
          <button
            onClick={() => navigate(`/path/${id}`)}
            className="flex-1 flex items-center justify-center gap-3 px-8 py-5 rounded-full text-16 font-bold bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:from-purple-500 hover:to-pink-500 transition-all duration-300 shadow-2xl hover:shadow-purple-500/50 hover:scale-105"
          >
            Get Your First Path
            <ArrowRight className="w-5 h-5" strokeWidth={2.5} />
          </button>
          <button
            onClick={handleShare}
            className="flex items-center justify-center gap-3 px-8 py-5 rounded-full text-16 font-bold glass text-foreground hover:bg-white/10 transition-all duration-300"
          >
            <Share2 className="w-5 h-5" strokeWidth={2} />
            {copied ? 'Copied!' : 'Share'}
          </button>
        </div>

        {/* Quick Links */}
        <div className="mt-8 flex justify-center gap-6 text-14 font-semibold">
          <button
            onClick={() => navigate('/feed')}
            className="text-purple-400 hover:text-purple-300 transition-colors"
          >
            Explore Feed
          </button>
          <span className="text-white/20">|</span>
          <button
            onClick={() => navigate(`/data/${id}`)}
            className="text-cyan-400 hover:text-cyan-300 transition-colors"
          >
            Data Controls
          </button>
        </div>
      </div>
    </div>
  )
}

export default DNACard
