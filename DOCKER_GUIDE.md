# 🐳 Docker Quick Reference

## Starting the Server

```bash
cd server
docker-compose up -d ocr-server
```

Server runs at: **http://localhost:3000**

## Running Tests

### Server Tests (Python)

```bash
# All server tests
docker-compose run --rm ocr-tests

# With coverage
docker-compose --profile test up ocr-tests-coverage

# Specific test
docker-compose run --rm ocr-tests pytest test/test_ocr.py -v
```

### Client Tests (JavaScript)

```bash
cd client

# All client tests
npm test

# Run once (non-watch mode)
npm run test:run

# With coverage
npm run test:coverage

# Interactive UI
npm run test:ui
```

## Common Commands

| Task | Command |
|------|---------|
| **Start server** | `docker-compose up -d ocr-server` |
| **Stop server** | `docker-compose down` |
| **View logs** | `docker-compose logs -f ocr-server` |
| **Rebuild** | `docker-compose up --build ocr-server` |
| **Run tests** | `docker-compose run --rm ocr-tests` |
| **Shell access** | `docker-compose exec ocr-server bash` |
| **Health check** | `curl http://localhost:3000/health` |

## Using Makefile (Optional)

If you have `make` installed:

```bash
make up        # Start server
make test      # Run tests
make test-cov  # Tests with coverage
make logs      # View logs
make down      # Stop server
make shell     # Access container shell
```

## API Examples

### Health Check
```bash
curl http://localhost:3000/health
```

### Training
```bash
curl -X POST http://localhost:3000/ \
  -H "Content-Type: application/json" \
  -d '{
    "train": true,
    "trainArray": [
      {"y0": [0.5, ...], "label": 5}
    ]
  }'
```

### Prediction
```bash
curl -X POST http://localhost:3000/ \
  -H "Content-Type: application/json" \
  -d '{
    "predict": true,
    "image": [0.5, 0.3, ...]
  }'
```

### Optimization (Find Optimal Hidden Nodes)
```bash
curl -X POST http://localhost:3000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "trainingData": [{"y0": [...], "label": 0}, ...],
    "testData": [{"y0": [...], "label": 1}, ...],
    "minNodes": 5,
    "maxNodes": 50,
    "step": 5
  }'
```

## Troubleshooting

### Port in use?
```bash
docker-compose down
# Or change port:
PORT=5000 docker-compose up ocr-server
```

### Clean everything
```bash
docker-compose down -v
docker system prune -a
```

### Container won't start?
```bash
docker-compose logs ocr-server
docker-compose up ocr-server  # Run without -d to see output
```

## No Docker? No Problem!

If you prefer traditional setup:

### Server (Python)
```bash
# Install dependencies
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run server
cd src
python server.py

# Run tests
pytest
```

### Client (JavaScript)
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test
```

## Files Overview

```
server/
├── Dockerfile              # Server container (Python 3.13)
├── Dockerfile.test         # Test container (Python 3.13)
├── docker-compose.yml      # Orchestration
├── .dockerignore          # Exclude from builds
├── Makefile               # Convenience commands
├── requirements.txt        # Python packages
├── src/                   # Application code
└── test/                  # Test suite
```

---

**Need help?** Check the [full README](README.md) or run `make help`
