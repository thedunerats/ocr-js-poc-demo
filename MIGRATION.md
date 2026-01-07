# Migration Guide: From Batch Scripts to Docker

## What Changed?

### ❌ Removed
- `setup.bat` - No longer needed
- `run.bat` - Replaced by Docker
- `test.bat` - Replaced by Docker
- `pytest.ini` - Configuration moved to Docker
- `QUICKSTART.md` - Consolidated into README

### ✅ Added
- `Dockerfile` - Server container definition
- `Dockerfile.test` - Test container definition
- `docker-compose.yml` - Service orchestration
- `.dockerignore` - Exclude files from Docker builds
- `Makefile` - Optional convenience commands
- `.github/workflows/ci.yml` - CI/CD pipeline

### 📝 Updated
- `README.md` - Docker-focused documentation
- `.gitignore` - Docker-aware patterns

## Before (Batch Scripts)

```bash
# Setup
cd server
setup.bat

# Run server
run.bat

# Run tests
test.bat
```

## After (Docker)

```bash
# Setup (one-time)
cd server
docker-compose build

# Run server
docker-compose up -d ocr-server

# Run tests
docker-compose run --rm ocr-tests
```

## Command Mapping

| Old Batch Command | New Docker Command |
|-------------------|-------------------|
| `setup.bat` | `docker-compose build` |
| `run.bat` | `docker-compose up ocr-server` |
| `test.bat` | `docker-compose run --rm ocr-tests` |
| N/A | `docker-compose down` (stop server) |
| N/A | `docker-compose logs -f` (view logs) |

## Benefits of Docker

### Before (Batch Scripts)
- ❌ Required Python installation
- ❌ Virtual environment management
- ❌ Platform-specific (Windows only)
- ❌ Manual dependency installation
- ❌ Inconsistent environments
- ❌ No isolation between projects

### After (Docker)
- ✅ No Python installation needed
- ✅ No virtual environment needed
- ✅ Works on Windows, Mac, Linux
- ✅ Automatic dependency management
- ✅ Consistent environments everywhere
- ✅ Complete isolation
- ✅ Easy CI/CD integration
- ✅ Production-ready

## Migration Steps

### Step 1: Install Docker
1. Download Docker Desktop: https://www.docker.com/products/docker-desktop
2. Install and start Docker Desktop
3. Verify installation: `docker --version`

### Step 2: Remove Old Setup (if exists)
```bash
cd server

# Remove virtual environment (if it exists)
Remove-Item -Recurse -Force venv

# The .bat files are already removed
```

### Step 3: Build Docker Images
```bash
cd server
docker-compose build
```

### Step 4: Start Server
```bash
docker-compose up -d ocr-server
```

### Step 5: Verify
```bash
# Check server is running
curl http://localhost:3000/health

# Or in PowerShell:
Invoke-WebRequest http://localhost:3000/health
```

### Step 6: Run Tests
```bash
docker-compose run --rm ocr-tests
```

## Configuration Changes

### pytest.ini → Docker
Previously configured in `pytest.ini`, now built into Docker commands:

```bash
# Old: pytest.ini settings
[tool:pytest]
testpaths = test
addopts = -v --tb=short

# New: In Dockerfile.test and docker-compose.yml
CMD ["pytest", "-v", "--tb=short", "--disable-warnings"]
```

### Environment Variables

Set in `docker-compose.yml` or command line:

```bash
# Change port
PORT=5000 docker-compose up ocr-server

# Custom pytest args
PYTEST_ARGS="-v -k test_predict" docker-compose run --rm ocr-tests
```

## Troubleshooting

### Docker Not Found
```bash
# Install Docker Desktop
# https://www.docker.com/products/docker-desktop
```

### Port Already in Use
```bash
# Stop existing server
docker-compose down

# Or use different port
PORT=5000 docker-compose up ocr-server
```

### Permission Errors (Linux/Mac)
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

### Images Take Too Much Space
```bash
# Clean up old images
docker system prune -a
```

### Want to Go Back to Batch Scripts?
You can still use Python directly:

```bash
cd server

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Run server
cd src
python server.py

# Run tests (from server directory)
pytest
```

## CI/CD Integration

Docker makes CI/CD much easier. The project now includes:

### GitHub Actions (`.github/workflows/ci.yml`)
Automatically runs on every push:
1. Builds Docker images
2. Runs all tests
3. Generates coverage reports
4. Validates server health

### Running CI Locally
```bash
cd server

# Build test image
docker build -f Dockerfile.test -t ocr-server-test .

# Run tests like CI does
docker run --rm ocr-server-test pytest -v

# Build server image
docker build -t ocr-server:local .

# Test health check
docker run -d -p 3000:3000 --name test-server ocr-server:local
sleep 5
curl http://localhost:3000/health
docker stop test-server && docker rm test-server
```

## Summary

### What You Gain
- ✅ **Consistency**: Same environment everywhere
- ✅ **Simplicity**: No Python/venv management
- ✅ **Isolation**: Projects don't interfere
- ✅ **Portability**: Works on any OS
- ✅ **Production-Ready**: Deploy anywhere
- ✅ **CI/CD**: Automated testing

### What You Lose
- ❌ Direct file editing (still possible with volumes)
- ❌ Instant Python access (use `docker-compose exec`)

### Learning Curve
- **Easy**: Basic `docker-compose up/down`
- **Medium**: Understanding Docker concepts
- **Optional**: Advanced Docker features

## Next Steps

1. ✅ Read [DOCKER_GUIDE.md](../DOCKER_GUIDE.md) for quick commands
2. ✅ Check [server/README.md](../server/README.md) for full documentation
3. ✅ Try running the server and tests
4. ✅ Explore `docker-compose.yml` to understand the setup

## Questions?

- Docker basics: https://docs.docker.com/get-started/
- Docker Compose: https://docs.docker.com/compose/
- Project README: [server/README.md](../server/README.md)
