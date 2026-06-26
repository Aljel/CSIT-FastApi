#!/bin/sh

SCRIPT_DIR=$(dirname "$0")
alembic stamp head 2>/dev/null || true
alembic upgrade head
python "${SCRIPT_DIR}/main.py"
