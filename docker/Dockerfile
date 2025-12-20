FROM python:3.13.11-slim-bookworm

# UV_PROJECT_ENVIRONMENT=/usr/local - установка зависимостей в глобаное окружение
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/usr/local

RUN python -m pip install -U pip &&  \
    python -m pip install uv

WORKDIR /project

COPY ./pyproject.toml ./uv.lock ./

RUN uv sync

COPY ./ ./
