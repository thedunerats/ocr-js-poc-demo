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
│   └── package.json
├── server/          # Flask backend
│   ├── src/
│   │   ├── app.py              # Flask application
│   │   ├── ocr.py              # Neural network implementation
│   │   └── neural_network_design.py
│   ├── test/                   # Comprehensive test suite
│   ├── Dockerfile
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

```
ocr-js-poc-demo/
├── client/           # Frontend application
│   ├── src/
│   │   ├── ocr.html  # Main HTML interface
│   │   └── ocr.js    # Client-side JavaScript
│   └── test/
├── server/           # Python backend server (Dockerized)
│   ├── src/
│   │   ├── ocr.py                      # Neural network implementation
│   │   ├── server.py                   # Flask application
│   │   └── neural_network_design.py   # Network configuration testing
│   ├── test/
│   │   ├── test_ocr.py                 # OCR tests
│   │   ├── test_server.py              # Flask endpoint tests
│   │   └── test_neural_network_design.py  # Design utility tests
│   ├── Dockerfile                      # Production server image
│   ├── Dockerfile.test                 # Test runner image
│   ├── docker-compose.yml              # Docker orchestration
│   ├── .dockerignore                   # Docker ignore patterns
│   ├── requirements.txt                # Python dependencies
│   └── README.md                       # Server documentation
└── README.md         # This file
```

## Quick Start

### Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose
- Modern web browser for the client

### Server Setup (Docker)

1. Navigate to the server directory:
   ```bash
   cd server
   ```

2. Build and start the server:
   ```bash
   docker-compose up -d ocr-server
   ```

3. Verify the server is running:
   ```bash
   curl http://localhost:3000/health
   ```

### Run Tests

```bash
cd server
docker-compose run --rm ocr-tests
```

### Client Setup

1. Open `client/src/ocr.html` in a web browser
2. The client will connect to the server at `http://localhost:3000`

## How It Works

### Neural Network
- **Architecture**: Feedforward neural network
  - Input layer: 400 nodes (20×20 pixel images)
  - Hidden layer: Configurable (default: 20 nodes)
  - Output layer: 10 nodes (digits 0-9)
- **Training**: Backpropagation with gradient descent
- **Activation**: Sigmoid function
- **Framework**: Custom implementation using NumPy

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

## Testing

The project includes comprehensive unit tests for all server components.

### Running Tests
```bash
cd server
test.bat  # Windows

# Or manually:
pytest
```

### Running Tests with Coverage
```bash
pytest --cov=src --cov-report=html
```

### Test Files
- `test/test_ocr.py` - Tests for OCRNeuralNetwork class
- `test/test_server.py` - Tests for Flask endpoints
- `test/test_neural_network_design.py` - Tests for network optimization utilities

## Dependencies

### Server
- Docker & Docker Compose
- Python 3.13 (in container)
- NumPy - Numerical computing
- Flask - Web framework
- Flask-CORS - Cross-origin resource sharing
- pytest - Testing framework

See [server/requirements.txt](server/requirements.txt) for full list.

### Client
- Modern web browser with JavaScript support
- No additional dependencies required

## Development

### Server Development
```bash
cd server

# Start with live code reloading (volume-mounted)
docker-compose up ocr-server

# Make changes to src/*.py files - changes reflect immediately

# Run tests after changes
docker-compose run --rm ocr-tests

# Access container shell
docker-compose exec ocr-server bash
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

- This is a proof-of-concept demonstration
- The neural network implementation is educational and not optimized for production
- For production OCR, consider using:
  - Tesseract OCR
  - Google Cloud Vision API
  - TensorFlow/PyTorch with pre-trained models

## License

This is a demonstration project.
