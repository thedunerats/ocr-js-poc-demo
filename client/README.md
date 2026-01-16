# OCR Client - React App

A modern React application for training and testing an OCR neural network with a drawing interface.

## Features

- 🎨 **Interactive Drawing Canvas**: Draw digits with your mouse
- 🎓 **Training Mode**: Collect and send training batches to the neural network
- 🧪 **Testing Mode**: Test predictions in real-time
- 🔧 **Network Optimizer**: Find optimal hidden layer configuration automatically
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

### Basic Workflow

1. **Draw a Digit**: Click and drag on the canvas to draw a digit (0-9)
2. **Train**: 
   - Enter the digit you drew in the input field
   - Click "Add to Batch" to collect samples (auto-trains after 3)
   - OR click "Train Now" to train immediately
   - Repeat for all digits 0-9 (at least 3-5 examples each)
3. **Test**: Draw a digit and click "Test" to see what the network predicts
4. **Optimize** (Optional): After collecting 10+ samples, use the optimizer to find the best configuration
5. **Reset**: Clear the canvas to start over

### Network Optimizer

The Network Optimizer helps you find the optimal number of hidden nodes for your training data. It automatically tests different network configurations and ranks them by accuracy.

**How to Use**:
1. **Collect Training Samples**: Draw and train at least 10 samples (minimum) or 30+ samples (recommended)
2. **Configure Parameters**:
   - **Min Nodes**: Starting point for testing (default: 5)
   - **Max Nodes**: Upper limit for testing (default: 30)
   - **Step**: Increment between tests (default: 5)
3. **Run Optimization**: Click "Find Optimal Configuration"
4. **Review Results**: View ranked configurations with accuracy scores

**Example**:
- Min=5, Max=30, Step=5 tests: 5, 10, 15, 20, 25, 30 hidden nodes
- 20 training samples = 14 train (70%), 6 test (30%)
- Best configuration shown with ⭐ OPTIMAL badge

**Data Requirements**:
- **Minimum:** 10 samples (required for 70/30 split)
- **Low Accuracy Warning:** 10-29 samples may show 0-30% accuracy (insufficient data)
- **Recommended:** 30+ samples (3+ per digit 0-9) for reliable results
- **Best Results:** 50+ samples (5+ per digit) for meaningful accuracy differences

**Tips**:
- More training samples = more reliable results
- With <30 samples, all configurations may show similar low accuracy
- Smaller step = more precise but slower
- Default range (5-30) works well for digit recognition
- Optimal node count varies based on your handwriting samples

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

**POST /api/train**

Training request:
```json
{
  "trainArray": [
    {"y0": [/* 784 pixel array (28×28) */], "label": 5}
  ]
}
```

**POST /api/predict**

Prediction request:
```json
{
  "image": [/* 784 pixel array */]
}
```

**POST /api/optimize**

Network optimization request:
```json
{
  "trainingData": [
    {"y0": [/* 784 pixel array */], "label": 5}
  ],
  "testData": [
    {"y0": [/* 784 pixel array */], "label": 3}
  ],
  "minNodes": 5,
  "maxNodes": 30,
  "step": 5
}
```

Response:
```json
{
  "results": [
    {"hiddenNodes": 20, "accuracy": 0.95},
    {"hiddenNodes": 15, "accuracy": 0.93}
  ],
  "optimal": {"hiddenNodes": 20, "accuracy": 0.95},
  "message": "Optimization completed. Tested 6 configurations."
}
```

## 🧪 Testing

The client includes a **comprehensive test suite with 51 tests** covering components, user interactions, API integration, and network optimization. All tests use **Vitest** and **React Testing Library** for reliable, maintainable testing.

📖 **See [test/README.md](test/README.md) for detailed testing documentation and examples.**

### Quick Test Commands

```bash
# Run all tests (watch mode - recommended during development)
npm test

# Run tests once (CI/CD mode)
npm run test:run

# Run tests with coverage report
npm run test:coverage

# Open interactive UI (great for debugging)
npm run test:ui
```

### Test Coverage Summary

**51 tests across 4 test files:**

1. **App Component Tests** ([test/App.test.jsx](test/App.test.jsx)) - **7 tests**
   - ✅ Main heading and subtitle rendering
   - ✅ Training count display and updates
   - ✅ Status message handling (show/hide)
   - ✅ Tips and recommendations display
   - ✅ DrawingCanvas integration

2. **DrawingCanvas Tests** ([test/DrawingCanvas.test.jsx](test/DrawingCanvas.test.jsx)) - **13 tests**
   - ✅ Canvas rendering (200x200px with grid)
   - ✅ User input validation (digit 0-9)
   - ✅ Button functionality (🎓 Add to Batch, ⚡ Train Now, 🧪 Test, 🔄 Reset)
   - ✅ Drawing mechanics and state management
   - ✅ Batch management and status display
   - ✅ Form validation and error messages
   - ✅ Canvas reset functionality

3. **Integration Tests** ([test/integration.test.jsx](test/integration.test.jsx)) - **13 tests**
   - ✅ Training API requests and responses
   - ✅ Prediction API requests and responses
   - ✅ Error handling (400, 500 errors)
   - ✅ Network failure handling
   - ✅ Data sanitization (NaN, undefined values)
   - ✅ Array length validation (784 elements)
   - ✅ Batch accumulation and sending

4. **NetworkOptimizer Tests** ([test/NetworkOptimizer.test.jsx](test/NetworkOptimizer.test.jsx)) - **18 tests**
   - ✅ Component rendering and UI elements
   - ✅ Input field validation (min/max/step)
   - ✅ Button states (disabled/enabled based on data)
   - ✅ Optimization API requests and data splitting (70/30)
   - ✅ Results display and ranking
   - ✅ Error handling (server errors, network failures)
   - ✅ Loading states and disabled inputs during optimization
   - ✅ Status message updates

### Test Coverage Metrics

- **Statements**: >85%
- **Branches**: >80%
- **Functions**: >85%
- **Lines**: >85%

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
│   │   ├── DrawingCanvas.css      # Canvas styles
│   │   ├── NetworkOptimizer.jsx   # Network optimization component
│   │   └── NetworkOptimizer.css   # Optimizer styles
│   ├── App.jsx                    # Main app component
│   ├── App.css                    # App styles
│   ├── main.jsx                   # React entry point
│   └── index.css                  # Global styles
├── test/
│   ├── setup.js                   # Test environment setup
│   ├── App.test.jsx               # App component tests (7 tests)
│   ├── DrawingCanvas.test.jsx     # Canvas tests (13 tests)
│   ├── integration.test.jsx       # API integration tests (13 tests)
│   └── NetworkOptimizer.test.jsx  # Optimizer tests (18 tests)
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
