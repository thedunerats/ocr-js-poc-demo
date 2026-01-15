# OCR Client - React App

A modern React application for training and testing an OCR neural network with a drawing interface.

## Features

- 🎨 **Interactive Drawing Canvas**: Draw digits with your mouse
- 🎓 **Training Mode**: Collect and send training batches to the neural network
- 🧪 **Testing Mode**: Test predictions in real-time
- 🎯 **Batch Processing**: Automatically sends training data in batches of 10
- 📊 **Visual Feedback**: See training progress and prediction results
- 🎭 **Modern UI**: Beautiful gradient design with smooth animations

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- OCR server running on `http://localhost:3000`

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

### Build for Production

```bash
# Create production build
npm run build

# Preview production build
npm run preview
```

## Usage

1. **Draw a Digit**: Click and drag on the canvas to draw a digit (0-9)
2. **Train**: 
   - Enter the digit you drew in the input field
   - Click "Add to Batch" to collect samples (auto-trains after 3)
   - OR click "Train Now" to train immediately
   - Repeat for all digits 0-9 (at least 3-5 examples each)
3. **Test**: Draw a digit and click "Test" to see what the network predicts
4. **Reset**: Clear the canvas to start over

### Training Strategy

**Quick Start (30 samples minimum)**:
- Train 3 examples of each digit (0-9)
- Use "Train Now" for immediate feedback
- Total time: ~5-10 minutes

**Better Accuracy (50+ samples)**:
- Train 5+ examples of each digit
- Vary your handwriting style
- Mix using "Add to Batch" and "Train Now"

**Why you need 30+ samples**:
- Network needs to learn all digits (0-9)
- Too few samples = poor predictions
- Unbalanced training = biased predictions
- More variety = better generalization

## API Integration

The client connects to the Flask backend through a Vite proxy:

- **Development**: `http://localhost:5173/api` → `http://localhost:3000`
- **Production**: Configure your backend URL in `vite.config.js`

### API Endpoints

**POST /api**

Training request:
```json
{
  "train": true,
  "trainArray": [
    {"y0": [/* 400 pixel array */], "label": 5}
  ]
}
```

Prediction request:
```json
{
  "predict": true,
  "image": [/* 400 pixel array */]
}
```

## 🧪 Testing

The client includes a comprehensive test suite with 33 tests covering components, interactions, and API integration.

### Quick Test Commands

```bash
# Run all tests (watch mode)
npm test

# Run tests once
npm run test:run

# Run tests with coverage report
npm run test:coverage

# Open interactive UI
npm run test:ui
```

### Test Coverage

**33 tests across 3 test files:**

1. **App Component Tests** (`test/App.test.jsx`) - 7 tests
   - Rendering and display
   - Status messages
   - Training count
   - Tips display

2. **DrawingCanvas Tests** (`test/DrawingCanvas.test.jsx`) - 13 tests
   - Canvas rendering and interactions
   - User input validation
   - Button functionality
   - Drawing mechanics
   - Batch management

3. **Integration Tests** (`test/integration.test.jsx`) - 13 tests
   - Training API calls
   - Prediction API calls
   - Error handling
   - Data sanitization
   - Full workflows

### Coverage Report

After running `npm run test:coverage`, view the HTML report:

```bash
# Windows
start coverage/index.html

# Mac/Linux
open coverage/index.html
```

### CI/CD Integration

Tests run automatically in GitHub Actions:
- On every push
- On every pull request
- Must pass before merging

## Project Structure

```
client/
├── src/
│   ├── components/
│   │   ├── DrawingCanvas.jsx      # Main canvas component
│   │   └── DrawingCanvas.css      # Canvas styles
│   ├── App.jsx                    # Main app component
│   ├── App.css                    # App styles
│   ├── main.jsx                   # React entry point
│   └── index.css                  # Global styles
├── test/
│   ├── setup.js                   # Test environment setup
│   ├── App.test.jsx               # App component tests (7 tests)
│   ├── DrawingCanvas.test.jsx     # Canvas tests (13 tests)
│   └── integration.test.jsx       # API integration tests (13 tests)
├── index.html                     # HTML template
├── vite.config.js                 # Vite configuration
├── vitest.config.js               # Test configuration
└── package.json                   # Dependencies
```

## Configuration

### Change Backend URL

Edit `vite.config.js`:

```javascript
server: {
  proxy: {
    '/api': {
      target: 'http://your-backend-url:3000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
}
```

### Change Batch Size

Edit `DrawingCanvas.jsx`:

```javascript
const BATCH_SIZE = 10 // Change this value
```

## Technologies

- **React 18**: UI framework
- **Vite**: Build tool and dev server
- **Vitest**: Test runner with coverage
- **Testing Library**: React component testing
- **Canvas API**: Drawing interface
- **Fetch API**: HTTP requests to backend

## Development

- Hot Module Replacement (HMR) for instant updates
- ESLint for code quality
- Modern ES6+ JavaScript
- CSS with animations and responsive design

## Tips

- Train multiple variations of each digit for better accuracy
- Use different writing styles and sizes
- The more training data, the better the predictions
- The network requires at least 10 samples before training
