import React from 'react'

export default function History({ items, currentId, onSelect, onDownloadPDF }) {
  if (!items || items.length === 0) return null

  return (
    <section className="history-section">
      <h2>Last 5 uploads</h2>
      <ul className="history-list">
        {items.map((item) => (
          <li key={item.id} className={currentId === item.id ? 'history-item active' : 'history-item'}>
            <button
              type="button"
              className="history-btn"
              onClick={() => onSelect(item.id)}
            >
              {item.name} — {item.row_count} rows
            </button>
            <button
              type="button"
              className="history-pdf"
              onClick={() => onDownloadPDF(item.id, item.name)}
              title="Download PDF report"
            >
              PDF
            </button>
          </li>
        ))}
      </ul>
    </section>
  )
}
