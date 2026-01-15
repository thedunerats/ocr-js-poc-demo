import { useState } from 'react'
import DrawingCanvas from './components/DrawingCanvas'
import NetworkOptimizer from './components/NetworkOptimizer'
import './App.css'

function App() {
  const [status, setStatus] = useState('')
  const [trainingCount, setTrainingCount] = useState(0)
  const [trainingData, setTrainingData] = useState([])

  return (
    <div className="app">
      <div className="container">
        <h1>OCR Neural Network Demo</h1>
        <p className="subtitle">Draw a digit and train or test the neural network</p>
        
        {status && (
          <div className={`status ${status.includes('Error') || status.includes('⚠️') ? 'error' : 'success'}`}>
            {status}
          </div>
        )}
        
        <DrawingCanvas 
          setStatus={setStatus}
          trainingCount={trainingCount}
          setTrainingCount={setTrainingCount}
          trainingData={trainingData}
          setTrainingData={setTrainingData}
        />
        
        <div className="info">
          <p>Training samples collected: <strong>{trainingCount}</strong></p>
          <p className="hint">💡 Tip: Train 3-5 examples of EACH digit (0-9) for accuracy</p>
          <p className="hint">⚡ Use "Train Now" for immediate training, or "Add to Batch" to collect 3 samples</p>
        </div>

        <NetworkOptimizer 
          trainingData={trainingData}
          setStatus={setStatus}
        />
      </div>
    </div>
  )
}

export default App
