import { useState } from 'react'

export default function NewListingForm({ onSearch, similarItems, onCreate, creating }) {
  const [query, setQuery] = useState('Nike Air Max 90')
  const [category, setCategory] = useState('Shoes')
  const [templateId, setTemplateId] = useState('')
  const [titleOverride, setTitleOverride] = useState('')
  const [priceOverride, setPriceOverride] = useState('')

  return (
    <section className="card">
      <h2>Create Listing From Similar Item</h2>
      <div className="form-grid">
        <label>
          Similar title
          <input value={query} onChange={(e) => setQuery(e.target.value)} />
        </label>
        <label>
          Category
          <input value={category} onChange={(e) => setCategory(e.target.value)} />
        </label>
      </div>

      <button className="button secondary" onClick={() => onSearch(query, category)}>
        Find Similar Listings
      </button>

      <div className="template-list">
        {similarItems.map((item) => (
          <label key={item.id} className="template-item">
            <input
              type="radio"
              name="template"
              value={item.id}
              checked={templateId === String(item.id)}
              onChange={(e) => {
                setTemplateId(e.target.value)
                setTitleOverride(item.title)
                setPriceOverride(String(item.price))
              }}
            />
            <div>
              <strong>{item.title}</strong>
              <small>
                {item.category} | {item.status} | {item.currency} {item.price.toFixed(2)}
              </small>
            </div>
          </label>
        ))}
        {similarItems.length === 0 ? <p className="empty">No template suggestions yet.</p> : null}
      </div>

      <div className="form-grid">
        <label>
          Listing title
          <input
            value={titleOverride}
            onChange={(e) => setTitleOverride(e.target.value)}
            placeholder="Auto-filled from template"
          />
        </label>
        <label>
          Listing price
          <input
            type="number"
            value={priceOverride}
            onChange={(e) => setPriceOverride(e.target.value)}
            placeholder="Auto-filled from template"
          />
        </label>
      </div>

      <button
        className="button"
        disabled={!templateId || creating}
        onClick={() =>
          onCreate({
            template_item_id: Number(templateId),
            title: titleOverride || undefined,
            price: priceOverride ? Number(priceOverride) : undefined
          })
        }
      >
        {creating ? 'Creating...' : 'Create Listing'}
      </button>
    </section>
  )
}
