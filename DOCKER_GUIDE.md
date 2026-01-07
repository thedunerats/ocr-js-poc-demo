# 🐳 Docker Quick Reference

## Starting the Server

```bash
cd server
docker-compose up -d ocr-server
```

Server runs at: **http://localhost:3000**

## Running Tests

```bash
# All tests
docker-compose run --rm ocr-tests

# With coverage
docker-compose --profile test up ocr-tests-coverage

# Specific test
docker-compose run --rm ocr-tests pytest test/test_ocr.py -v
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

## Files Overview

```
server/
├── Dockerfile              # Server container
├── Dockerfile.test         # Test container
├── docker-compose.yml      # Orchestration
├── .dockerignore          # Exclude from builds
├── Makefile               # Convenience commands
├── requirements.txt        # Python packages
├── src/                   # Application code
└── test/                  # Test suite
```

---

**Need help?** Check the [full README](README.md) or run `make help`
