import React from 'react'

export default function DataTable({ data }) {
  if (!data || data.length === 0) return null

  const columns = Object.keys(data[0])

  return (
    <section className="table-section">
      <h2>Data table</h2>
      <div className="table-wrapper">
        <table className="data-table">
          <thead>
            <tr>
              {columns.map((col) => (
                <th key={col}>{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.map((row, i) => (
              <tr key={i}>
                {columns.map((col) => (
                  <td key={col}>{row[col] ?? ''}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}
