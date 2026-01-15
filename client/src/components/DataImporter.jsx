import { useState, useRef } from 'react'
import './DataImporter.css'
import { generateDigitPattern } from '../utils/digitPatternGenerator'

const API_URL = '/api'

function DataImporter({ setStatus, trainingCount, setTrainingCount, setTrainingData, setPixelArray }) {
  const [isImporting, setIsImporting] = useState(false)
  const [generatedDigit, setGeneratedDigit] = useState(null)
  const [isGenerating, setIsGenerating] = useState(false)
  const generatingRef = useRef(false)

  const handleFileUpload = async (event) => {
    const file = event.target.files[0]
    if (!file) return

    // Validate file type
    if (!file.name.endsWith('.json')) {
      setStatus('❌ Please upload a JSON file')
      return
    }

    setIsImporting(true)
    setStatus('📂 Reading file...')

    try {
      const fileContent = await file.text()
      const data = JSON.parse(fileContent)

      // Validate data structure
      if (!Array.isArray(data)) {
        throw new Error('File must contain an array of training samples')
      }

      if (data.length === 0) {
        throw new Error('File contains no training samples')
      }

      // Validate each sample
      const validatedData = []
      for (let i = 0; i < data.length; i++) {
        const sample = data[i]
        
        if (!sample.y0 || !Array.isArray(sample.y0)) {
          throw new Error(`Sample ${i}: Missing or invalid 'y0' array`)
        }

        if (sample.y0.length !== 400) {
          throw new Error(`Sample ${i}: Expected 400 pixels, got ${sample.y0.length}`)
        }

        if (typeof sample.label !== 'number' || sample.label < 0 || sample.label > 9) {
          throw new Error(`Sample ${i}: Label must be a number between 0-9, got ${sample.label}`)
        }

        // Sanitize pixel values
        const y0 = sample.y0.map(val => {
          const num = Number(val)
          return isFinite(num) ? Math.max(0, Math.min(1, num)) : 0
        })

        validatedData.push({ y0, label: sample.label })
      }

      setStatus(`✓ Loaded ${validatedData.length} samples, sending to server...`)

      // Send to server for training
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          train: true,
          trainArray: validatedData
        })
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.error || `Server returned status ${response.status}`)
      }

      // Update local state
      setTrainingData(prev => [...prev, ...validatedData])
      setTrainingCount(prev => prev + validatedData.length)
      setStatus(`✅ Successfully imported and trained ${validatedData.length} samples!`)

    } catch (error) {
      setStatus(`❌ Import error: ${error.message}`)
      console.error('Import error:', error)
    } finally {
      setIsImporting(false)
      // Clear the file input
      event.target.value = ''
    }
  }

  const generateSampleFile = () => {
    // Generate a sample JSON file with proper structure
    const sampleData = [
      {
        y0: Array(784).fill(0).map(() => Math.random() > 0.8 ? 1 : 0),
        label: 0
      },
      {
        y0: Array(784).fill(0).map(() => Math.random() > 0.8 ? 1 : 0),
        label: 1
      },
      {
        y0: Array(784).fill(0).map(() => Math.random() > 0.8 ? 1 : 0),
        label: 2
      }
    ]

    const blob = new Blob([JSON.stringify(sampleData, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)

    const link = document.createElement('a')
    link.href = url
    link.download = 'training_data_sample.json'
    link.click()

    URL.revokeObjectURL(url)
    setStatus('📥 Downloaded sample file template')
  }

  const handleGenerateDigit = () => {
    // Robust locking using ref (doesn't cause re-render)
    if (generatingRef.current) return
    
    generatingRef.current = true
    setIsGenerating(true)
    
    // Clear previous pattern to free memory
    setGeneratedDigit(null)
    
    // Generate synchronously (it's fast enough)
    const pattern = generateDigitPattern()
    setGeneratedDigit(pattern)
    
    // Display it on the canvas
    if (setPixelArray) {
      setPixelArray(pattern.y0)
    }
    
    setStatus(`🎲 Generated digit "${pattern.label}" - Review it and click "Train on this" if it looks good!`)
    
    // Reduced cooldown for smoother experience
    setTimeout(() => {
      generatingRef.current = false
      setIsGenerating(false)
    }, 100)
  }

  const handleTrainGenerated = async () => {
    if (!generatedDigit) {
      setStatus('❌ No generated digit to train on')
      return
    }

    setIsImporting(true)
    setStatus('⏳ Training on generated digit...')

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          train: true,
          trainArray: [generatedDigit]
        })
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Server error')
      }

      // Update training data
      setTrainingCount(prevCount => prevCount + 1)
      if (setTrainingData) {
        setTrainingData(prevData => [...prevData, generatedDigit])
      }

      setStatus(`✅ Successfully trained on generated digit "${generatedDigit.label}"!`)
      setGeneratedDigit(null) // Clear after successful training
      
    } catch (error) {
      setStatus(`❌ Training error: ${error.message}`)
    } finally {
      setIsImporting(false)
    }
  }

  return (
    <div className="data-importer">
      <h3>📁 Smart Training Data Generator</h3>
      <p className="importer-description">
        Generate realistic digit patterns or upload your own training data
      </p>

      <div className="generator-section">
        <h4>🎲 Generate & Review</h4>
        <p className="section-note">Generate a random digit, review it on the canvas, then train if it looks good</p>
        <div className="generator-controls">
          <button 
            onClick={handleGenerateDigit}
            className="btn btn-primary"
            disabled={isImporting || isGenerating}
          >
            {isGenerating ? '⏳ Generating...' : '🎲 Generate Random Digit'}
          </button>
          
          {generatedDigit && (
            <button 
              onClick={handleTrainGenerated}
              className="btn btn-success"
              disabled={isImporting}
            >
              ✓ Train on This ({generatedDigit.label})
            </button>
          )}
        </div>
      </div>

      <div className="divider">
        <span>OR</span>
      </div>

      <div className="upload-section">
        <h4>📤 Bulk Upload</h4>
        <p className="section-note">Upload a JSON file with multiple training samples</p>
        <div className="importer-controls">
          <label htmlFor="fileUpload" className={`btn btn-import ${isImporting ? 'disabled' : ''}`}>
            {isImporting ? '⏳ Importing...' : '📤 Upload Training Data'}
            <input
              id="fileUpload"
              type="file"
              accept=".json"
              onChange={handleFileUpload}
              disabled={isImporting}
              style={{ display: 'none' }}
            />
          </label>

          <button
            onClick={generateSampleFile}
            className="btn btn-secondary"
            disabled={isImporting}
          >
            📥 Download Sample Template
          </button>
        </div>
      </div>

      <div className="format-info">
        <details>
          <summary>Expected JSON Format</summary>
          <pre>{`[
  {
    "y0": [/* 784 pixel values (0-1) */],
    "label": 0
  },
  {
    "y0": [/* 784 pixel values (0-1) */],
    "label": 5
  }
]`}</pre>
          <p className="format-note">
            • Each sample needs a <code>y0</code> array with 784 values (28×28 pixels)<br />
            • Pixel values should be between 0 (black) and 1 (white)<br />
            • <code>label</code> must be a digit from 0-9
          </p>
        </details>
      </div>
    </div>
  )
}

export default DataImporter
