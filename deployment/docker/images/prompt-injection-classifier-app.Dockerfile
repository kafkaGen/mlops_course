FROM python:3.11-slim-buster AS builder

ENV POETRY_VERSION=2.1.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir poetry==${POETRY_VERSION}

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root \
    && rm -rf ${POETRY_CACHE_DIR}

####################

FROM python:3.11-slim-buster AS runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    HYDRA_FULL_ERROR=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src /app/src

EXPOSE 8000

CMD fastapi run src/api/main.py --host 0.0.0.0 --port 8000