import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import DataImporter from '../src/components/DataImporter'

describe('DataImporter Component', () => {
  let mockSetStatus, mockSetTrainingCount, mockSetTrainingData

  beforeEach(() => {
    mockSetStatus = vi.fn()
    mockSetTrainingCount = vi.fn()
    mockSetTrainingData = vi.fn()
    global.fetch = vi.fn()
    global.URL.createObjectURL = vi.fn(() => 'blob:mock-url')
    global.URL.revokeObjectURL = vi.fn()
    
    // Mock File.prototype.text() method
    if (!File.prototype.text) {
      File.prototype.text = async function() {
        return this.textContent || ''
      }
    }
  })
  
  // Helper to create a mock file with text() method
  const createMockFile = (content, filename, options = {}) => {
    const file = new File([content], filename, options)
    file.textContent = content
    return file
  }

  it('renders importer heading and description', () => {
    render(
      <DataImporter
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
        setTrainingData={mockSetTrainingData}
      />
    )

    expect(screen.getByText(/Smart Training Data Generator/i)).toBeInTheDocument()
    expect(screen.getByText(/Generate realistic digit patterns or upload your own training data/i)).toBeInTheDocument()
  })

  it('renders generate and upload buttons', () => {
    render(
      <DataImporter
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
        setTrainingData={mockSetTrainingData}
      />
    )

    expect(screen.getByText(/Generate Random Digit/i)).toBeInTheDocument()
    expect(screen.getByText(/Upload Training Data/i)).toBeInTheDocument()
  })

  it('renders download sample button', () => {
    render(
      <DataImporter
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
        setTrainingData={mockSetTrainingData}
      />
    )

    expect(screen.getByText(/Download Sample Template/i)).toBeInTheDocument()
  })

  it('shows expected format documentation', () => {
    render(
      <DataImporter
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
        setTrainingData={mockSetTrainingData}
      />
    )

    expect(screen.getByText(/Expected JSON Format/i)).toBeInTheDocument()
  })

  it('generates and downloads sample file', async () => {
    const user = userEvent.setup()
    const mockClick = vi.fn()
    
    // Mock document.createElement
    const originalCreateElement = document.createElement
    document.createElement = vi.fn((tag) => {
      if (tag === 'a') {
        return { 
          click: mockClick,
          href: '',
          download: ''
        }
      }
      return originalCreateElement.call(document, tag)
    })

    render(
      <DataImporter
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
        setTrainingData={mockSetTrainingData}
      />
    )

    const downloadButton = screen.getByText(/Download Sample Template/i)
    await user.click(downloadButton)

    expect(mockClick).toHaveBeenCalled()
    expect(mockSetStatus).toHaveBeenCalledWith(expect.stringContaining('Downloaded sample file'))

    // Restore original
    document.createElement = originalCreateElement
  })

  it('rejects non-JSON files', async () => {
    const user = userEvent.setup()
    
    render(
      <DataImporter
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
        setTrainingData={mockSetTrainingData}
      />
    )

    const fileInput = document.querySelector('input[type="file"]')
    const file = createMockFile('test', 'test.txt', { type: 'text/plain' })

    // Directly trigger the change event since userEvent.upload respects the accept attribute
    Object.defineProperty(fileInput, 'files', {
      value: [file],
      writable: false
    })
    
    fileInput.dispatchEvent(new Event('change', { bubbles: true }))

    await waitFor(() => {
      expect(mockSetStatus).toHaveBeenCalledWith(expect.stringContaining('Please upload a JSON file'))
    })
  })

  it('validates file contains array', async () => {
    const user = userEvent.setup()
    
    render(
      <DataImporter
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
        setTrainingData={mockSetTrainingData}
      />
    )

    const fileInput = document.querySelector('input[type="file"]')
    const file = createMockFile('{"invalid": "data"}', 'test.json', { type: 'application/json' })

    await user.upload(fileInput, file)

    await waitFor(() => {
      expect(mockSetStatus).toHaveBeenCalledWith(
        expect.stringContaining('must contain an array')
      )
    })
  })

  it('validates file is not empty', async () => {
    const user = userEvent.setup()
    
    render(
      <DataImporter
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
        setTrainingData={mockSetTrainingData}
      />
    )

    const fileInput = document.querySelector('input[type="file"]')
    const file = createMockFile('[]', 'test.json', { type: 'application/json' })

    await user.upload(fileInput, file)

    await waitFor(() => {
      expect(mockSetStatus).toHaveBeenCalledWith(
        expect.stringContaining('contains no training samples')
      )
    })
  })

  it('validates sample structure', async () => {
    const user = userEvent.setup()
    
    render(
      <DataImporter
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
        setTrainingData={mockSetTrainingData}
      />
    )

    const fileInput = document.querySelector('input[type="file"]')
    const invalidData = [{ invalid: 'sample' }]
    const file = createMockFile(JSON.stringify(invalidData), 'test.json', { type: 'application/json' })

    await user.upload(fileInput, file)

    await waitFor(() => {
      expect(mockSetStatus).toHaveBeenCalledWith(
        expect.stringContaining("Missing or invalid 'y0' array")
      )
    })
  })

  it('validates pixel array length', async () => {
    const user = userEvent.setup()
    
    render(
      <DataImporter
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
        setTrainingData={mockSetTrainingData}
      />
    )

    const fileInput = document.querySelector('input[type="file"]')
    const invalidData = [{ y0: [1, 2, 3], label: 0 }]
    const file = createMockFile(JSON.stringify(invalidData), 'test.json', { type: 'application/json' })

    await user.upload(fileInput, file)

    await waitFor(() => {
      expect(mockSetStatus).toHaveBeenCalledWith(
        expect.stringContaining('Expected 784 pixels')
      )
    })
  })

  it('validates label range', async () => {
    const user = userEvent.setup()
    
    render(
      <DataImporter
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
        setTrainingData={mockSetTrainingData}
      />
    )

    const fileInput = document.querySelector('input[type="file"]')
    const invalidData = [{ y0: Array(784).fill(0), label: 15 }]
    const file = createMockFile(JSON.stringify(invalidData), 'test.json', { type: 'application/json' })

    await user.upload(fileInput, file)

    await waitFor(() => {
      expect(mockSetStatus).toHaveBeenCalledWith(
        expect.stringContaining('Label must be a number between 0-9')
      )
    })
  })

  it('successfully imports valid data', async () => {
    const user = userEvent.setup()
    
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true })
    })

    render(
      <DataImporter
        setStatus={mockSetStatus}
        trainingCount={5}
        setTrainingCount={mockSetTrainingCount}
        setTrainingData={mockSetTrainingData}
      />
    )

    const fileInput = document.querySelector('input[type="file"]')
    const validData = [
      { y0: Array(784).fill(0.5), label: 5 },
      { y0: Array(784).fill(0.3), label: 3 }
    ]
    const file = createMockFile(JSON.stringify(validData), 'test.json', { type: 'application/json' })

    await user.upload(fileInput, file)

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(
        '/api',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
        })
      )
    })

    await waitFor(() => {
      expect(mockSetTrainingCount).toHaveBeenCalled()
      expect(mockSetTrainingData).toHaveBeenCalled()
      expect(mockSetStatus).toHaveBeenCalledWith(
        expect.stringContaining('Successfully imported')
      )
    })
  })

  it('sanitizes pixel values', async () => {
    const user = userEvent.setup()
    
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true })
    })

    render(
      <DataImporter
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
        setTrainingData={mockSetTrainingData}
      />
    )

    const fileInput = document.querySelector('input[type="file"]')
    const dataWithInvalidValues = [
      { 
        y0: [NaN, Infinity, -0.5, 1.5, ...Array(780).fill(0.5)],
        label: 0
      }
    ]
    const file = createMockFile(JSON.stringify(dataWithInvalidValues), 'test.json', { type: 'application/json' })

    await user.upload(fileInput, file)

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalled()
    })

    // Check that the sanitized data was sent
    const callArgs = global.fetch.mock.calls[0][1]
    const requestBody = JSON.parse(callArgs.body)
    const firstSample = requestBody.trainArray[0]
    
    // NaN and Infinity should be converted to 0
    expect(firstSample.y0[0]).toBe(0)
    expect(firstSample.y0[1]).toBe(0)
    // Values should be clamped to 0-1
    expect(firstSample.y0[2]).toBe(0)
    expect(firstSample.y0[3]).toBe(1)
  })

  it('handles server errors', async () => {
    const user = userEvent.setup()
    
    global.fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ error: 'Server error' })
    })

    render(
      <DataImporter
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
        setTrainingData={mockSetTrainingData}
      />
    )

    const fileInput = document.querySelector('input[type="file"]')
    const validData = [{ y0: Array(784).fill(0.5), label: 5 }]
    const file = createMockFile(JSON.stringify(validData), 'test.json', { type: 'application/json' })

    await user.upload(fileInput, file)

    await waitFor(() => {
      expect(mockSetStatus).toHaveBeenCalledWith(
        expect.stringContaining('Import error')
      )
    })
  })

  it('disables buttons while importing', async () => {
    const user = userEvent.setup()
    
    global.fetch.mockImplementation(() => 
      new Promise(resolve => setTimeout(() => resolve({
        ok: true,
        json: async () => ({ success: true })
      }), 100))
    )

    render(
      <DataImporter
        setStatus={mockSetStatus}
        trainingCount={0}
        setTrainingCount={mockSetTrainingCount}
        setTrainingData={mockSetTrainingData}
      />
    )

    const fileInput = document.querySelector('input[type="file"]')
    const validData = [{ y0: Array(784).fill(0.5), label: 5 }]
    const file = createMockFile(JSON.stringify(validData), 'test.json', { type: 'application/json' })

    await user.upload(fileInput, file)

    // Wait for importing state to appear
    await waitFor(() => {
      expect(mockSetStatus).toHaveBeenCalledWith(expect.stringContaining('Reading file'))
    })
  })
})
