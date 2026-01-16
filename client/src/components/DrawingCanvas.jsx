import { useRef, useEffect, useState } from 'react'
import './DrawingCanvas.css'

const CANVAS_WIDTH = 280
const TRANSLATED_WIDTH = 28
const PIXEL_WIDTH = 10 // TRANSLATED_WIDTH = CANVAS_WIDTH / PIXEL_WIDTH
const BATCH_SIZE = 3 // Reduced for faster training
const TRAIN_URL = '/api/train'
const PREDICT_URL = '/api/predict'

function DrawingCanvas({ setStatus, trainingCount, setTrainingCount, trainingData, setTrainingData, pixelArray, setPixelArray, readOnly = false }) {
  const canvasRef = useRef(null)
  const prevPixelArrayRef = useRef(null)
  const redrawScheduledRef = useRef(false)
  const animationFrameRef = useRef(null)
  const [isDrawing, setIsDrawing] = useState(false)
  const [data, setData] = useState(new Array(784).fill(0))
  const [digit, setDigit] = useState('')
  const [trainArray, setTrainArray] = useState([])

  // Update canvas when pixelArray changes (from generated digit)
  useEffect(() => {
    if (pixelArray && pixelArray.length === 784) {
      // Skip if it's the same array reference (prevents double-renders)
      if (prevPixelArrayRef.current === pixelArray) return
      
      prevPixelArrayRef.current = pixelArray
      
      // Cancel any pending animation frame and reset flag
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
        animationFrameRef.current = null
      }
      
      // Always reset the flag before scheduling
      redrawScheduledRef.current = true
      
      // Use requestAnimationFrame to batch updates
      animationFrameRef.current = requestAnimationFrame(() => {
        setData(pixelArray)
        redrawCanvas(pixelArray)
        redrawScheduledRef.current = false
        animationFrameRef.current = null
      })
    }
    
    // Cleanup on unmount
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
        animationFrameRef.current = null
        redrawScheduledRef.current = false
      }
    }
  }, [pixelArray])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    ctx.fillStyle = '#000000'
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_WIDTH)
    drawGrid(ctx)
  }, [])

  const drawGrid = (ctx) => {
    ctx.strokeStyle = '#555555'
    ctx.lineWidth = 0.5
    
    for (let x = PIXEL_WIDTH; x < CANVAS_WIDTH; x += PIXEL_WIDTH) {
      ctx.beginPath()
      ctx.moveTo(x, 0)
      ctx.lineTo(x, CANVAS_WIDTH)
      ctx.stroke()
    }
    
    for (let y = PIXEL_WIDTH; y < CANVAS_WIDTH; y += PIXEL_WIDTH) {
      ctx.beginPath()
      ctx.moveTo(0, y)
      ctx.lineTo(CANVAS_WIDTH, y)
      ctx.stroke()
    }
  }

  const redrawCanvas = (pixelData) => {
    const canvas = canvasRef.current
    if (!canvas) return
    
    const ctx = canvas.getContext('2d')
    
    // Clear canvas
    ctx.fillStyle = '#000000'
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_WIDTH)
    drawGrid(ctx)
    
    // Draw only non-zero pixels - batch fillStyle for efficiency
    ctx.fillStyle = '#ffffff'
    for (let i = 0; i < pixelData.length; i++) {
      if (pixelData[i] > 0) {
        const y = Math.floor(i / TRANSLATED_WIDTH)
        const x = i % TRANSLATED_WIDTH
        ctx.fillRect(x * PIXEL_WIDTH, y * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH)
      }
    }
  }

  const getCanvasCoordinates = (e) => {
    const canvas = canvasRef.current
    const rect = canvas.getBoundingClientRect()
    return {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    }
  }

  const fillSquare = (x, y) => {
    const ctx = canvasRef.current.getContext('2d')
    const xPixel = Math.floor(x / PIXEL_WIDTH)
    const yPixel = Math.floor(y / PIXEL_WIDTH)
    
    // Use row-major order: index = y * width + x
    const index = yPixel * TRANSLATED_WIDTH + xPixel
    if (index >= 0 && index < 784) {
      const newData = [...data]
      newData[index] = 1
      setData(newData)

      ctx.fillStyle = '#ffffff'
      ctx.fillRect(xPixel * PIXEL_WIDTH, yPixel * PIXEL_WIDTH, PIXEL_WIDTH, PIXEL_WIDTH)
    }
  }

  const handleMouseDown = (e) => {
    if (readOnly) return
    setIsDrawing(true)
    const { x, y } = getCanvasCoordinates(e)
    fillSquare(x, y)
  }

  const handleMouseMove = (e) => {
    if (!isDrawing || readOnly) return
    const { x, y } = getCanvasCoordinates(e)
    fillSquare(x, y)
  }

  const handleMouseUp = () => {
    setIsDrawing(false)
  }

  const resetCanvas = () => {
    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    ctx.fillStyle = '#000000'
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_WIDTH)
    drawGrid(ctx)
    setData(new Array(784).fill(0))
    setDigit('')
    setStatus('')
  }

  const sendData = async (url, json) => {
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(json)
      })

      if (!response.ok) {
        throw new Error(`Server returned status ${response.status}`)
      }

      const responseData = await response.json()
      return responseData
    } catch (error) {
      console.error('Error:', error)
      throw error
    }
  }

  const handleTrain = async (forceTrain = false) => {
    if (!digit || data.indexOf(1) < 0) {
      setStatus('⚠️ Please type and draw a digit to train the network')
      return
    }

    // Create a deep copy of the data array to avoid reference issues
    const newTrainArray = [...trainArray, { y0: [...data], label: parseInt(digit) }]
    setTrainArray(newTrainArray)
    setTrainingCount(trainingCount + 1)
    
    // Store in global training data for optimizer
    if (setTrainingData) {
      setTrainingData(prev => [...prev, { y0: [...data], label: parseInt(digit) }])
    }
    
    // Send immediately if force training or batch is full
    if (forceTrain || newTrainArray.length >= BATCH_SIZE) {
      try {
        setStatus('🚀 Training network...')
        
        // Ensure all data is properly formatted and numeric
        const sanitizedTrainArray = newTrainArray.map((sample, idx) => {
          // Ensure y0 is an array of numbers
          const y0 = sample.y0.map(val => {
            const num = Number(val)
            if (!isFinite(num)) {
              console.error(`Sample ${idx}: Invalid value at pixel:`, val)
              return 0 // Default to 0 for invalid values
            }
            return num
          })
          
          return {
            y0: y0,
            label: parseInt(sample.label)
          }
        })
        
        await sendData(
          TRAIN_URL,
          {
            trainArray: sanitizedTrainArray
          }
        )
        setStatus(`✓ Trained with ${newTrainArray.length} sample${newTrainArray.length > 1 ? 's' : ''}! Total: ${trainingCount + 1}`)
        setTrainArray([])
      } catch (error) {
        setStatus(`❌ Error: ${error.message}`)
        console.error('Training error:', error)
        return
      }
    } else {
      setStatus(`✓ Added digit ${digit} (${newTrainArray.length}/${BATCH_SIZE} in batch)`)
    }
    
    resetCanvas()
  }

  const handleTest = async () => {
    if (data.indexOf(1) < 0) {
      setStatus('⚠️ Please draw a digit to test the network')
      return
    }

    try {
      setStatus('🔍 Testing...')
      const response = await sendData(
        PREDICT_URL,
        {
          image: data
        }
      )
      
      if (response.type === 'test') {
        setStatus(`🎯 The neural network predicts you wrote a '${response.result}'`)
      }
    } catch (error) {
      setStatus(`❌ Error testing: ${error.message}`)
    }
  }

  return (
    <div className="drawing-canvas">
      <h2>{readOnly ? 'Preview Canvas' : 'Drawing Canvas'} (28x28 Grid)</h2>
      <p className="canvas-instruction">
        {readOnly ? 'Generated patterns appear here for review' : 'Draw a digit below'}
      </p>
      
      <canvas
        ref={canvasRef}
        width={CANVAS_WIDTH}
        height={CANVAS_WIDTH}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
      />
      
      <div className="controls">
        <div className="input-group">
          <label htmlFor="digit">Digit (0-9):</label>
          <input
            id="digit"
            type="number"
            min="0"
            max="9"
            value={digit}
            onChange={(e) => setDigit(e.target.value)}
            placeholder="Enter digit"
          />
        </div>
        
        <div className="button-group">
          <button onClick={() => handleTrain(false)} className="btn btn-primary">
            🎓 Add to Batch
          </button>
          <button 
            onClick={() => handleTrain(true)} 
            className="btn btn-primary-alt"
            disabled={trainArray.length === 0 && data.indexOf(1) < 0}
          >
            ⚡ Train Now
          </button>
          <button onClick={handleTest} className="btn btn-success">
            🧪 Test
          </button>
          <button onClick={resetCanvas} className="btn btn-secondary">
            🔄 Reset
          </button>
        </div>
        
        {trainArray.length > 0 && (
          <div className="batch-info">
            📦 Pending batch: {trainArray.length} sample{trainArray.length > 1 ? 's' : ''}
            <button onClick={() => handleTrain(true)} className="btn-link">
              Send now
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default DrawingCanvas
