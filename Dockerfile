FROM node:22-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend/ .
RUN npm run build

# 2) Install Python deps with uv (no project code yet for better caching)
FROM python:3.12-slim AS backend
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# psycopg2-binary needs libpq at runtime
RUN apt-get update \
 && apt-get install -y --no-install-recommends libpq5 curl ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# RUN pip install --no-cache-dir uv

WORKDIR /app/Backend
# COPY Backend/pyproject.toml Backend/uv.lock ./
COPY Backend/requirements.txt ./
# RUN uv sync --frozen --no-dev



# 3) Copy backend source and baked frontend assets
COPY Backend/ .
COPY --from=frontend-builder /app/frontend/dist ../frontend/dist

ENV PATH="/app/Backend/.venv/bin:${PATH}" \
    DJANGO_SETTINGS_MODULE=config.settings \
    PYTHONDONTWRITEBYTECODE=1 \
    SECRET_KEY=changeme \
    DEBUG=False

RUN pip install -r requirements.txt

# Collect static assets into STATIC_ROOT
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Run migrations then serve (adjust DB_* env vars at runtime). Respect $PORT for platforms like Render.
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:${PORT:-8000}"]
