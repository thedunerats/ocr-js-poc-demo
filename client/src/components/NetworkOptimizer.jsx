import { useState } from 'react'
import './NetworkOptimizer.css'

const API_URL = '/api/optimize'

function NetworkOptimizer({ trainingData, setStatus }) {
  const [isOptimizing, setIsOptimizing] = useState(false)
  const [results, setResults] = useState(null)
  const [minNodes, setMinNodes] = useState(5)
  const [maxNodes, setMaxNodes] = useState(30)
  const [step, setStep] = useState(5)

  const handleOptimize = async () => {
    if (!trainingData || trainingData.length < 10) {
      setStatus('⚠️ Need at least 10 training samples to optimize (70% train, 30% test split)')
      return
    }

    setIsOptimizing(true)
    setStatus('🔍 Optimizing network configuration...')
    setResults(null)

    try {
      // Split data: 70% training, 30% testing
      const splitIndex = Math.floor(trainingData.length * 0.7)
      const trainingSet = trainingData.slice(0, splitIndex)
      const testSet = trainingData.slice(splitIndex)

      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          trainingData: trainingSet,
          testData: testSet,
          minNodes: parseInt(minNodes),
          maxNodes: parseInt(maxNodes),
          step: parseInt(step)
        })
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || `Server returned status ${response.status}`)
      }

      const data = await response.json()
      setResults(data)
      setStatus(`✅ ${data.message} Best: ${data.optimal.hiddenNodes} nodes with ${(data.optimal.accuracy * 100).toFixed(1)}% accuracy`)
    } catch (error) {
      setStatus(`❌ Optimization error: ${error.message}`)
      console.error('Optimization error:', error)
    } finally {
      setIsOptimizing(false)
    }
  }

  return (
    <div className="network-optimizer">
      <h3>🧠 Network Optimizer</h3>
      <p className="optimizer-description">
        Find the optimal number of hidden nodes for your training data
      </p>

      <div className="optimizer-controls">
        <div className="input-row">
          <div className="input-group-small">
            <label htmlFor="minNodes">Min Nodes:</label>
            <input
              id="minNodes"
              type="number"
              min="1"
              max="100"
              value={minNodes}
              onChange={(e) => setMinNodes(e.target.value)}
              disabled={isOptimizing}
            />
          </div>

          <div className="input-group-small">
            <label htmlFor="maxNodes">Max Nodes:</label>
            <input
              id="maxNodes"
              type="number"
              min="1"
              max="100"
              value={maxNodes}
              onChange={(e) => setMaxNodes(e.target.value)}
              disabled={isOptimizing}
            />
          </div>

          <div className="input-group-small">
            <label htmlFor="step">Step:</label>
            <input
              id="step"
              type="number"
              min="1"
              max="10"
              value={step}
              onChange={(e) => setStep(e.target.value)}
              disabled={isOptimizing}
            />
          </div>
        </div>

        <button 
          onClick={handleOptimize}
          className="btn btn-optimize"
          disabled={isOptimizing || !trainingData || trainingData.length < 10}
        >
          {isOptimizing ? '⏳ Optimizing...' : '🚀 Find Optimal Configuration'}
        </button>

        {trainingData && trainingData.length < 10 && (
          <p className="warning-text">
            Need {10 - trainingData.length} more training samples (currently: {trainingData.length})
          </p>
        )}
      </div>

      {results && (
        <div className="results-section">
          <h4>📊 Optimization Results</h4>
          
          <div className="optimal-result">
            <div className="optimal-badge">⭐ OPTIMAL</div>
            <div className="optimal-details">
              <span className="optimal-nodes">{results.optimal.hiddenNodes} Hidden Nodes</span>
              <span className="optimal-accuracy">{(results.optimal.accuracy * 100).toFixed(2)}% Accuracy</span>
            </div>
          </div>

          <div className="all-results">
            <table>
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Hidden Nodes</th>
                  <th>Accuracy</th>
                </tr>
              </thead>
              <tbody>
                {results.results.map((result, index) => (
                  <tr key={index} className={index === 0 ? 'best-result' : ''}>
                    <td>{index + 1}</td>
                    <td>{result.hiddenNodes}</td>
                    <td>{(result.accuracy * 100).toFixed(2)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}

export default NetworkOptimizer
