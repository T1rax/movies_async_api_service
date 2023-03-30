#!/usr/bin/env bash

set -e

python3 utils/wait_for_services.py

pytest src