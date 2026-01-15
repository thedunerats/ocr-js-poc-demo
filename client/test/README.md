# Client Test Suite

This directory contains **33 comprehensive tests** for the OCR React frontend, covering components, user interactions, and API integration.

## Overview

- **Total Tests**: 33
- **Test Files**: 3
- **Framework**: Vitest + React Testing Library
- **Coverage**: Components, interactions, API calls, error handling

## Test Structure

```
test/
├── setup.js                  # Test environment setup
├── App.test.jsx             # App component tests (7 tests)
├── DrawingCanvas.test.jsx   # DrawingCanvas component tests (13 tests)
├── integration.test.jsx     # API integration tests (13 tests)
└── README.md                # This file
```

## Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm test -- --watch

# Run tests with UI
npm run test:ui

# Run tests with coverage
npm run test:coverage
```

## Test Coverage

### 📊 Coverage Statistics
- **Statements**: >85%
- **Branches**: >80%
- **Functions**: >85%
- **Lines**: >85%

### App Component (7 tests)
- ✅ Renders main heading "OCR Neural Network Demo"
- ✅ Renders subtitle with instructions
- ✅ Displays training count (starts at 0)
- ✅ Shows training tips and recommendations
- ✅ Renders DrawingCanvas component properly
- ✅ Status message display/hide logic
- ✅ Updates training count when training occurs

### DrawingCanvas Component (13 tests)
- ✅ Canvas rendering (200x200px)
- ✅ Digit input field with placeholder
- ✅ All control buttons (Add to Batch, Train Now, Test, Reset)
- ✅ Batch status display when samples added
- ✅ User can type digits (0-9)
- ✅ Reset button clears canvas and input
- ✅ Warning when training without drawing
- ✅ Warning when training without entering digit
- ✅ Warning when testing without drawing
- ✅ Training request when batch is full
- ✅ Fetch error handling
- ✅ Digit input validation (0-9)
- ✅ Batch count display

### API Integration (13 tests)
- ✅ Training API requests
- ✅ Prediction API requests
- ✅ Error response handling (400, 500)
- ✅ Network failure handling
- ✅ Data sanitization
- ✅ Batch management

## Testing Tools

- **Vitest**: Fast unit test framework
- **React Testing Library**: Testing React components
- **jsdom**: DOM implementation for Node.js
- **@testing-library/user-event**: User interaction simulation

## Writing New Tests

Example test structure:

```javascript
import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import MyComponent from '../src/components/MyComponent'

describe('MyComponent', () => {
  it('renders correctly', () => {
    render(<MyComponent />)
    expect(screen.getByText(/expected text/i)).toBeInTheDocument()
  })
})
```

## Mocking

### Fetch API
```javascript
global.fetch = vi.fn(() =>
  Promise.resolve({
    ok: true,
    json: async () => ({ success: true })
  })
)
```

### Canvas Context
Canvas operations are mocked in the test environment. For detailed canvas testing, consider additional mocking as needed.

## Best Practices

1. **Arrange-Act-Assert**: Structure tests clearly
2. **User-centric**: Test from user's perspective
3. **Descriptive names**: Make test intentions clear
4. **Isolated**: Each test should be independent
5. **Fast**: Keep tests quick and focused

## Coverage Goals

- Aim for >80% code coverage
- Focus on critical user paths
- Test error conditions
- Validate edge cases

## Continuous Integration

Tests run automatically in CI/CD pipeline. All tests must pass before merging.
