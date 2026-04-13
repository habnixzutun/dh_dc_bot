# Dockerfile

# Verwende ein schlankes Python 3.9 Image als Basis
FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --no-dev --no-install-project

# Kopiere alle restlichen Dateien deines Projekts in das Arbeitsverzeichnis
COPY . .

# Definiere den Befehl, der beim Start des Containers ausgeführt wird
CMD ["uv", "run", "bot.py"]