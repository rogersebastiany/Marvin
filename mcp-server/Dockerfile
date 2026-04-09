FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

COPY server.py web_to_docs_server.py prompt_engineer_server.py system_design_server.py ./
COPY docs/ ./docs/
COPY diagrams/ ./diagrams/

ENV PYTHONUNBUFFERED=1

# Default: docs server. Override via docker-compose command/env.
ENV MCP_SERVER=server.py
CMD ["sh", "-c", "uv run python $MCP_SERVER"]
