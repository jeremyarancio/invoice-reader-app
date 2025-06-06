# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
ADD . /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# DB migration
RUN chmod +x docker/entrypoint.sh
ENTRYPOINT ["/app/docker/entrypoint.sh"]

# Production stage
FROM base AS prod
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "src/invoice_reader/app/main.py"]

# Development stage
FROM base AS dev
# Install development dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --dev
# Use a development server with hot-reloading
CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8000", "src/invoice_reader/app/main.py"]