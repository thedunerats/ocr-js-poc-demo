# OCR-JS POC Demo

A proof-of-concept OCR (Optical Character Recognition) application with a Python neural network backend and JavaScript frontend, fully containerized with Docker.

## Project Structure

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
