#!/bin/bash

uv run celery -A src.workers.celeryconfig worker --loglevel=info --pool=gevent --concurrency=4 -Q notification -n worker2 &
uv run celery -A src.workers.celeryconfig worker --loglevel=info --pool=gevent --concurrency=2 -n worker1 &
uv run celery -A src.workers.celeryconfig beat --loglevel=info


