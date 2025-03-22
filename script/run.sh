#!/usr/bin/env bash

set -euxo pipefail

docker compose up -d
uv run main.py