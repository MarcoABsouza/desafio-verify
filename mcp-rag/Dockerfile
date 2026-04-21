FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY pyproject.toml uv.lock* ./
RUN uv pip install --system mcp

COPY mcp-rag/ ./mcp-rag/

EXPOSE 8002
CMD ["python", "mcp-rag/main.py"]