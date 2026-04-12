FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY marvin_server.py ./
COPY backends/ ./backends/
COPY relation_types.json ./
COPY ../docs/ ./docs/
COPY ../diagrams/ ./diagrams/

ENV PYTHONUNBUFFERED=1

CMD ["uv", "run", "python", "marvin_server.py"]
