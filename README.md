# Site Search

I wanted to show how to build both a RAG and Semantic search feature for my blog. This will utilize my experience at GitHub building AI and ML systems to aid customers in detecting their problems.


## Developer setup

Use a devcontainer, but don't run it in the cloud. Run it locally in docker.

1. Run `uv sync` to verify installation of dependencies.
1. Start the Redis service using: `docker compose up -d`
1. Run the script with `uv run main.py`
