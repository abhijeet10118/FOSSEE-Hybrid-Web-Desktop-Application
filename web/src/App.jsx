import React, { useState, useEffect } from 'react'
import { login, logout, isAuthenticated } from './api'
import Login from './components/Login'
import Dashboard from './components/Dashboard'
import './App.css'

function App() {
  const [auth, setAuth] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    setAuth(isAuthenticated())
    setLoading(false)
  }, [])

  const handleLogin = async (username, password) => {
    await login(username, password)
    setAuth(true)
  }

  const handleLogout = () => {
    logout()
    setAuth(false)
  }

  if (loading) return <div className="app-loading">Loading…</div>
  if (!auth) return <Login onLogin={handleLogin} />

  return <Dashboard onLogout={handleLogout} />
}

export default App
