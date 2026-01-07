# OCR Server - Docker Setup

A containerized OCR (Optical Character Recognition) neural network server built with Python and Flask.

## Quick Start with Docker

### Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose

### Run the Server

```bash
# Start the server
docker-compose up ocr-server

# Or run in detached mode
docker-compose up -d ocr-server
```

The server will be available at: `http://localhost:3000`

### Run Tests

```bash
# Run all tests
docker-compose run --rm ocr-tests

# Run with coverage
docker-compose --profile test up ocr-tests-coverage

# Run specific test file
docker-compose run --rm ocr-tests pytest test/test_ocr.py

# Run with custom pytest arguments
docker-compose run --rm ocr-tests pytest -v -k "test_predict"
```

### Development Mode

```bash
# Build and start with live code reloading
docker-compose up --build ocr-server

# View logs
docker-compose logs -f ocr-server

# Stop the server
docker-compose down
```

## Docker Commands Reference

### Building

```bash
# Build the application image
docker build -t ocr-server .

# Build the test image
docker build -f Dockerfile.test -t ocr-server-test .

# Build all services
docker-compose build
```

### Running

```bash
# Run server on custom port
docker run -p 5000:3000 ocr-server

# Run tests
docker run --rm ocr-server-test

# Run with environment variables
docker run -e PORT=5000 -p 5000:5000 ocr-server
```

### Management

```bash
# Stop all containers
docker-compose down

# Remove volumes
docker-compose down -v

# View running containers
docker ps

# View logs
docker-compose logs ocr-server
docker logs ocr-server
```

## API Endpoints

### GET /health
Health check endpoint to verify the server is running.

**Response:**
```json
{
  "status": "healthy",
  "message": "OCR server is running"
}
```

### POST /
Accepts JSON payloads for training and prediction:

**Training:**
```json
{
  "train": true,
  "trainArray": [
    {
      "y0": [/* 400-element array representing 20x20 pixel image */],
      "label": 5
    }
  ]
}
```

**Prediction:**
```json
{
  "predict": true,
  "image": [/* 400-element array representing 20x20 pixel image */]
}
```

**Response:**
```json
{
  "type": "test",
  "result": 5
}
```

## Testing

### Run All Tests
```bash
docker-compose run --rm ocr-tests
```

### Run Specific Test File
```bash
docker-compose run --rm ocr-tests pytest test/test_ocr.py
docker-compose run --rm ocr-tests pytest test/test_server.py
docker-compose run --rm ocr-tests pytest test/test_neural_network_design.py
```

### Run with Coverage
```bash
docker-compose --profile test up ocr-tests-coverage
```

Coverage report will be in `htmlcov/index.html`

### Interactive Testing
```bash
# Run tests interactively
docker-compose run --rm ocr-tests bash
# Inside container:
pytest -v
pytest --cov=src
exit
```

## Project Structure

```
server/
├── src/
│   ├── ocr.py                      # Neural network implementation
│   ├── server.py                   # Flask application
│   └── neural_network_design.py   # Network optimization
├── test/
│   ├── __init__.py                 # Test package init
│   ├── test_ocr.py                 # OCR tests (15 tests)
│   ├── test_server.py              # Flask endpoint tests (18 tests)
│   └── test_neural_network_design.py  # Design utility tests (13 tests)
├── Dockerfile                      # Production server image
├── Dockerfile.test                 # Test runner image
├── docker-compose.yml              # Docker Compose configuration
├── .dockerignore                   # Docker ignore patterns
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## How It Works

### Neural Network
- **Architecture**: Feedforward neural network
  - Input layer: 400 nodes (20×20 pixel images)
  - Hidden layer: Configurable (default: 20 nodes)
  - Output layer: 10 nodes (digits 0-9)
- **Training**: Backpropagation with gradient descent
- **Activation**: Sigmoid function
- **Framework**: Custom implementation using NumPy

### Docker Setup
- **Base Image**: Python 3.13-slim (lightweight)
- **Multi-stage**: Separate images for app and tests
- **Health Checks**: Automatic health monitoring
- **Volumes**: Code mounting for development
- **Profiles**: Test services run on-demand

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 3000 | Server port |
| `PYTEST_ARGS` | `-v` | Pytest arguments for tests |

### Customize Port

```bash
# Using docker-compose
PORT=5000 docker-compose up ocr-server

# Using docker run
docker run -e PORT=5000 -p 5000:5000 ocr-server
```

## Production Deployment

```bash
# Build production image
docker build -t ocr-server:latest .

# Run without volume mounts
docker run -d -p 3000:3000 --name ocr-server ocr-server:latest

# Or use docker-compose without volumes
# (comment out volumes in docker-compose.yml)
docker-compose up -d ocr-server
```

## Troubleshooting

### Port Already in Use
```bash
# Use different port
docker run -p 5000:3000 ocr-server

# Or stop conflicting container
docker ps
docker stop <container-id>
```

### View Container Logs
```bash
docker-compose logs -f ocr-server
docker logs -f ocr-server
```

### Rebuild After Changes
```bash
docker-compose up --build ocr-server
```

### Clean Up Everything
```bash
# Stop and remove containers
docker-compose down

# Remove images
docker rmi ocr-server ocr-server-test

# Remove unused Docker resources
docker system prune -a
```

## Development Tips

1. **Live Reloading**: The docker-compose.yml includes volume mounts for development. Changes to source files will be reflected without rebuilding.

2. **Interactive Shell**: Access container shell for debugging:
   ```bash
   docker-compose exec ocr-server bash
   ```

3. **Test-Driven Development**: Keep tests running in watch mode:
   ```bash
   docker-compose run --rm ocr-tests pytest -v --tb=short -f
   ```

4. **Coverage Reports**: Generate and view coverage:
   ```bash
   docker-compose --profile test up ocr-tests-coverage
   # Open htmlcov/index.html in browser
   ```

## Migration from Batch Scripts

Previously using `.bat` scripts? Here's the Docker equivalent:

| Old Command | New Docker Command |
|-------------|-------------------|
| `setup.bat` | `docker-compose build` |
| `run.bat` | `docker-compose up ocr-server` |
| `test.bat` | `docker-compose run --rm ocr-tests` |

## Notes

- The neural network saves its trained weights to `ocr_neural_network.json`
- Training data should be provided through the client interface
- For production OCR, consider using Tesseract or deep learning frameworks like TensorFlow/PyTorch
- Docker images are optimized for size using Python slim base image
- Health checks ensure the server is responding correctly

## Testing Details

**Total: 46+ unit tests**

- **test_ocr.py**: 15 tests for OCRNeuralNetwork class
- **test_server.py**: 18 tests for Flask endpoints
- **test_neural_network_design.py**: 13 tests for design utilities

All tests run automatically in isolated Docker containers with consistent environments.
