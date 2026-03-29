import { useMemo } from 'react'

const statusPillClass = {
  active: 'pill pill-active',
  sold: 'pill pill-sold',
  cancelled: 'pill pill-cancelled'
}

export default function ItemDashboard({ items, statusFilter, setStatusFilter, search, setSearch }) {
  const counts = useMemo(() => {
    return items.reduce(
      (acc, item) => {
        acc.total += 1
        acc[item.status] = (acc[item.status] || 0) + 1
        return acc
      },
      { total: 0, active: 0, sold: 0, cancelled: 0 }
    )
  }, [items])

  return (
    <section className="card">
      <div className="card-header">
        <h2>Item Tracking</h2>
        <div className="stat-grid">
          <div className="stat"><span>Total</span><strong>{counts.total}</strong></div>
          <div className="stat"><span>Active</span><strong>{counts.active}</strong></div>
          <div className="stat"><span>Sold</span><strong>{counts.sold}</strong></div>
          <div className="stat"><span>Cancelled</span><strong>{counts.cancelled}</strong></div>
        </div>
      </div>

      <div className="toolbar">
        <select value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
          <option value="">All statuses</option>
          <option value="active">Active</option>
          <option value="sold">Sold</option>
          <option value="cancelled">Cancelled</option>
        </select>
        <input
          type="text"
          placeholder="Search title..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Title</th>
              <th>Category</th>
              <th>Status</th>
              <th>Price</th>
              <th>Qty</th>
            </tr>
          </thead>
          <tbody>
            {items.length === 0 ? (
              <tr>
                <td colSpan="5" className="empty">No items found for current filters.</td>
              </tr>
            ) : (
              items.map((item) => (
                <tr key={item.id}>
                  <td>{item.title}</td>
                  <td>{item.category}</td>
                  <td>
                    <span className={statusPillClass[item.status] || 'pill'}>{item.status}</span>
                  </td>
                  <td>
                    {item.currency} {item.price.toFixed(2)}
                  </td>
                  <td>{item.quantity}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </section>
  )
}
