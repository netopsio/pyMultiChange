.PHONY: help install test lint format clean build

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run all linters"
	@echo "  make format     - Format code with ruff"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make build      - Build package"

install:
	poetry install

test:
	poetry run pytest

test-cov:
	poetry run pytest --cov=pymultichange --cov-report=html --cov-report=term

lint:
	poetry run ruff check .
	poetry run pylint pymultichange
	poetry run mypy pymultichange

format:
	poetry run ruff format .
	poetry run ruff check --fix .

clean:
	rm -rf build dist .eggs *.egg-info
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build:
	poetry build

all: lint test
