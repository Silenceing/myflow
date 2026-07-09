import { useState, useRef } from 'react'
import ReactMarkdown from 'react-markdown'

function App() {
  const [topic, setTopic] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('cn')
  const [elapsed, setElapsed] = useState(0)
  const timerRef = useRef(null)

  const startTimer = () => {
    setElapsed(0)
    timerRef.current = setInterval(() => {
      setElapsed((prev) => prev + 1)
    }, 1000)
  }

  const stopTimer = () => {
    if (timerRef.current) {
      clearInterval(timerRef.current)
      timerRef.current = null
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!topic.trim()) return

    setLoading(true)
    setError(null)
    setResult(null)
    startTimer()

    try {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 300000)

      const response = await fetch('/api/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic: topic.trim() }),
        signal: controller.signal,
      })

      clearTimeout(timeoutId)

      const text = await response.text()

      if (!text || text.trim() === '') {
        throw new Error('Server returned empty response. The request may have timed out.')
      }

      let data
      try {
        data = JSON.parse(text)
      } catch {
        throw new Error('Invalid response from server: ' + text.substring(0, 200))
      }

      if (data.success) {
        setResult(data)
      } else {
        setError(data.error || 'Research failed')
      }
    } catch (err) {
      if (err.name === 'AbortError') {
        setError('Request timed out after 5 minutes. The research task may be too complex.')
      } else {
        setError(err.message || 'Network error')
      }
    } finally {
      stopTimer()
      setLoading(false)
    }
  }

  const formatTime = (s) => {
    const m = Math.floor(s / 60)
    const sec = s % 60
    return `${m}:${sec.toString().padStart(2, '0')}`
  }

  return (
    <div className="app">
      <header className="header">
        <h1>MyFlow</h1>
        <p className="subtitle">AI Research Agent powered by CrewAI</p>
      </header>

      <main className="main">
        <form onSubmit={handleSubmit} className="search-form">
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            placeholder="Enter a research topic (e.g., AI Agents, Quantum Computing)"
            className="search-input"
            disabled={loading}
          />
          <button type="submit" className="search-button" disabled={loading || !topic.trim()}>
            {loading ? (
              <span className="loading-text">
                <span className="spinner"></span>
                Researching... {formatTime(elapsed)}
              </span>
            ) : (
              'Start Research'
            )}
          </button>
        </form>

        {loading && (
          <div className="progress-box">
            <div className="progress-bar">
              <div className="progress-bar-inner"></div>
            </div>
            <p className="progress-text">
              Agent is researching "{topic}"... This may take 1-2 minutes.
            </p>
          </div>
        )}

        {error && (
          <div className="error-box">
            <strong>Error:</strong> {error}
          </div>
        )}

        {result && (
          <div className="result-section">
            <div className="result-header">
              <h2>Research Report: {result.topic}</h2>
              <div className="tabs">
                <button
                  className={`tab ${activeTab === 'cn' ? 'active' : ''}`}
                  onClick={() => setActiveTab('cn')}
                >
                  中文
                </button>
                <button
                  className={`tab ${activeTab === 'en' ? 'active' : ''}`}
                  onClick={() => setActiveTab('en')}
                >
                  English
                </button>
              </div>
            </div>
            <div className="report-content">
              <ReactMarkdown>
                {activeTab === 'cn' ? result.report_cn : result.report_en}
              </ReactMarkdown>
            </div>
          </div>
        )}

        {!result && !loading && !error && (
          <div className="placeholder">
            <div className="placeholder-icon">🔍</div>
            <p>Enter a topic above and click "Start Research" to generate a report</p>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>Powered by <a href="https://crewai.com" target="_blank" rel="noopener noreferrer">CrewAI</a> | Deploy on <a href="https://pages.edgeone.ai" target="_blank" rel="noopener noreferrer">EdgeOne Makers</a></p>
      </footer>
    </div>
  )
}

export default App
