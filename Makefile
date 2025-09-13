.PHONY: run install help setup clean test

# Default target
help:
	@echo "Available commands:"
	@echo "  make setup    - Create virtual environment and install dependencies"
	@echo "  make install  - Install required dependencies (requires venv)"
	@echo "  make run      - Run the FastAPI server (no reload)"
	@echo "  make run-dev  - Run the FastAPI server with auto-reload (recommended)"
	@echo "  make test     - Run tests"
	@echo "  make clean    - Remove virtual environment"
	@echo "  make help     - Show this help message"

# Setup virtual environment and install dependencies
setup:
	python3 -m venv venv
	@echo "Virtual environment created. Run 'source venv/bin/activate' to activate it."
	@echo "Then run 'make install' to install dependencies."

# Install dependencies (requires activated virtual environment)
install:
	pip3 install -r backend/requirements.txt

# Run the server (requires activated virtual environment)
run:
	cd backend && python3 main.py

# Run with auto-reload (recommended for development)
run-dev:
	cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run tests
test:
	python3 -m pytest

# Clean up virtual environment
clean:
	rm -rf venv
