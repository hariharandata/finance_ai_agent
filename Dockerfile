FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml ruff.toml ./
COPY src ./src
COPY tests ./tests

RUN pip install --upgrade pip && pip install ruff black pytest

CMD ["python", "src/main.py"]