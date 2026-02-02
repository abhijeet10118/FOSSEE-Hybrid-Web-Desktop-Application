import React from 'react'

function downloadSummaryFile(summary, name) {
  const safeName = (name || 'summary').replace(/\.[^.]+$/, '').replace(/[^\w.-]/g, '_')
  const blob = new Blob([JSON.stringify({ name, ...summary }, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `summary_${safeName}.json`
  a.click()
  URL.revokeObjectURL(url)
}

export default function Summary({ summary, name }) {
  if (!summary) return null
  const { total_count, averages, type_distribution } = summary
  return (
    <section className="summary-section">
      <div className="summary-section-header">
        <h2>Summary — {name}</h2>
        <button
          type="button"
          className="btn-download-summary"
          onClick={() => downloadSummaryFile(summary, name)}
        >
          Download Summary
        </button>
      </div>
      <div className="summary-grid">
        <div className="summary-card">
          <span className="summary-label">Total equipment</span>
          <span className="summary-value">{total_count ?? 0}</span>
        </div>
        {averages && Object.keys(averages).length > 0 && (
          <div className="summary-card">
            <span className="summary-label">Averages</span>
            <ul className="summary-list">
              {Object.entries(averages).map(([k, v]) => (
                <li key={k}>{k}: {Number(v).toFixed(2)}</li>
              ))}
            </ul>
          </div>
        )}
        {type_distribution && Object.keys(type_distribution).length > 0 && (
          <div className="summary-card">
            <span className="summary-label">By type</span>
            <ul className="summary-list">
              {Object.entries(type_distribution).map(([k, v]) => (
                <li key={k}>{k}: {v}</li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </section>
  )
}
