import React, { useState, useEffect, useCallback } from 'react'
import { getHistory, getDataset, uploadCSV, downloadPDF, logout } from '../api'
import Upload from './Upload'
import DataTable from './DataTable'
import Charts from './Charts'
import History from './History'
import Summary from './Summary'
import './Dashboard.css'
import './Upload.css'
import './Summary.css'
import './Charts.css'
import './DataTable.css'
import './History.css'

export default function Dashboard({ onLogout }) {
  const [history, setHistory] = useState([])
  const [current, setCurrent] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const loadHistory = useCallback(async () => {
    try {
      const list = await getHistory()
      setHistory(list)
    } catch (e) {
      setError(e.message)
    }
  }, [])

  useEffect(() => {
    loadHistory()
  }, [loadHistory])

  const handleUpload = async (file) => {
    setError('')
    setLoading(true)
    try {
      const dataset = await uploadCSV(file)
      setCurrent(dataset)
      await loadHistory()
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSelectDataset = async (id) => {
    setError('')
    setLoading(true)
    try {
      const dataset = await getDataset(id)
      setCurrent(dataset)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleDownloadPDF = (id, name) => {
    downloadPDF(id, name ? `report_${name}` : undefined)
  }

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>Chemical Equipment Parameter Visualizer</h1>
        <button type="button" className="btn-logout" onClick={onLogout}>
          Log out
        </button>
      </header>
      <Upload onUpload={handleUpload} loading={loading} />
      {error && <p className="dashboard-error">{error}</p>}
      <History
        items={history}
        currentId={current?.id}
        onSelect={handleSelectDataset}
        onDownloadPDF={handleDownloadPDF}
      />
      {current && (
        <>
          <Summary summary={current.summary} name={current.name} />
          <Charts summary={current.summary} rawData={current.raw_data} />
          <DataTable data={current.raw_data} />
        </>
      )}
    </div>
  )
}
