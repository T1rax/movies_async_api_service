#!/usr/bin/env bash

set -e

gunicorn main:app --bind 0.0.0.0:8000 --workers 3 --worker-class uvicorn.workers.UvicornWorker --log-file=- --access-logfile=- --error-logfile=-