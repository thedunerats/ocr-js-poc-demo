# Client Test Suite

This directory contains unit and integration tests for the OCR React frontend.

## Test Structure

```
test/
├── setup.js                  # Test environment setup
├── App.test.jsx             # App component tests
├── DrawingCanvas.test.jsx   # DrawingCanvas component tests
└── integration.test.jsx     # API integration tests
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

The test suite covers:

### App Component
- ✅ Renders main heading and subtitle
- ✅ Displays training count
- ✅ Shows training tips
- ✅ Renders DrawingCanvas component
- ✅ Status message handling

### DrawingCanvas Component
- ✅ Canvas rendering
- ✅ User input handling (digit entry)
- ✅ Control buttons (Train, Test, Clear)
- ✅ Batch status display
- ✅ Form validation
- ✅ Error handling

### API Integration
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
