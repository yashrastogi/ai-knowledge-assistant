import { useState } from 'react'
import './App.css'

function App() {
  const [status, setStatus] = useState<string>('Not connected')

  const checkStatus = async () => {
    try {
      const response = await fetch('/api/health')
      const data = await response.json()
      setStatus(data.status || 'Unknown')
    } catch (error) {
      setStatus('Error connecting to backend')
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Knowledge Assistant</h1>
        <p>RAG-powered Q&A with Multi-Agent Workflow</p>
        <div>
          <button onClick={checkStatus}>Check Backend Status</button>
          <p>Backend Status: {status}</p>
        </div>
      </header>
    </div>
  )
}

export default App
