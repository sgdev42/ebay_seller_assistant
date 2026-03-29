async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    },
    ...options
  })

  if (!response.ok) {
    const detail = await response.text()
    throw new Error(detail || `Request failed: ${response.status}`)
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
}

export const api = {
  getEbayAuthConfig: () => request('/api/ebay/auth-config'),
  updateEbayAuthConfig: (payload) =>
    request('/api/ebay/auth-config', {
      method: 'PUT',
      body: JSON.stringify(payload)
    }),
  syncItems: () => request('/api/items/sync', { method: 'POST' }),
  listItems: ({ status, search }) => {
    const params = new URLSearchParams()
    if (status) params.set('status', status)
    if (search) params.set('search', search)
    const qs = params.toString()
    return request(`/api/items${qs ? `?${qs}` : ''}`)
  },
  similarItems: ({ title, category }) => {
    const params = new URLSearchParams()
    params.set('title', title)
    if (category) params.set('category', category)
    return request(`/api/items/similar?${params.toString()}`)
  },
  createFromTemplate: (payload) =>
    request('/api/listings/from-template', {
      method: 'POST',
      body: JSON.stringify(payload)
    })
}
