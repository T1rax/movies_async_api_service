#!/usr/bin/env bash

set -e

gunicorn main:app -b 0.0.0.0:8000 -w 3 -k uvicorn.workers.UvicornWorker