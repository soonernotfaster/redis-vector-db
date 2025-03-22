# Redis as Vector Database 

This code is based off of Redis' [Vector Database Tutorial](https://redis.io/docs/latest/develop/get-started/vector-database/). I am using this as a spike to determine if Redis is the right tool for a site search and/or a data source for RAG.

## Developer setup

Use a devcontainer, but don't run it in the cloud. Run it locally in docker.

1. Run `uv sync` to verify installation of dependencies.
1. Start the Redis service using: `docker compose up -d`
1. Run the script with `uv run main.py`
