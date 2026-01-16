# OCR Server

A containerized OCR (Optical Character Recognition) neural network server built with Python and Flask.

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python run.py

# Server will be available at http://localhost:3000
```

### Docker Deployment

#### Prerequisites
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Docker Compose

#### Run the Server

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

### POST /train
Train the neural network with provided training data.

**Request:**
```json
{
  "trainArray": [
    {
      "y0": [/* 784-element array representing 28x28 pixel image */],
      "label": 5
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Training completed"
}
```

### POST /predict
Make a prediction using the trained neural network.

**Request:**
```json
{
  "image": [/* 784-element array representing 28x28 pixel image */]
}
```

**Response:**
```json
{
  "type": "test",
  "result": 7
}
```

### POST /optimize

Find optimal neural network configuration by testing different hidden node counts.

**Data Requirements:**
- Minimum 10 total samples (for 70/30 train/test split)
- Recommended 30+ samples (3+ per digit 0-9) for reliable results
- With <30 samples, expect low accuracy (0-30%) as network cannot learn all digit patterns

**Request:**
```json
{
  "trainingData": [{"y0": [/* 784 values */], "label": 5}, ...],
  "testData": [{"y0": [/* 784 values */], "label": 3}, ...],
  "minNodes": 5,
  "maxNodes": 30,
  "step": 5
}
```

**Response:**
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

**Note:** With insufficient data, the response includes warnings:
```json
{
  "message": "Optimization completed. Tested 6 configurations. ⚠️ Warning: Only 7 training samples may not be enough for reliable results. Recommend 30+ samples (3+ per digit 0-9). ⚠️ Low accuracy detected - network needs more diverse training data."
}
```

## Testing

The server includes a comprehensive test suite with 64+ tests covering all components.

### Quick Test Commands

```bash
# Run all tests
docker-compose run --rm ocr-tests

# Run all tests locally
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test/test_ocr.py
pytest test/test_app.py
pytest test/test_neural_network_design.py

# Run with coverage
pytest --cov=src --cov-report=html
```

### Test Coverage

**OCR Neural Network Tests** (`test/test_ocr.py` - 28 tests)
- ✅ Initialization and weight configuration
- ✅ Training with various data formats
- ✅ Prediction accuracy
- ✅ Model save/load functionality
- ✅ Backup system (create, restore, cleanup)
- ✅ Edge cases and validation
- ✅ Numerical stability (sigmoid overflow protection)
- ✅ Invalid input handling

**Flask API Tests** (`test/test_app.py` - 39 tests)
- ✅ Health check endpoint
- ✅ Training endpoint validation
- ✅ Prediction endpoint validation
- ✅ **Optimization endpoint** (14 tests)
- ✅ CORS headers
- ✅ Error responses (400, 500)
- ✅ Input sanitization
- ✅ Array size validation
- ✅ Label range validation
- ✅ Non-numeric value detection

**Neural Network Design Tests** (`test/test_neural_network_design.py` - 18 tests)
- ✅ Model testing utilities
- ✅ Accuracy calculations
- ✅ Different network configurations
- ✅ **Optimal hidden nodes search**
- ✅ Data splitting
- ✅ Empty dataset handling

### Coverage Report

```bash
# Generate HTML coverage report
docker-compose --profile test up ocr-tests-coverage

# Or locally
pytest --cov=src --cov-report=html

# Open htmlcov/index.html in browser
```

### Interactive Testing

```bash
# Run tests interactively in container
docker-compose run --rm ocr-tests bash

# Inside container:
pytest -v                    # All tests
pytest test/test_ocr.py     # Specific file
pytest -k "backup"          # Tests matching pattern
exit
```

## Project Structure

```
server/
├── src/
│   ├── __init__.py                 # Package marker
│   ├── app.py                      # Flask application
│   ├── ocr.py                      # Neural network implementation
│   └── neural_network_design.py   # Network optimization
├── test/
│   ├── __init__.py                 # Test package init
│   ├── test_ocr.py                 # Neural network tests (28 tests)
│   ├── test_app.py                 # Flask API tests (39 tests)
│   └── test_neural_network_design.py  # Design utility tests (18 tests)
├── Dockerfile                      # Production server image
├── Dockerfile.test                 # Test runner image
├── docker-compose.yml              # Docker Compose configuration
├── .dockerignore                   # Docker ignore patterns
├── run.py                          # Application entry point
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## How It Works

### Neural Network
- **Architecture**: Feedforward neural network
  - Input layer: 784 nodes (28×28 pixel images)
  - Hidden layer: Configurable (default: 20 nodes)
  - Output layer: 10 nodes (digits 0-9)
- **Training**: Backpropagation with gradient descent
- **Activation**: Sigmoid function
- **Framework**: Custom implementation using NumPy
- **Model Persistence**: Automatic backup system
  - Creates timestamped backups before overwriting (e.g., `ocr_neural_network.json.backup.20260107_143000`)
  - Keeps last 5 backups by default (configurable via `max_backups` parameter)
  - Supports restore from any backup using `restore_from_backup(backup_index)`
  - List all backups with `list_backups()`

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
- Training data is provided through the React client interface
- For production OCR, consider using Tesseract or deep learning frameworks like TensorFlow/PyTorch
- Docker images are optimized for size using Python slim base image
- Health checks ensure the server is responding correctly

## Model Backup & Restore

The neural network includes production-grade backup protection to prevent loss of trained models.

### Automatic Backups

Every time you save a model, the system automatically:
1. Creates a timestamped backup of the existing model (if one exists)
2. Saves the new model
3. Cleans up old backups to save disk space

**Example:**
```python
nn = OCRNeuralNetwork(...)
nn.save()  # Creates backup like: ocr_neural_network.json.backup.20260107_143000
nn.save(max_backups=10)  # Keep up to 10 backups (default: 5)
```

### Restore from Backup

If a model update degrades performance, restore from a previous backup:

```python
# Restore the most recent backup
nn.restore_from_backup(backup_index=0)

# Restore the second most recent backup
nn.restore_from_backup(backup_index=1)
```

### List Available Backups

View all available backups sorted by most recent first:

```python
backups = nn.list_backups()
for timestamp, filepath in backups:
    print(f"Backup from {timestamp}: {filepath}")
```

### Production Recommendations

1. **Regular Backups**: Models are automatically backed up on each save
2. **Backup Retention**: Adjust `max_backups` based on your disk space and update frequency
3. **Monitoring**: Keep the 5-10 most recent backups for quick rollback
4. **Testing**: Always validate model accuracy before deploying to production
5. **Manual Backups**: For critical deployments, manually copy the JSON file before major changes

## Testing Details

**Total: 46+ unit tests**

- **test_ocr.py**: 15 tests for OCRNeuralNetwork class
- **test_server.py**: 18 tests for Flask endpoints
- **test_neural_network_design.py**: 13 tests for design utilities

All tests run automatically in isolated Docker containers with consistent environments.
