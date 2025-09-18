FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD . /app/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

# -----------------------
FROM base AS prod

ENTRYPOINT ["/entrypoint.sh"]

CMD fastapi run --host 0.0.0.0 --port 8000 "$API_PATH"

FROM base AS dev

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --dev

ENTRYPOINT ["/entrypoint.sh"]

CMD fastapi dev --host 0.0.0.0 --port 8000 --reload "$API_PATH"