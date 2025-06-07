# Makefile for Python AI Agent Project

# Customize these variables
TEMPLATE_DIR := .
OUTPUT_DIR := generated-project
PROJECT_NAME := my_project
VENV_DIR := $(HOME)/.venvs/aienv
PYTHON := $(VENV_DIR)/bin/python
PIP := $(VENV_DIR)/bin/pip

# Create a new project from cookiecutter template
cookiecutter:
	cookiecutter $(TEMPLATE_DIR) --output-dir $(OUTPUT_DIR)

# Set up virtual environment and install required tools
install: $(VENV_DIR)/bin/activate

$(VENV_DIR)/bin/activate:
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "🛠️ Creating virtual environment at $(VENV_DIR)"; \
		python3 -m venv $(VENV_DIR); \
	fi
	@echo "📦 Installing required dependencies: phidata, yfinance, openai, groq"
	@$(PIP) install --upgrade pip
	@$(PIP) install phidata yfinance openai groq duckduckgo-search 'fastapi[standard]' sqlalchemy
	@echo "📦 Installing dev tools: ruff, black, pytest"
	@$(PIP) install black ruff pytest

# Run Ruff linting
lint:
	$(VENV_DIR)/bin/ruff check

# Auto-fix lint issues
lint-fix:
	$(VENV_DIR)/bin/ruff check --fix

# Format code with Black
format:
	$(VENV_DIR)/bin/black src tests

# Run tests
test:
	$(VENV_DIR)/bin/pytest tests

# Build Docker image
docker-build:
	docker build -t $(PROJECT_NAME):latest .

# Run Docker container
docker-run:
	docker run --rm -it $(PROJECT_NAME):latest

# Clean up
clean:
	rm -rf $(OUTPUT_DIR)

single_agent:
	$(PYTHON) src/ai_agent_project/single_agent.py

two_agents:
	$(PYTHON) src/ai_agent_project/two_agents.py

.PHONY: cookiecutter install lint lint-fix format test docker-build docker-run clean