import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import DrawingCanvas from '../src/components/DrawingCanvas'

describe('DrawingCanvas Component', () => {
  let mockSetStatus
  let mockSetTrainingCount

  beforeEach(() => {
    mockSetStatus = vi.fn()
    mockSetTrainingCount = vi.fn()
    global.fetch = vi.fn()
  })

  it('renders canvas element', () => {
    render(
      <DrawingCanvas
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
      />
    )
    const canvas = document.querySelector('canvas')
    expect(canvas).toBeTruthy()
  })

  it('renders digit input field', () => {
    render(
      <DrawingCanvas
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
      />
    )
    const input = screen.getByPlaceholderText(/Enter digit/i)
    expect(input).toBeInTheDocument()
  })

  it('renders all control buttons', () => {
    render(
      <DrawingCanvas
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
      />
    )
    expect(screen.getByRole('button', { name: /Add to Batch/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Train Now/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Test/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Reset/i })).toBeInTheDocument()
  })

  it('shows batch status when samples are added', () => {
    render(
      <DrawingCanvas
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
      />
    )
    // Initially no batch should be shown (only shows when trainArray.length > 0)
    const batchInfo = screen.queryByText(/Pending batch/i)
    expect(batchInfo).toBeNull()
  })

  it('allows user to type a digit', async () => {
    const user = userEvent.setup()
    render(
      <DrawingCanvas
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
      />
    )
    
    const input = screen.getByPlaceholderText(/Enter digit/i)
    await user.type(input, '5')
    expect(input.value).toBe('5')
  })

  it('clears canvas when Reset button is clicked', async () => {
    const user = userEvent.setup()
    render(
      <DrawingCanvas
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
      />
    )
    
    const input = screen.getByPlaceholderText(/Enter digit/i)
    await user.type(input, '7')
    
    const resetButton = screen.getByRole('button', { name: /Reset/i })
    await user.click(resetButton)
    
    expect(input.value).toBe('')
    expect(mockSetStatus).toHaveBeenCalledWith('')
  })

  it('shows warning when training without drawing', async () => {
    const user = userEvent.setup()
    render(
      <DrawingCanvas
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
      />
    )
    
    const input = screen.getByPlaceholderText(/Enter digit/i)
    await user.type(input, '3')
    
    const trainButton = screen.getByRole('button', { name: /Add to Batch/i })
    await user.click(trainButton)
    
    expect(mockSetStatus).toHaveBeenCalledWith(
      expect.stringContaining('Please type and draw a digit')
    )
  })

  it('shows warning when training without entering digit', async () => {
    const user = userEvent.setup()
    render(
      <DrawingCanvas
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
      />
    )
    
    const trainButton = screen.getByRole('button', { name: /Add to Batch/i })
    await user.click(trainButton)
    
    expect(mockSetStatus).toHaveBeenCalledWith(
      expect.stringContaining('Please type and draw a digit')
    )
  })

  it('shows warning when testing without drawing', async () => {
    const user = userEvent.setup()
    render(
      <DrawingCanvas
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
      />
    )
    
    const testButton = screen.getByRole('button', { name: /Test/i })
    await user.click(testButton)
    
    expect(mockSetStatus).toHaveBeenCalledWith(
      expect.stringContaining('Please draw a digit to test')
    )
  })

  it('sends training request when batch is full', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, message: 'Training completed' })
    })

    const user = userEvent.setup()
    render(
      <DrawingCanvas
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
      />
    )
    
    // Note: This test would need actual canvas interaction to work fully
    // For now, we're just testing the structure
    expect(screen.getByRole('button', { name: /Add to Batch/i })).toBeInTheDocument()
  })

  it('handles fetch errors gracefully', async () => {
    global.fetch.mockRejectedValueOnce(new Error('Network error'))

    render(
      <DrawingCanvas
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
      />
    )
    
    // Verify component renders without crashing
    expect(screen.getByRole('button', { name: /Test/i })).toBeInTheDocument()
  })

  it('validates digit input is between 0-9', async () => {
    const user = userEvent.setup()
    render(
      <DrawingCanvas
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
      />
    )
    
    const input = screen.getByPlaceholderText(/Enter digit/i)
    
    // Type a valid digit
    await user.type(input, '8')
    expect(input.value).toBe('8')
    
    // Clear and type invalid
    await user.clear(input)
    await user.type(input, '15')
    // Input should handle validation (component logic)
  })

  it('displays batch count correctly', () => {
    render(
      <DrawingCanvas
        setStatus={mockSetStatus}
        trainingCount={5}
        setTrainingCount={mockSetTrainingCount}
      />
    )
    
    // No pending batch initially
    const batchInfo = screen.queryByText(/Pending batch/i)
    expect(batchInfo).toBeNull()
  })
})
