# Makefile for OCR Server Docker operations

.PHONY: help build up down logs test test-cov clean restart shell

help:
	@echo "OCR Server - Docker Commands"
	@echo "============================"
	@echo "make build       - Build Docker images"
	@echo "make up          - Start the server"
	@echo "make down        - Stop the server"
	@echo "make logs        - View server logs"
	@echo "make test        - Run all tests"
	@echo "make test-cov    - Run tests with coverage"
	@echo "make clean       - Clean up containers and images"
	@echo "make restart     - Restart the server"
	@echo "make shell       - Open shell in server container"

build:
	docker-compose build

up:
	docker-compose up -d ocr-server
	@echo "Server started at http://localhost:3000"
	@echo "Check health: curl http://localhost:3000/health"

down:
	docker-compose down

logs:
	docker-compose logs -f ocr-server

test:
	docker-compose run --rm ocr-tests

test-cov:
	docker-compose --profile test up ocr-tests-coverage
	@echo "Coverage report generated in htmlcov/index.html"

clean:
	docker-compose down -v
	docker rmi ocr-server ocr-server-test 2>/dev/null || true

restart: down up

shell:
	docker-compose exec ocr-server bash
