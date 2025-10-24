# TSDuck GUI Makefile

.PHONY: help install install-dev clean test run check-deps check-tsduck

# Default target
help:
	@echo "TSDuck GUI - Available targets:"
	@echo "  install      - Install the application"
	@echo "  install-dev  - Install with development dependencies"
	@echo "  clean        - Clean build artifacts"
	@echo "  test         - Run tests"
	@echo "  run          - Run the application"
	@echo "  check-deps   - Check dependencies"
	@echo "  check-tsduck - Check TSDuck installation"
	@echo "  build        - Build the application"
	@echo "  dist         - Create distribution package"

# Installation
install:
	pip install -r requirements.txt
	python setup.py install

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"

# Clean
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

# Testing
test:
	python -m pytest tests/ -v

# Run application
run:
	python3 launch.py

# Check dependencies
check-deps:
	python -c "import sys; print(f'Python version: {sys.version}')"
	python -c "import PyQt6; print('PyQt6: OK')"
	python -c "import numpy; print('NumPy: OK')"
	python -c "import matplotlib; print('Matplotlib: OK')"
	python -c "import psutil; print('psutil: OK')"
	python -c "import requests; print('requests: OK')"
	python -c "import pyqtgraph; print('pyqtgraph: OK')"
	python -c "import qdarkstyle; print('qdarkstyle: OK')"

# Check TSDuck
check-tsduck:
	@echo "Checking TSDuck installation..."
	@which tsp > /dev/null && echo "TSDuck found: $$(tsp --version)" || echo "TSDuck not found"
	@python -c "try: import tsduck; print('TSDuck Python bindings: OK'); except ImportError: print('TSDuck Python bindings: Not available')"

# Build
build: clean
	python setup.py build

# Distribution
dist: clean
	python setup.py sdist bdist_wheel

# Development setup
dev-setup: install-dev
	@echo "Development environment setup complete"
	@echo "Run 'make run' to start the application"

# Full check
check: check-deps check-tsduck
	@echo "All checks completed"

# Quick start
quick-start: check-tsduck
	@echo "Starting TSDuck GUI..."
	python3 tsduck_gui.py

# Docker support (if needed)
docker-build:
	docker build -t tsduck-gui .

docker-run:
	docker run -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$$DISPLAY tsduck-gui

# Platform-specific targets
install-macos:
	brew install tsduck
	make install

install-ubuntu:
	sudo apt-get update
	sudo apt-get install -y tsduck
	make install

install-windows:
	winget install tsduck
	make install

# Documentation
docs:
	@echo "Generating documentation..."
	@echo "See README.md for detailed documentation"

# Linting
lint:
	flake8 tsduck_gui.py tsduck_backend.py stream_monitor.py
	black --check tsduck_gui.py tsduck_backend.py stream_monitor.py
	mypy tsduck_gui.py tsduck_backend.py stream_monitor.py

# Format code
format:
	black tsduck_gui.py tsduck_backend.py stream_monitor.py

# Security check
security:
	bandit -r tsduck_gui.py tsduck_backend.py stream_monitor.py

# All checks
all-checks: check lint security test
	@echo "All checks completed successfully"
