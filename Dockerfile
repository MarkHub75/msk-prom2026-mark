# SafeWatch image (tech.md 3, slice 15): the frontend is built on node, the app runs on python.
FROM node:24-slim AS frontend
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.13.0 /uv /usr/local/bin/uv
WORKDIR /app
ENV UV_LINK_MODE=copy UV_COMPILE_BYTECODE=1 UV_PYTHON_DOWNLOADS=never PYTHONUNBUFFERED=1
COPY pyproject.toml uv.lock .python-version ./
RUN uv sync --locked --no-dev --no-install-project
COPY src ./src
COPY config ./config
COPY contract ./contract
COPY tools/linq ./tools/linq
COPY --from=frontend /app/frontend/dist ./frontend/dist
RUN uv sync --locked --no-dev
EXPOSE 8000
CMD ["uv", "run", "--no-sync", "safewatch", "serve", "--host", "0.0.0.0", "--port", "8000"]
