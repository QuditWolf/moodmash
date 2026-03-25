import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../../services/api'
import { Loader2, ArrowRight } from 'lucide-react'
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  Radar,
  ResponsiveContainer,
} from 'recharts'

const Analytics = () => {
  const { id } = useParams()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const result = await api.getAnalytics(id)
        setData(result)
      } catch (err) {
        setError(err.message || 'Failed to load analytics.')
      } finally {
        setLoading(false)
      }
    }
    fetchAnalytics()
  }, [id])

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center px-6">
        <Loader2 className="w-6 h-6 text-muted-foreground animate-spin mb-4" />
        <p className="text-sm text-muted-foreground font-mono">
          Loading analytics...
        </p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center px-6">
        <p className="text-sm text-red-400 font-mono mb-6">{error}</p>
        <button
          onClick={() => window.location.reload()}
          className="px-6 py-3 rounded-lg text-sm font-medium bg-white text-black hover:bg-white/90 transition-all duration-180 ease-out"
        >
          Retry
        </button>
      </div>
    )
  }

  const domainScores = data.domain_scores || data.radar_scores || {}
  const radarData = Object.entries(domainScores).map(([key, value]) => ({
    axis: key.charAt(0).toUpperCase() + key.slice(1),
    value: value || 0,
  }))

  const goalAlignment = data.goal_alignment_pct || data.goal_alignment_score || 0
  const stats = {
    done: data.items_done || 0,
    skipped: data.items_skipped || 0,
    saved: data.items_saved || 0,
  }
  const domainBreakdown = data.domain_breakdown || {}
  const insight = data.pattern_insight || data.ai_pattern_insight || data.insight || null

  return (
    <div className="min-h-screen bg-background px-6 py-12">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl sm:text-3xl font-medium tracking-tighter text-foreground mb-2 font-mono">
          Analytics
        </h1>
        <p className="text-sm text-muted-foreground font-mono mb-10">
          Your growth patterns and insights.
        </p>

        {/* Radar Chart */}
        {radarData.length > 0 && (
          <div className="border border-white/10 rounded-lg p-6 mb-6">
            <p className="text-xs text-muted-foreground font-mono mb-4 uppercase tracking-wider">
              Domain Scores
            </p>
            <div className="w-full h-72">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData} cx="50%" cy="50%" outerRadius="70%">
                  <PolarGrid stroke="rgba(255,255,255,0.1)" />
                  <PolarAngleAxis
                    dataKey="axis"
                    tick={{ fill: 'rgba(255,255,255,0.5)', fontSize: 12, fontFamily: 'IBM Plex Mono, monospace' }}
                  />
                  <Radar
                    name="Score"
                    dataKey="value"
                    stroke="rgba(255,255,255,0.8)"
                    fill="rgba(255,255,255,0.15)"
                    strokeWidth={1.5}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* Goal Alignment */}
        <div className="border border-white/10 rounded-lg p-6 mb-6">
          <p className="text-xs text-muted-foreground font-mono mb-3 uppercase tracking-wider">
            Goal Alignment
          </p>
          <div className="flex items-end gap-3 mb-3">
            <span className="text-4xl font-medium text-foreground font-mono tracking-tighter">
              {Math.round(goalAlignment)}%
            </span>
          </div>
          <div className="w-full h-2 bg-white/5 rounded-full overflow-hidden">
            <div
              className="h-full bg-white rounded-full transition-all duration-500"
              style={{ width: `${goalAlignment}%` }}
            />
          </div>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-3 gap-3 mb-6">
          {[
            { label: 'Done', value: stats.done },
            { label: 'Skipped', value: stats.skipped },
            { label: 'Saved', value: stats.saved },
          ].map((stat) => (
            <div
              key={stat.label}
              className="border border-white/10 rounded-lg p-4 text-center bg-white/5"
            >
              <p className="text-2xl font-medium text-foreground font-mono">
                {stat.value}
              </p>
              <p className="text-xs text-muted-foreground font-mono mt-1">
                {stat.label}
              </p>
            </div>
          ))}
        </div>

        {/* Domain Breakdown */}
        {Object.keys(domainBreakdown).length > 0 && (
          <div className="border border-white/10 rounded-lg p-6 mb-6">
            <p className="text-xs text-muted-foreground font-mono mb-4 uppercase tracking-wider">
              Domain Breakdown
            </p>
            <div className="space-y-3">
              {Object.entries(domainBreakdown).map(([domain, value]) => {
                const maxValue = Math.max(...Object.values(domainBreakdown), 1)
                const pct = (value / maxValue) * 100
                return (
                  <div key={domain}>
                    <div className="flex justify-between text-xs font-mono text-muted-foreground mb-1">
                      <span>{domain.charAt(0).toUpperCase() + domain.slice(1)}</span>
                      <span>{value}</span>
                    </div>
                    <div className="w-full h-1.5 bg-white/5 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-white/60 rounded-full transition-all duration-500"
                        style={{ width: `${pct}%` }}
                      />
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        )}

        {/* AI Pattern Insight */}
        {insight && (
          <div className="border border-white/10 rounded-lg p-6 mb-6">
            <p className="text-xs text-muted-foreground font-mono mb-3 uppercase tracking-wider">
              AI Pattern Insight
            </p>
            <p className="text-sm text-muted-foreground font-mono italic leading-relaxed">
              {insight}
            </p>
          </div>
        )}

        {/* Footer link */}
        <div className="mt-10 text-center">
          <Link
            to={`/data/${id}`}
            className="inline-flex items-center gap-2 text-sm font-mono text-muted-foreground hover:text-foreground transition-colors"
          >
            View Your Data
            <ArrowRight className="w-4 h-4" strokeWidth={1.5} />
          </Link>
        </div>
      </div>
    </div>
  )
}

export default Analytics
