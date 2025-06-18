# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

# Arguments for user/group IDs
ARG USER_ID=1000
ARG GROUP_ID=1000

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
ADD --chown=appuser:appuser . /app/
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Create user with matching IDs
RUN addgroup --gid $GROUP_ID appuser && \
    adduser --disabled-password --gecos '' --uid $USER_ID --gid $GROUP_ID appuser

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# DB migration
RUN chmod +x docker/entrypoint.sh
USER appuser
ENTRYPOINT ["/app/docker/entrypoint.sh"]

# Production stage
FROM base AS prod
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000", "src/invoice_reader/app/main.py"]

# Development stage
FROM base AS dev
# Install development dependencies
USER root
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --dev && \
    chown -R ${USER_ID}:${GROUP_ID} /app
USER appuser
# Use a development server with hot-reloading
CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8000", "src/invoice_reader/app/main.py"]