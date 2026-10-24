# syntax=docker/dockerfile:1
# Argus: build the final frontend, then serve it from the Python backend.
FROM node:24-slim AS frontend
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN --mount=type=cache,target=/root/.npm npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.13.0 /uv /usr/local/bin/uv
WORKDIR /app
ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1 UV_PYTHON_DOWNLOADS=never PYTHONUNBUFFERED=1
ENV SAFEWATCH_FAKE=1 INFERENCE_BACKEND=linq
COPY pyproject.toml uv.lock .python-version ./
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --no-dev --no-install-project
COPY src ./src
COPY config ./config
COPY contract ./contract
COPY tools/linq ./tools/linq
COPY --from=frontend /app/frontend/dist ./frontend/dist
RUN --mount=type=cache,target=/root/.cache/uv uv sync --locked --no-dev
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=6 \
    CMD ["/app/.venv/bin/python", "-c", "import urllib.request; r = urllib.request.urlopen('http://127.0.0.1:8000/api/health', timeout=3); assert r.status == 200"]
CMD ["uv", "run", "--no-sync", "safewatch", "serve", "--host", "0.0.0.0", "--port", "8000", "--seed"]
