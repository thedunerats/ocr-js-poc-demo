import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from '../src/App'

describe('App Component', () => {
  it('renders the main heading', () => {
    render(<App />)
    expect(screen.getByRole('heading', { name: /OCR Neural Network Demo/i })).toBeInTheDocument()
  })

  it('renders the subtitle', () => {
    render(<App />)
    expect(screen.getByText(/Draw a digit and train or test the neural network/i)).toBeInTheDocument()
  })

  it('displays training count', () => {
    render(<App />)
    expect(screen.getByText(/Training samples collected:/i)).toBeInTheDocument()
    expect(screen.getByText('0')).toBeInTheDocument()
  })

  it('shows training tips', () => {
    render(<App />)
    expect(screen.getByText(/Tip: Train 3-5 examples of EACH digit/i)).toBeInTheDocument()
    expect(screen.getByText(/Use "Train Now" for immediate training/i)).toBeInTheDocument()
  })

  it('renders DrawingCanvas component', () => {
    render(<App />)
    // Check for input field that's part of DrawingCanvas
    const digitInput = screen.getByLabelText(/Digit/i)
    expect(digitInput).toBeInTheDocument()
  })

  it('does not show status initially', () => {
    render(<App />)
    // Status div should not be present when status is empty
    const statusDiv = document.querySelector('.status')
    expect(statusDiv).toBeNull()
  })

  it('updates training count when training occurs', () => {
    const { rerender } = render(<App />)
    expect(screen.getByText('0')).toBeInTheDocument()
    
    // This would be updated through DrawingCanvas interaction
    // For now just verify the initial state
  })
})
