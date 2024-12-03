FROM python:3.11-slim

WORKDIR /code

RUN pip install --no-cache-dir uv

COPY ./pyproject.toml ./uv.lock* /code/

RUN uv sync

COPY . /code/