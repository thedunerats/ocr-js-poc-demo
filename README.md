# OCR Neural Network Demo

A full-stack OCR (Optical Character Recognition) application with a custom neural network backend and modern React frontend.

## 🎯 Features

- **Custom Neural Network**: Feedforward neural network implemented from scratch with NumPy
- **Interactive Drawing Interface**: React-based canvas for drawing digits
- **Real-time Training**: Train the network with your own handwriting
- **Live Predictions**: Test the network's accuracy instantly
- **Production-Ready**: Docker support, CI/CD pipeline, comprehensive testing
- **Model Backup System**: Automatic versioned backups with restore capability

## 🏗️ Architecture

```
ocr-js-poc-demo/
├── client/          # React frontend (Vite)
│   ├── src/
│   │   ├── components/
│   │   │   └── DrawingCanvas.jsx
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── test/                   # Client test suite (33 tests)
│   │   ├── App.test.jsx
│   │   ├── DrawingCanvas.test.jsx
│   │   ├── integration.test.jsx
│   │   └── setup.js
│   ├── package.json
│   ├── vite.config.js
│   └── vitest.config.js        # Test configuration
├── server/          # Flask backend
│   ├── src/
│   │   ├── app.py              # Flask application
│   │   ├── ocr.py              # Neural network implementation
│   │   └── neural_network_design.py
│   ├── test/                   # Server test suite (64+ tests)
│   ├── Dockerfile
│   ├── run.py
│   └── requirements.txt
└── .github/workflows/  # CI/CD pipeline
```

## 🚀 Quick Start

### Option 1: Run Locally (Recommended for Development)

**Prerequisites:**
- Python 3.13+
- Node.js 18+
- npm

**Step 1: Start the Server**

```powershell
cd server
pip install -r requirements.txt
python run.py
```

The server will start on `http://localhost:3000`

**Step 2: Start the Client (in a new terminal)**

```powershell
cd client
npm install
npm run dev
```

The client will start on `http://localhost:5173`

**Or use the convenience script:**

```powershell
# Run from project root
.\start.ps1
```

**Step 3: Run Tests (Optional)**

```powershell
# Test the server
cd server
pytest

# Test the client
cd client
npm test
```

## 📖 Using the Application

### Training the Neural Network

1. **Open the app** at `http://localhost:5173`
2. **Draw a digit** (0-9) on the black canvas using your mouse
3. **Enter the digit** you drew in the input field
4. **Choose training method**:
   - **Add to Batch**: Collects samples, auto-trains after 3
   - **Train Now**: Trains immediately with current drawing
5. **Train multiple digits**: Repeat for all digits 0-9

### Testing Predictions

1. **Draw a digit** on the canvas
2. **Click "Test"** button
3. **See the prediction** displayed in the status message

### Quick Training Strategy (Recommended)

For best results, train at least **3-5 examples of each digit**:

```
Step 1: Draw "0" → enter 0 → click "Train Now" (repeat 3-5 times)
Step 2: Draw "1" → enter 1 → click "Train Now" (repeat 3-5 times)
Step 3: Draw "2" → enter 2 → click "Train Now" (repeat 3-5 times)
... continue through all digits 0-9 ...
```

**Minimum training**: 30 samples (3 per digit × 10 digits)  
**Recommended**: 50+ samples (5+ per digit) for better accuracy

### Training Tips

- ✅ **Vary your handwriting** - different sizes and styles
- ✅ **Use the full canvas** - don't draw too small
- ✅ **Train all digits** - network needs examples of each (0-9)
- ✅ **Train more = better accuracy** - more data improves predictions
- ⚠️ **Wait for training** - let each batch complete before testing

## 🛠️ Tech Stack

### Frontend
- **Framework**: React 18 with Vite
- **Testing**: Vitest + React Testing Library (33 tests)
- **Canvas API**: For drawing interface
- **Build Tool**: Vite with HMR

### Backend Neural Network
- **Architecture**: 3-layer feedforward network
  - Input layer: 400 nodes (20×20 pixel grid)
  - Hidden layer: 20 nodes
  - Output layer: 10 nodes (digits 0-9)
- **Training**: Backpropagation with gradient descent
- **Activation**: Sigmoid function
- **Framework**: Custom implementation using NumPy
- **Testing**: pytest (64+ tests)

### Server
- **Framework**: Flask with CORS support
- **Endpoints**:
  - `GET /health` - Health check
  - `POST /` - Training and prediction

### API
The server provides a simple REST API:
- `POST /` with `{ "train": true, "trainArray": [...] }` - Train the network
- `POST /` with `{ "predict": true, "image": [...] }` - Predict a digit
- `GET /health` - Check server status

## 📚 Documentation

- **[README.md](README.md)** - Main documentation (this file)
- **[DATA_FLOW_GUIDE.md](DATA_FLOW_GUIDE.md)** - Detailed explanation of data flow and neural network architecture
- **[DOCKER_GUIDE.md](DOCKER_GUIDE.md)** - Docker quick reference
- **[MIGRATION.md](MIGRATION.md)** - Migration guide from batch scripts to Docker
- **[client/README.md](client/README.md)** - Frontend-specific documentation
- **[client/test/README.md](client/test/README.md)** - Client testing guide
- **[server/README.md](server/README.md)** - Backend-specific documentation

## 🧪 Testing

The project includes comprehensive test suites for both frontend and backend with **97+ total tests**.

### Server Tests (Python/pytest)

**Running Tests Locally:**
```bash
cd server
pytest                                    # Run all tests
pytest -v                                 # Verbose output
pytest --cov=src --cov-report=html       # With coverage
```

**Running Tests in Docker:**
```bash
cd server
docker-compose run --rm ocr-tests
```

**Test Coverage:**
- ✅ **64+ tests** across all server components
- ✅ **OCR Neural Network** (28 tests)
  - Initialization, training, prediction
  - Backup/restore functionality
  - Edge cases and validation
  - Numerical stability
- ✅ **Flask API** (24+ tests)
  - Training endpoint validation
  - Prediction endpoint validation
  - Error handling (400, 500)
  - CORS headers
  - Input sanitization
- ✅ **Neural Network Design** (12 tests)
  - Model testing utilities
  - Accuracy calculations
  - Configuration validation

### Client Tests (Vitest/React Testing Library)

**Running Tests:**
```bash
cd client
npm test                   # Watch mode
npm run test:run          # Run once
npm run test:coverage     # With coverage
npm run test:ui           # Interactive UI
```

**Test Coverage:**
- ✅ **33 tests** covering React components
- ✅ **App Component** (7 tests)
  - Rendering and layout
  - Training count display
  - Status messages
- ✅ **DrawingCanvas Component** (13 tests)
  - Canvas rendering
  - User interactions
  - Form validation
  - Button functionality
- ✅ **API Integration** (13 tests)
  - Training API calls
  - Prediction API calls
  - Error handling
  - Data sanitization
  - Batch management

### CI/CD Pipeline

**Automated Testing:**
The GitHub Actions workflow runs all tests on every push and pull request:
- ✅ **Server tests** (Python/pytest) - 64+ tests
  - OCR Neural Network (28 tests)
  - Flask API endpoints (24+ tests)
  - Neural network design utilities (12 tests)
- ✅ **Client tests** (JavaScript/Vitest) - 33 tests
  - App component (7 tests)
  - DrawingCanvas component (13 tests)
  - API integration (13 tests)
- ✅ Code coverage reports (both server and client)
- ✅ Linting (flake8, black)
- ✅ Build validation

**Total Test Coverage: 97+ tests**

**Test Files:**

**Server:**
- `test/test_ocr.py` - OCR Neural Network tests (28 tests)
- `test/test_app.py` - Flask API endpoint tests (24+ tests)
- `test/test_neural_network_design.py` - Network design utilities (12 tests)

**Client:**
- `test/App.test.jsx` - App component tests (7 tests)
- `test/DrawingCanvas.test.jsx` - Canvas component tests (13 tests)
- `test/integration.test.jsx` - API integration tests (13 tests)
- `test/setup.js` - Test environment configuration

## 📚 Documentation

- **[README.md](README.md)** - Main documentation (this file)
- **[DATA_FLOW_GUIDE.md](DATA_FLOW_GUIDE.md)** - Detailed explanation of data flow and neural network architecture
- **[DOCKER_GUIDE.md](DOCKER_GUIDE.md)** - Docker quick reference
- **[MIGRATION.md](MIGRATION.md)** - Migration guide from batch scripts to Docker
- **[client/README.md](client/README.md)** - Frontend-specific documentation
- **[client/test/README.md](client/test/README.md)** - Client testing guide
- **[server/README.md](server/README.md)** - Backend-specific documentation

## 📦 Dependencies

### Server
- Docker & Docker Compose
- Python 3.13 (in container)
- NumPy - Numerical computing
- Flask - Web framework
- Flask-CORS - Cross-origin resource sharing
- pytest - Testing framework
- pytest-cov - Test coverage

See [server/requirements.txt](server/requirements.txt) for full list.

### Client
- Node.js 18+ and npm
- React 18 - UI framework
- Vite - Build tool and dev server
- Vitest - Testing framework
- React Testing Library - Component testing
- jsdom - DOM implementation for tests

See [client/package.json](client/package.json) for full list.

## Development

### Server Development
```bash
cd server

# Start with live code reloading (volume-mounted)
docker-compose up ocr-server

# Make changes to src/*.py files - changes reflect immediately

# Run tests after changes
docker-compose run --rm ocr-tests

# Run specific test file
docker-compose run --rm ocr-tests pytest test/test_ocr.py -v

# Run with coverage
docker-compose run --rm ocr-tests pytest --cov=src --cov-report=html

# Access container shell
docker-compose exec ocr-server bash
```

### Client Development
```bash
cd client

# Start development server with HMR
npm run dev

# Run tests in watch mode (automatic re-run on changes)
npm test

# Run tests once
npm run test:run

# Run tests with coverage
npm run test:coverage

# Run tests with interactive UI
npm run test:ui

# Build for production
npm run build

# Preview production build
npm run preview
```

### Testing Network Configurations
```bash
cd server
docker-compose run --rm ocr-tests python src/neural_network_design.py
```

### Production Deployment
```bash
cd server

# Build production image (no volume mounts)
docker build -t ocr-server:prod .

# Run in production mode
docker run -d -p 3000:3000 --name ocr-server-prod ocr-server:prod

# Or edit docker-compose.yml to remove volume mounts
docker-compose up -d ocr-server
```

## Advantages of Docker Setup

✅ **Consistent Environment**: Same Python version and dependencies everywhere  
✅ **No Local Setup**: No need to install Python or manage virtual environments  
✅ **Isolated Testing**: Tests run in clean containers every time  
✅ **Easy CI/CD**: Simple integration with CI/CD pipelines  
✅ **Cross-Platform**: Works identically on Windows, Mac, and Linux  
✅ **Health Monitoring**: Built-in health checks  
✅ **Production-Ready**: Easy to deploy to cloud platforms

### Training Data
The network expects:
- Flattened 20×20 pixel images (400 values)
- Pixel values normalized between 0 and 1
- Labels from 0 to 9

## Notes

- This is a proof-of-concept demonstration with production-quality testing (97+ tests)
- The neural network implementation is educational and demonstrates core ML concepts
- Comprehensive test coverage ensures reliability and maintainability
- For production OCR at scale, consider using:
  - Tesseract OCR
  - Google Cloud Vision API
  - TensorFlow/PyTorch with pre-trained models
- See [DATA_FLOW_GUIDE.md](DATA_FLOW_GUIDE.md) for detailed architecture explanation

## License

This is a demonstration project.
