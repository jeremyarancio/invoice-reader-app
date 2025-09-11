# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

# Arguments for user/group IDs - match your host
ARG USER_ID=1001
ARG GROUP_ID=1001

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install system dependencies (including poppler-utils for pdf2image)
RUN apt-get update \
    && apt-get install -y poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 1. First install dependencies as root (using root's cache)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# 2. Add source code
ADD . /app/

# 3. Complete installation
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# 4. Create user and fix permissions
RUN addgroup --gid $GROUP_ID appuser && \
    adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID appuser && \
    chown -R appuser:appuser /app

# 5. Set environment
ENV PATH="/app/.venv/bin:$PATH"

# 6. Prepare entrypoint
USER appuser
RUN alembic upgrade head

# Production stage
FROM base AS prod
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "src/invoice_reader/app/main.py"]

# Development stage
FROM base AS dev
# Install development dependencies as root
USER root
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --dev && \
    chown -R appuser:appuser /app
USER appuser
CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8000", "src/invoice_reader/app/main.py"]