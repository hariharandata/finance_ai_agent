# Makefile for Cookiecutter-based Python Project

# Customize these variables
TEMPLATE_DIR := .
OUTPUT_DIR := generated-project
PROJECT_NAME := my_project

# Create a new project from cookiecutter template
cookiecutter:
	cookiecutter $(TEMPLATE_DIR) --output-dir $(OUTPUT_DIR)

# Run Ruff linting
lint:
	ruff check src tests

# Auto-fix lint issues
lint-fix:
	ruff check src tests --fix

# Format code with Black
format:
	black src tests

# Run tests
test:
	pytest tests

# Build Docker image (if Dockerfile present)
docker-build:
	docker build -t $(PROJECT_NAME):latest .

# Run Docker container
docker-run:
	docker run --rm -it $(PROJECT_NAME):latest

# Remove generated project
clean:
	rm -rf $(OUTPUT_DIR)

.PHONY: cookiecutter lint lint-fix format test docker-build docker-run clean