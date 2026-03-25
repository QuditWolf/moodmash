const BASE = import.meta.env.VITE_API_URL ?? ''

async function request(method, path, body) {
  const opts = { method, headers: { 'Content-Type': 'application/json' } }
  if (body) opts.body = JSON.stringify(body)
  const res = await fetch(`${BASE}${path}`, opts)
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`)
  return res.json()
}

export const api = {
  onboard:        (answers, goal) => request('POST', '/api/onboard', { quiz_answers: answers, goal }),
  getDNA:         (id) => request('GET', `/api/dna/${id}`),
  getPath:        (id, opts) => request('POST', '/api/path', { session_id: id, ...opts }),
  submitFeedback: (pathId, data) => request('POST', `/api/path/${pathId}/feedback`, data),
  getAnalytics:   (id) => request('GET', `/api/analytics/${id}`),
  exportData:     (id) => request('GET', `/api/data/${id}`),
  deleteData:     (id) => request('DELETE', `/api/data/${id}`),
}
