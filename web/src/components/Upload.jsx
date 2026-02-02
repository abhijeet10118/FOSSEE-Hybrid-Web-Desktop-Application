import React, { useRef, useState } from 'react'

export default function Upload({ onUpload, loading }) {
  const inputRef = useRef(null)
  const [drag, setDrag] = useState(false)

  const handleFile = (file) => {
    if (!file || !file.name.toLowerCase().endsWith('.csv')) return
    onUpload(file)
  }

  const handleChange = (e) => {
    const file = e.target.files?.[0]
    handleFile(file)
    e.target.value = ''
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDrag(false)
    handleFile(e.dataTransfer.files?.[0])
  }

  const handleDragOver = (e) => {
    e.preventDefault()
    setDrag(true)
  }

  const handleDragLeave = () => setDrag(false)

  return (
    <section className="upload-section">
      <div
        className={`upload-zone ${drag ? 'upload-zone-drag' : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onClick={() => inputRef.current?.click()}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".csv"
          onChange={handleChange}
          className="upload-input"
        />
        <p className="upload-text">
          {loading ? 'Uploading…' : 'Drop a CSV file here or click to browse'}
        </p>
        <p className="upload-hint">Equipment Name, Type, Flowrate, Pressure, Temperature</p>
      </div>
    </section>
  )
}
