import { useEffect, useState } from 'react'

export default function EbayAuthForm({ onLoad, onSave, saving }) {
  const [form, setForm] = useState({
    client_id: '',
    client_secret: '',
    refresh_token: '',
    marketplace_id: 'EBAY_US',
    use_mock: true
  })
  const [loaded, setLoaded] = useState(false)
  const [hasClientSecret, setHasClientSecret] = useState(false)
  const [hasRefreshToken, setHasRefreshToken] = useState(false)

  useEffect(() => {
    async function hydrate() {
      const data = await onLoad()
      if (!data) return
      setForm((prev) => ({
        ...prev,
        client_id: data.client_id || '',
        marketplace_id: data.marketplace_id || 'EBAY_US',
        use_mock: Boolean(data.use_mock)
      }))
      setHasClientSecret(Boolean(data.has_client_secret))
      setHasRefreshToken(Boolean(data.has_refresh_token))
      setLoaded(true)
    }

    hydrate()
  }, [onLoad])

  return (
    <section className="card">
      <h2>eBay Connection</h2>
      <p className="empty">Provide OAuth credentials here instead of editing backend env files.</p>

      <div className="form-grid">
        <label>
          Client ID
          <input
            value={form.client_id}
            onChange={(e) => setForm({ ...form, client_id: e.target.value })}
          />
        </label>
        <label>
          Marketplace ID
          <input
            value={form.marketplace_id}
            onChange={(e) => setForm({ ...form, marketplace_id: e.target.value })}
          />
        </label>
      </div>

      <div className="form-grid">
        <label>
          Client Secret
          <input
            type="password"
            placeholder={hasClientSecret ? 'Stored. Enter to replace.' : ''}
            value={form.client_secret}
            onChange={(e) => setForm({ ...form, client_secret: e.target.value })}
          />
        </label>
        <label>
          Refresh Token
          <input
            type="password"
            placeholder={hasRefreshToken ? 'Stored. Enter to replace.' : ''}
            value={form.refresh_token}
            onChange={(e) => setForm({ ...form, refresh_token: e.target.value })}
          />
        </label>
      </div>

      <label className="checkbox-label">
        <input
          type="checkbox"
          checked={form.use_mock}
          onChange={(e) => setForm({ ...form, use_mock: e.target.checked })}
        />
        Use mock eBay data (disable when real OAuth is ready)
      </label>

      <button
        className="button secondary"
        disabled={saving || !loaded}
        onClick={() => onSave(form)}
      >
        {saving ? 'Saving...' : 'Save eBay Connection'}
      </button>
    </section>
  )
}
