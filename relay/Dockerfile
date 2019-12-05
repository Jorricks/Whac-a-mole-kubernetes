FROM python:3.7-alpine AS builder
WORKDIR /app
COPY requirements.txt .

ARG BUILD_DEPS="build-base gcc"

RUN apk add --no-cache --virtual .build-deps ${BUILD_DEPS} \
&& python3 -m venv .venv \
&& .venv/bin/pip install --no-cache-dir -U pip -r requirements.txt \
&& apk del .build-deps

COPY . /app

RUN .venv/bin/pip install --no-cache-dir -U pip ".[dev]" \
&& . .venv/bin/activate \
&& mypy src/molerelay --ignore-missing-imports \
&& flake8 --max-line-length=100 src/molerelay \
&& .venv/bin/pip install --no-cache-dir -U pip .

FROM python:3.7-alpine

WORKDIR /app

RUN apk add bash wget

COPY --from=builder /app /app

ENV PATH ="/app/.venv/bin:$PATH"

EXPOSE 8080

CMD . .venv/bin/activate && molerelay start --port 8080



