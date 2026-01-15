import { useState } from 'react'
import DrawingCanvas from './components/DrawingCanvas'
import NetworkOptimizer from './components/NetworkOptimizer'
import DataImporter from './components/DataImporter'
import './App.css'

function App() {
  const [status, setStatus] = useState('')
  const [trainingCount, setTrainingCount] = useState(0)
  const [trainingData, setTrainingData] = useState([])
  const [pixelArray, setPixelArray] = useState(Array(784).fill(0))
  const [activeTab, setActiveTab] = useState('draw')

  return (
    <div className="app">
      <div className="container">
        <h1>OCR Neural Network Demo</h1>
        <p className="subtitle">Train and test a neural network for digit recognition</p>
        
        {status && (
          <div className={`status ${status.includes('Error') || status.includes('⚠️') ? 'error' : 'success'}`}>
            {status}
          </div>
        )}

        <div className="info-bar">
          <p>Training samples: <strong>{trainingCount}</strong></p>
          <p className="hint">💡 Train 3-5 examples of each digit (0-9)</p>
        </div>

        <div className="tabs">
          <button 
            className={`tab ${activeTab === 'draw' ? 'active' : ''}`}
            onClick={() => setActiveTab('draw')}
          >
            ✏️ Draw
          </button>
          <button 
            className={`tab ${activeTab === 'generate' ? 'active' : ''}`}
            onClick={() => setActiveTab('generate')}
          >
            🎲 Generate
          </button>
          <button 
            className={`tab ${activeTab === 'optimize' ? 'active' : ''}`}
            onClick={() => setActiveTab('optimize')}
          >
            ⚙️ Optimize
          </button>
        </div>

        <div className="tab-content">
          {activeTab === 'draw' && (
            <DrawingCanvas 
              setStatus={setStatus}
              trainingCount={trainingCount}
              setTrainingCount={setTrainingCount}
              trainingData={trainingData}
              setTrainingData={setTrainingData}
              pixelArray={pixelArray}
              setPixelArray={setPixelArray}
            />
          )}

          {activeTab === 'generate' && (
            <>
              <DrawingCanvas 
                setStatus={setStatus}
                trainingCount={trainingCount}
                setTrainingCount={setTrainingCount}
                trainingData={trainingData}
                setTrainingData={setTrainingData}
                pixelArray={pixelArray}
                setPixelArray={setPixelArray}
                readOnly={true}
              />
              <DataImporter
                setStatus={setStatus}
                trainingCount={trainingCount}
                setTrainingCount={setTrainingCount}
                setTrainingData={setTrainingData}
                setPixelArray={setPixelArray}
              />
            </>
          )}

          {activeTab === 'optimize' && (
            <>
              <DrawingCanvas 
                setStatus={setStatus}
                trainingCount={trainingCount}
                setTrainingCount={setTrainingCount}
                trainingData={trainingData}
                setTrainingData={setTrainingData}
                pixelArray={pixelArray}
                setPixelArray={setPixelArray}
                readOnly={true}
              />
              <NetworkOptimizer 
                trainingData={trainingData}
                setStatus={setStatus}
              />
            </>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
