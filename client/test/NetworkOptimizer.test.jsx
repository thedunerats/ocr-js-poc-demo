import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import NetworkOptimizer from '../src/components/NetworkOptimizer'

describe('NetworkOptimizer Component', () => {
  let mockSetStatus

  beforeEach(() => {
    mockSetStatus = vi.fn()
    global.fetch = vi.fn()
  })

  it('renders optimizer heading and description', () => {
    render(
      <NetworkOptimizer
        trainingData={[]}
        setStatus={mockSetStatus}
      />
    )

    expect(screen.getByText(/Network Optimizer/i)).toBeInTheDocument()
    expect(screen.getByText(/Find the optimal number of hidden nodes/i)).toBeInTheDocument()
  })

  it('renders input fields with default values', () => {
    render(
      <NetworkOptimizer
        trainingData={[]}
        setStatus={mockSetStatus}
      />
    )

    const minNodesInput = screen.getByLabelText(/Min Nodes/i)
    const maxNodesInput = screen.getByLabelText(/Max Nodes/i)
    const stepInput = screen.getByLabelText(/Step/i)

    expect(minNodesInput).toHaveValue(5)
    expect(maxNodesInput).toHaveValue(30)
    expect(stepInput).toHaveValue(5)
  })

  it('renders optimize button', () => {
    render(
      <NetworkOptimizer
        trainingData={[]}
        setStatus={mockSetStatus}
      />
    )

    expect(screen.getByRole('button', { name: /Find Optimal Configuration/i })).toBeInTheDocument()
  })

  it('disables optimize button when not enough training data', () => {
    render(
      <NetworkOptimizer
        trainingData={[{ y0: Array(784).fill(0.5), label: 1 }]}
        setStatus={mockSetStatus}
      />
    )

    const button = screen.getByRole('button', { name: /Find Optimal Configuration/i })
    expect(button).toBeDisabled()
  })

  it('shows warning when not enough training samples', () => {
    render(
      <NetworkOptimizer
        trainingData={[{ y0: Array(784).fill(0.5), label: 1 }]}
        setStatus={mockSetStatus}
      />
    )

    expect(screen.getByText(/Need 9 more training samples/i)).toBeInTheDocument()
  })

  it('enables optimize button with sufficient training data', () => {
    const trainingData = Array.from({ length: 10 }, (_, i) => ({
      y0: Array(784).fill(0.5),
      label: i % 10
    }))

    render(
      <NetworkOptimizer
        trainingData={trainingData}
        setStatus={mockSetStatus}
      />
    )

    const button = screen.getByRole('button', { name: /Find Optimal Configuration/i })
    expect(button).not.toBeDisabled()
  })

  it('allows user to change min nodes', async () => {
    const user = userEvent.setup()
    render(
      <NetworkOptimizer
        trainingData={[]}
        setStatus={mockSetStatus}
      />
    )

    const minNodesInput = screen.getByLabelText(/Min Nodes/i)
    await user.clear(minNodesInput)
    await user.type(minNodesInput, '10')

    expect(minNodesInput).toHaveValue(10)
  })

  it('allows user to change max nodes', async () => {
    const user = userEvent.setup()
    render(
      <NetworkOptimizer
        trainingData={[]}
        setStatus={mockSetStatus}
      />
    )

    const maxNodesInput = screen.getByLabelText(/Max Nodes/i)
    await user.clear(maxNodesInput)
    await user.type(maxNodesInput, '50')

    expect(maxNodesInput).toHaveValue(50)
  })

  it('allows user to change step', async () => {
    const user = userEvent.setup()
    render(
      <NetworkOptimizer
        trainingData={[]}
        setStatus={mockSetStatus}
      />
    )

    const stepInput = screen.getByLabelText(/Step/i)
    await user.clear(stepInput)
    await user.type(stepInput, '3')

    expect(stepInput).toHaveValue(3)
  })

  it('button is disabled when not enough data', () => {
    const trainingData = Array.from({ length: 5 }, (_, i) => ({
      y0: Array(784).fill(0.5),
      label: i
    }))

    render(
      <NetworkOptimizer
        trainingData={trainingData}
        setStatus={mockSetStatus}
      />
    )

    const button = screen.getByRole('button', { name: /Find Optimal Configuration/i })
    expect(button).toBeDisabled()
  })

  it('sends optimization request with correct data', async () => {
    const user = userEvent.setup()
    const trainingData = Array.from({ length: 20 }, (_, i) => ({
      y0: Array(784).fill(0.5),
      label: i % 10
    }))

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        results: [
          { hiddenNodes: 20, accuracy: 0.95 },
          { hiddenNodes: 15, accuracy: 0.93 }
        ],
        optimal: { hiddenNodes: 20, accuracy: 0.95 },
        message: 'Optimization completed. Tested 2 configurations.'
      })
    })

    render(
      <NetworkOptimizer
        trainingData={trainingData}
        setStatus={mockSetStatus}
      />
    )

    const button = screen.getByRole('button', { name: /Find Optimal Configuration/i })
    await user.click(button)

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        '/api/optimize',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        })
      )
    })

    // Check that data was split correctly
    const callArgs = global.fetch.mock.calls[0][1]
    const requestBody = JSON.parse(callArgs.body)
    expect(requestBody.trainingData).toHaveLength(14) // 70% of 20
    expect(requestBody.testData).toHaveLength(6) // 30% of 20
  })

  it('displays optimization results after successful request', async () => {
    const user = userEvent.setup()
    const trainingData = Array.from({ length: 20 }, (_, i) => ({
      y0: Array(784).fill(0.5),
      label: i % 10
    }))

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        results: [
          { hiddenNodes: 20, accuracy: 0.95 },
          { hiddenNodes: 15, accuracy: 0.93 }
        ],
        optimal: { hiddenNodes: 20, accuracy: 0.95 },
        message: 'Optimization completed. Tested 2 configurations.'
      })
    })

    render(
      <NetworkOptimizer
        trainingData={trainingData}
        setStatus={mockSetStatus}
      />
    )

    const button = screen.getByRole('button', { name: /Find Optimal Configuration/i })
    await user.click(button)

    await waitFor(() => {
      expect(screen.getByText(/Optimization Results/i)).toBeInTheDocument()
    })

    expect(screen.getByText(/20 Hidden Nodes/i)).toBeInTheDocument()
    expect(screen.getByText(/95.00% Accuracy/i)).toBeInTheDocument()
  })

  it('shows optimizing state while request is in progress', async () => {
    const user = userEvent.setup()
    const trainingData = Array.from({ length: 20 }, (_, i) => ({
      y0: Array(784).fill(0.5),
      label: i % 10
    }))

    global.fetch.mockImplementation(() => 
      new Promise(resolve => setTimeout(resolve, 1000))
    )

    render(
      <NetworkOptimizer
        trainingData={trainingData}
        setStatus={mockSetStatus}
      />
    )

    const button = screen.getByRole('button', { name: /Find Optimal Configuration/i })
    await user.click(button)

    expect(screen.getByRole('button', { name: /Optimizing/i })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Optimizing/i })).toBeDisabled()
  })

  it('disables inputs while optimizing', async () => {
    const user = userEvent.setup()
    const trainingData = Array.from({ length: 20 }, (_, i) => ({
      y0: Array(784).fill(0.5),
      label: i % 10
    }))

    global.fetch.mockImplementation(() => 
      new Promise(resolve => setTimeout(resolve, 1000))
    )

    render(
      <NetworkOptimizer
        trainingData={trainingData}
        setStatus={mockSetStatus}
      />
    )

    const button = screen.getByRole('button', { name: /Find Optimal Configuration/i })
    await user.click(button)

    const minNodesInput = screen.getByLabelText(/Min Nodes/i)
    const maxNodesInput = screen.getByLabelText(/Max Nodes/i)
    const stepInput = screen.getByLabelText(/Step/i)

    expect(minNodesInput).toBeDisabled()
    expect(maxNodesInput).toBeDisabled()
    expect(stepInput).toBeDisabled()
  })

  it('handles optimization error', async () => {
    const user = userEvent.setup()
    const trainingData = Array.from({ length: 20 }, (_, i) => ({
      y0: Array(784).fill(0.5),
      label: i % 10
    }))

    global.fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ error: 'Server error' })
    })

    render(
      <NetworkOptimizer
        trainingData={trainingData}
        setStatus={mockSetStatus}
      />
    )

    const button = screen.getByRole('button', { name: /Find Optimal Configuration/i })
    await user.click(button)

    await waitFor(() => {
      expect(mockSetStatus).toHaveBeenCalledWith(
        expect.stringContaining('Optimization error')
      )
    })
  })

  it('handles network failure', async () => {
    const user = userEvent.setup()
    const trainingData = Array.from({ length: 20 }, (_, i) => ({
      y0: Array(784).fill(0.5),
      label: i % 10
    }))

    global.fetch.mockRejectedValueOnce(new Error('Network error'))

    render(
      <NetworkOptimizer
        trainingData={trainingData}
        setStatus={mockSetStatus}
      />
    )

    const button = screen.getByRole('button', { name: /Find Optimal Configuration/i })
    await user.click(button)

    await waitFor(() => {
      expect(mockSetStatus).toHaveBeenCalledWith(
        expect.stringContaining('Network error')
      )
    })
  })

  it('displays results table with all configurations', async () => {
    const user = userEvent.setup()
    const trainingData = Array.from({ length: 20 }, (_, i) => ({
      y0: Array(784).fill(0.5),
      label: i % 10
    }))

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        results: [
          { hiddenNodes: 20, accuracy: 0.95 },
          { hiddenNodes: 15, accuracy: 0.93 },
          { hiddenNodes: 25, accuracy: 0.90 }
        ],
        optimal: { hiddenNodes: 20, accuracy: 0.95 },
        message: 'Optimization completed. Tested 3 configurations.'
      })
    })

    render(
      <NetworkOptimizer
        trainingData={trainingData}
        setStatus={mockSetStatus}
      />
    )

    const button = screen.getByRole('button', { name: /Find Optimal Configuration/i })
    await user.click(button)

    await waitFor(() => {
      expect(screen.getByText('20')).toBeInTheDocument()
      expect(screen.getByText('15')).toBeInTheDocument()
      expect(screen.getByText('25')).toBeInTheDocument()
    })
  })

  it('updates status with optimization results', async () => {
    const user = userEvent.setup()
    const trainingData = Array.from({ length: 20 }, (_, i) => ({
      y0: Array(784).fill(0.5),
      label: i % 10
    }))

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        results: [
          { hiddenNodes: 20, accuracy: 0.95 }
        ],
        optimal: { hiddenNodes: 20, accuracy: 0.95 },
        message: 'Optimization completed. Tested 1 configurations.'
      })
    })

    render(
      <NetworkOptimizer
        trainingData={trainingData}
        setStatus={mockSetStatus}
      />
    )

    const button = screen.getByRole('button', { name: /Find Optimal Configuration/i })
    await user.click(button)

    await waitFor(() => {
      expect(mockSetStatus).toHaveBeenCalledWith(
        expect.stringContaining('Best: 20 nodes with 95.0% accuracy')
      )
    })
  })
})
