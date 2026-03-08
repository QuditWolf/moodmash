import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../../services/api'
import { Loader2, Download, Trash2, AlertTriangle } from 'lucide-react'

const DataPanel = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)
  const [deleting, setDeleting] = useState(false)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const result = await api.exportData(id)
        setData(result)
      } catch (err) {
        setError(err.message || 'Failed to load your data.')
      } finally {
        setLoading(false)
      }
    }
    fetchData()
  }, [id])

  const handleExport = () => {
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: 'application/json',
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `moodmash-data-${id}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  const handleDelete = async () => {
    setDeleting(true)
    try {
      await api.deleteData(id)
      sessionStorage.removeItem('session_id')
      navigate('/')
    } catch (err) {
      setError(err.message || 'Failed to delete data.')
      setDeleting(false)
      setShowDeleteConfirm(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex flex-col items-center justify-center px-6">
        <Loader2 className="w-6 h-6 text-muted-foreground animate-spin mb-4" />
        <p className="text-sm text-muted-foreground font-mono">
          Loading your data...
        </p>
      </div>
    )
  }

  if (error && !data) {
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

  const radarScores = data?.radar_scores || data?.domain_scores || {}
  const archetype = data?.archetype || 'Unknown'

  const weStore = [
    'Anonymized taste vector',
    'Archetype',
    'Goal',
    'Path completions',
  ]

  const weDontStore = [
    'Quiz answers (discarded)',
    'Spotify raw data',
    'Personal info',
    'Browsing history',
  ]

  return (
    <div className="min-h-screen bg-background px-6 py-12">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl sm:text-3xl font-medium tracking-tighter text-foreground mb-2 font-mono">
          Your Data
        </h1>
        <p className="text-sm text-muted-foreground font-mono mb-10">
          Full transparency into what we store.
        </p>

        {error && (
          <p className="text-sm text-red-400 font-mono mb-6">{error}</p>
        )}

        {/* Taste Vector */}
        <div className="border border-white/10 rounded-lg p-6 mb-6">
          <p className="text-xs text-muted-foreground font-mono mb-3 uppercase tracking-wider">
            Your Taste Vector
          </p>
          <p className="text-lg font-medium text-foreground font-mono mb-4">
            {archetype}
          </p>
          {Object.keys(radarScores).length > 0 && (
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
              {Object.entries(radarScores).map(([key, value]) => (
                <div
                  key={key}
                  className="bg-white/5 rounded px-3 py-2 text-center"
                >
                  <p className="text-xs text-muted-foreground font-mono">
                    {key}
                  </p>
                  <p className="text-sm text-foreground font-mono mt-1">
                    {typeof value === 'number' ? value.toFixed(2) : value}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* What We Store vs Don't Store */}
        <div className="border border-white/10 rounded-lg p-6 mb-6">
          <p className="text-xs text-muted-foreground font-mono mb-4 uppercase tracking-wider">
            What We Store vs What We Don't
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <div>
              <p className="text-sm text-foreground font-mono mb-3 font-medium">
                We Store
              </p>
              <ul className="space-y-2">
                {weStore.map((item) => (
                  <li
                    key={item}
                    className="text-sm text-muted-foreground font-mono flex items-start gap-2"
                  >
                    <span className="text-white/40 mt-0.5">*</span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
            <div>
              <p className="text-sm text-foreground font-mono mb-3 font-medium">
                We Don't Store
              </p>
              <ul className="space-y-2">
                {weDontStore.map((item) => (
                  <li
                    key={item}
                    className="text-sm text-muted-foreground font-mono flex items-start gap-2"
                  >
                    <span className="text-white/40 mt-0.5">-</span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-3 mb-6">
          <button
            onClick={handleExport}
            className="flex-1 flex items-center justify-center gap-2 px-6 py-4 rounded-lg text-sm font-medium border border-white/10 text-foreground hover:bg-white/5 transition-all duration-180 ease-out font-mono"
          >
            <Download className="w-4 h-4" strokeWidth={1.5} />
            Export as JSON
          </button>
          <button
            onClick={() => setShowDeleteConfirm(true)}
            className="flex-1 flex items-center justify-center gap-2 px-6 py-4 rounded-lg text-sm font-medium border border-red-500/30 text-red-400 hover:bg-red-500/10 transition-all duration-180 ease-out font-mono"
          >
            <Trash2 className="w-4 h-4" strokeWidth={1.5} />
            Delete All Data
          </button>
        </div>

        {/* Legal Reference */}
        <p className="text-xs text-muted-foreground/60 font-mono text-center">
          Aligned with India's Digital Personal Data Protection Act, 2023
        </p>

        {/* Delete Confirmation Modal */}
        {showDeleteConfirm && (
          <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center px-6">
            <div className="bg-background border border-white/10 rounded-lg p-6 max-w-md w-full">
              <div className="flex items-center gap-3 mb-4">
                <AlertTriangle className="w-5 h-5 text-red-400" strokeWidth={1.5} />
                <h2 className="text-lg font-medium text-foreground font-mono">
                  Delete all data?
                </h2>
              </div>
              <p className="text-sm text-muted-foreground font-mono mb-6">
                This will permanently delete your taste vector, archetype, and
                all path history. This action cannot be undone.
              </p>
              <div className="flex gap-3">
                <button
                  onClick={() => setShowDeleteConfirm(false)}
                  disabled={deleting}
                  className="flex-1 px-4 py-3 rounded-lg text-sm font-medium border border-white/10 text-foreground hover:bg-white/5 transition-colors font-mono"
                >
                  Cancel
                </button>
                <button
                  onClick={handleDelete}
                  disabled={deleting}
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-3 rounded-lg text-sm font-medium bg-red-500/20 border border-red-500/30 text-red-400 hover:bg-red-500/30 transition-colors font-mono"
                >
                  {deleting ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    'Delete Forever'
                  )}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default DataPanel
