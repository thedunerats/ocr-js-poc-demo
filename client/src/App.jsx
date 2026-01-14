import { useState } from 'react'
import DrawingCanvas from './components/DrawingCanvas'
import './App.css'

function App() {
  const [status, setStatus] = useState('')
  const [trainingCount, setTrainingCount] = useState(0)

  return (
    <div className="app">
      <div className="container">
        <h1>OCR Neural Network Demo</h1>
        <p className="subtitle">Draw a digit and train or test the neural network</p>
        
        {status && (
          <div className={`status ${status.includes('Error') ? 'error' : 'success'}`}>
            {status}
          </div>
        )}
        
        <DrawingCanvas 
          setStatus={setStatus}
          trainingCount={trainingCount}
          setTrainingCount={setTrainingCount}
        />
        
        <div className="info">
          <p>Training samples collected: <strong>{trainingCount}</strong></p>
          <p className="hint">💡 Tip: Train multiple variations of each digit for better accuracy</p>
        </div>
      </div>
    </div>
  )
}

export default App
