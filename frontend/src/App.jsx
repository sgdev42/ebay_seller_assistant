import { useCallback, useEffect, useMemo, useState } from 'react'

import { api } from './api/client'
import EbayAuthForm from './components/EbayAuthForm'
import ItemDashboard from './components/ItemDashboard'
import NewListingForm from './components/NewListingForm'

export default function App() {
  const [items, setItems] = useState([])
  const [statusFilter, setStatusFilter] = useState('')
  const [search, setSearch] = useState('')
  const [similarItems, setSimilarItems] = useState([])
  const [loading, setLoading] = useState(false)
  const [creating, setCreating] = useState(false)
  const [suggesting, setSuggesting] = useState(false)
  const [savingAuth, setSavingAuth] = useState(false)
  const [suggestedPricing, setSuggestedPricing] = useState(null)
  const [message, setMessage] = useState('')

  const debouncedSearch = useMemo(() => search.trim(), [search])

  const loadItems = useCallback(async () => {
    setLoading(true)
    try {
      const data = await api.listItems({ status: statusFilter, search: debouncedSearch })
      setItems(data)
    } catch (error) {
      setMessage(`Error loading items: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }, [statusFilter, debouncedSearch])

  async function syncItems() {
    setMessage('Syncing items from eBay...')
    try {
      const result = await api.syncItems()
      setMessage(`Sync completed. Created: ${result.created}, Updated: ${result.updated}.`)
      await loadItems()
    } catch (error) {
      setMessage(`Sync failed: ${error.message}`)
    }
  }

  async function searchSimilar(title, category) {
    if (!title || title.length < 3) {
      setMessage('Please enter at least 3 characters for similarity search.')
      return
    }

    try {
      const data = await api.similarItems({ title, category })
      setSimilarItems(data)
      setMessage(`Found ${data.length} similar item(s).`)
    } catch (error) {
      setMessage(`Similarity search failed: ${error.message}`)
    }
  }

  async function createFromTemplate(payload) {
    setCreating(true)
    try {
      const created = await api.createFromTemplate(payload)
      setMessage(`Listing created: ${created.ebay_item_id} (${created.title})`)
      await loadItems()
    } catch (error) {
      setMessage(`Create listing failed: ${error.message}`)
    } finally {
      setCreating(false)
    }
  }

  async function suggestPrice(payload) {
    setSuggesting(true)
    try {
      const suggestion = await api.suggestPrice(payload)
      setSuggestedPricing(suggestion)
      setMessage(
        `Suggested ${suggestion.currency} ${suggestion.suggested_price.toFixed(2)} from ${suggestion.sample_size} comparable items.`
      )
    } catch (error) {
      setMessage(`Pricing suggestion failed: ${error.message}`)
      setSuggestedPricing(null)
    } finally {
      setSuggesting(false)
    }
  }

  async function loadAuthConfig() {
    try {
      return await api.getEbayAuthConfig()
    } catch (error) {
      setMessage(`Failed to load eBay connection config: ${error.message}`)
      return null
    }
  }

  async function saveAuthConfig(payload) {
    setSavingAuth(true)
    try {
      const data = await api.updateEbayAuthConfig(payload)
      const mode = data.use_mock ? 'mock mode enabled' : 'real mode enabled'
      setMessage(`eBay connection saved (${mode}).`)
    } catch (error) {
      setMessage(`Failed to save eBay connection config: ${error.message}`)
    } finally {
      setSavingAuth(false)
    }
  }

  useEffect(() => {
    loadItems()
  }, [loadItems])

  return (
    <main className="app-shell">
      <header className="hero">
        <h1>eBay Seller Assistant</h1>
        <p>Track items and create new listings from proven templates.</p>
        <button className="button" onClick={syncItems} disabled={loading}>
          {loading ? 'Loading...' : 'Sync Items'}
        </button>
        {message ? <p className="message">{message}</p> : null}
      </header>

      <ItemDashboard
        items={items}
        statusFilter={statusFilter}
        setStatusFilter={setStatusFilter}
        search={search}
        setSearch={setSearch}
      />

      <EbayAuthForm onLoad={loadAuthConfig} onSave={saveAuthConfig} saving={savingAuth} />

      <NewListingForm
        onSearch={searchSimilar}
        similarItems={similarItems}
        onCreate={createFromTemplate}
        onSuggestPrice={suggestPrice}
        suggestedPricing={suggestedPricing}
        suggesting={suggesting}
        creating={creating}
      />
    </main>
  )
}
