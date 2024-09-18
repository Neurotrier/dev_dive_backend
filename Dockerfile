FROM python:3.11-slim

WORKDIR /code

RUN pip install --no-cache-dir poetry

COPY ./pyproject.toml ./poetry.lock* /code/

RUN poetry install --no-root --no-dev

COPY . /code/

RUN chmod +x /code/start.sh