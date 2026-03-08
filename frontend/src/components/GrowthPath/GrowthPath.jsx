import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../../services/api'
import { Loader2, Check, SkipForward, Bookmark, Clock, ArrowRight } from 'lucide-react'

const moods = [
  { name: 'focused', color: 'from-blue-600 to-cyan-600' },
  { name: 'exploratory', color: 'from-purple-600 to-pink-600' },
  { name: 'melancholic', color: 'from-indigo-600 to-purple-600' },
  { name: 'energized', color: 'from-orange-600 to-red-600' },
  { name: 'calm', color: 'from-green-600 to-emerald-600' },
]
const times = [
  { label: '15min', value: 15 },
  { label: '30min', value: 30 },
  { label: '60min', value: 60 },
  { label: '90min', value: 90 },
]

const engagementColors = {
  Absorb: { border: 'border-l-blue-500', bg: 'bg-blue-500/10', text: 'text-blue-400' },
  Create: { border: 'border-l-amber-500', bg: 'bg-amber-500/10', text: 'text-amber-400' },
  Reflect: { border: 'border-l-purple-500', bg: 'bg-purple-500/10', text: 'text-purple-400' },
}

const GrowthPath = () => {
  const { id } = useParams()
  const [mood, setMood] = useState(null)
  const [timeAvailable, setTimeAvailable] = useState(null)
  const [items, setItems] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [feedbackSent, setFeedbackSent] = useState({})

  const handleGetPath = async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await api.getPath(id, {
        mood,
        goal: 'general',
        time_available: timeAvailable,
      })
      setItems(data.items || data.path || [])
    } catch (err) {
      setError(err.message || 'Failed to generate your path.')
    } finally {
      setLoading(false)
    }
  }

  const handleFeedback = async (item, status) => {
    try {
      await api.submitFeedback(id, {
        session_id: id,
        item_id: item.id || item.title,
        status,
        reaction: status,
      })
      setFeedbackSent((prev) => ({
        ...prev,
        [item.id || item.title]: status,
      }))
    } catch (err) {
      console.error('Feedback error:', err)
    }
  }

  // Selection phase
  if (!items && !loading) {
    return (
      <div className="min-h-screen bg-background px-6 py-12 relative overflow-hidden">
        {/* Animated background */}
        <div className="absolute inset-0 opacity-20">
          <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-cyan-500 rounded-full mix-blend-multiply filter blur-3xl animate-pulse"></div>
          <div className="absolute bottom-1/4 left-1/4 w-96 h-96 bg-purple-500 rounded-full mix-blend-multiply filter blur-3xl animate-pulse" style={{ animationDelay: '1s' }}></div>
        </div>

        <div className="max-w-3xl mx-auto relative z-10">
          <h1 className="text-40 font-bold mb-3">
            <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
              Tonight's Path
            </span>
          </h1>
          <p className="text-16 text-muted-foreground mb-12">
            Tell us your mood and time. We'll curate a path that blends enjoyment with growth.
          </p>

          {error && (
            <p className="text-14 text-red-400 mb-6">{error}</p>
          )}

          {/* Mood Selector */}
          <div className="mb-10">
            <p className="text-14 text-cyan-400 font-bold uppercase tracking-wider mb-4">
              Step 1 — How are you feeling right now?
            </p>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              {moods.map((m) => (
                <button
                  key={m.name}
                  onClick={() => setMood(m.name)}
                  className={`p-4 rounded-2xl text-14 font-bold transition-all duration-300 capitalize ${
                    mood === m.name
                      ? `bg-gradient-to-r ${m.color} text-white shadow-2xl scale-105`
                      : 'glass text-muted-foreground hover:text-foreground hover:scale-102'
                  }`}
                >
                  {m.name}
                </button>
              ))}
            </div>
          </div>

          {/* Time Selector */}
          <div className="mb-12">
            <p className="text-14 text-purple-400 font-bold uppercase tracking-wider mb-4">
              Step 2 — How much time do you have?
            </p>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {times.map((t) => (
                <button
                  key={t.value}
                  onClick={() => setTimeAvailable(t.value)}
                  className={`px-6 py-4 rounded-2xl text-16 font-bold transition-all duration-300 ${
                    timeAvailable === t.value
                      ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-2xl scale-105'
                      : 'glass text-muted-foreground hover:text-foreground hover:scale-102'
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </div>
          </div>

          {/* Submit */}
          <button
            onClick={handleGetPath}
            disabled={!mood || !timeAvailable}
            className={`flex items-center justify-center gap-3 w-full px-10 py-5 rounded-full text-18 font-bold transition-all duration-300 ${
              mood && timeAvailable
                ? 'bg-gradient-to-r from-cyan-600 to-purple-600 text-white hover:from-cyan-500 hover:to-purple-500 shadow-2xl hover:shadow-cyan-500/50 hover:scale-105'
                : 'glass text-muted-foreground cursor-not-allowed'
            }`}
          >
            Get My Path
            <ArrowRight className="w-5 h-5" strokeWidth={2.5} />
          </button>
        </div>
      </div>
    )
  }

  // Loading
  if (loading) {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center px-6">
        <Loader2 className="w-8 h-8 text-purple-500 animate-spin mb-4" />
        <p className="text-14 text-muted-foreground">
          Curating your growth path...
        </p>
      </div>
    )
  }

  // Path items
  return (
    <div className="min-h-screen bg-background px-6 py-12">
      <div className="max-w-3xl mx-auto">
        <div className="mb-10">
          <h1 className="text-40 font-bold mb-3">
            <span className="bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
              Tonight's Path
            </span>
          </h1>
          <p className="text-16 text-muted-foreground">
            {mood} / {timeAvailable}min — Curated for growth & enjoyment
          </p>
        </div>

        <div className="space-y-6">
          {items.map((item, index) => {
            const colors = engagementColors[item.engagement_type] || engagementColors.Absorb
            const itemKey = item.id || item.title || index

            const feedback = feedbackSent[itemKey]

            return (
              <div
                key={itemKey}
                className={`rounded-3xl glass p-6 border-l-4 ${colors.border} ${colors.bg} card-hover`}
              >
                {/* Header */}
                <div className="flex items-start justify-between gap-4 mb-4">
                  <div className="flex-1">
                    <h3 className="text-20 font-bold text-foreground mb-2">
                      {item.title}
                    </h3>
                    {item.creator && (
                      <p className="text-14 text-muted-foreground font-semibold">
                        {item.creator}
                      </p>
                    )}
                  </div>
                  {item.engagement_type && (
                    <span className={`px-4 py-2 text-12 font-bold ${colors.text} rounded-full border ${colors.border} ${colors.bg} shrink-0 uppercase tracking-wider`}>
                      {item.engagement_type}
                    </span>
                  )}
                </div>

                {/* Tags */}
                <div className="flex flex-wrap gap-2 mb-4">
                  {item.domain && (
                    <span className="px-3 py-1 text-12 font-semibold text-foreground rounded-full glass">
                      {item.domain}
                    </span>
                  )}
                  {item.time_minutes && (
                    <span className="flex items-center gap-1 px-3 py-1 text-12 font-semibold text-foreground rounded-full glass">
                      <Clock className="w-3 h-3" strokeWidth={2} />
                      {item.time_minutes}min
                    </span>
                  )}
                </div>

                {/* Reasons */}
                {item.why_youll_love_it && (
                  <p className="text-14 text-foreground/90 mb-2 leading-relaxed">
                    <span className="font-bold text-cyan-400">Why you'll love it:</span> {item.why_youll_love_it}
                  </p>
                )}
                {item.why_it_grows_you && (
                  <p className="text-14 text-foreground/90 mb-5 leading-relaxed">
                    <span className="font-bold text-purple-400">Why it grows you:</span> {item.why_it_grows_you}
                  </p>
                )}

                {/* Actions */}
                {!feedback ? (
                  <div className="flex gap-3 pt-4 border-t border-white/10">
                    <button
                      onClick={() => handleFeedback(item, 'done')}
                      className="flex items-center gap-2 px-4 py-2 rounded-full text-13 font-bold bg-green-500/20 text-green-400 border border-green-500/30 hover:bg-green-500/30 transition-all"
                    >
                      <Check className="w-4 h-4" strokeWidth={2} />
                      Done
                    </button>
                    <button
                      onClick={() => handleFeedback(item, 'skip')}
                      className="flex items-center gap-2 px-4 py-2 rounded-full text-13 font-bold glass text-muted-foreground hover:text-foreground transition-all"
                    >
                      <SkipForward className="w-4 h-4" strokeWidth={2} />
                      Skip
                    </button>
                    <button
                      onClick={() => handleFeedback(item, 'save')}
                      className="flex items-center gap-2 px-4 py-2 rounded-full text-13 font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30 hover:bg-amber-500/30 transition-all"
                    >
                      <Bookmark className="w-4 h-4" strokeWidth={2} />
                      Save
                    </button>
                  </div>
                ) : (
                  <div className="pt-4 border-t border-white/10">
                    <span className="text-13 font-semibold text-muted-foreground">
                      {feedback === 'done' && '✓ Marked as done'}
                      {feedback === 'skip' && '⏭ Skipped'}
                      {feedback === 'save' && '🔖 Saved for later'}
                    </span>
                  </div>
                )}
              </div>
            )
          })}
        </div>

        {/* Footer link */}
        <div className="mt-12 text-center">
          <Link
            to={`/analytics/${id}`}
            className="inline-flex items-center gap-2 px-6 py-3 rounded-full text-14 font-bold glass text-foreground hover:bg-white/10 transition-all"
          >
            View Analytics
            <ArrowRight className="w-4 h-4" strokeWidth={2} />
          </Link>
        </div>
      </div>
    </div>
  )
}

export default GrowthPath
