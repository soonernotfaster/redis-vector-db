# Redis as Vector Database 

This code is based off of Redis' [Vector Database Tutorial](https://redis.io/docs/latest/develop/get-started/vector-database/). I am using this as a spike to determine if Redis is the right tool for a site search and/or a data source for RAG.

## Developer setup

We will use a `devcontainer`, but to save you money I will walk you through running it locally using Docker.

This repo uses the [Scripts to Rule Them All](https://github.blog/engineering/scripts-to-rule-them-all/) pattern, where applicable.
This allows `uv` dependencies to instal on container start.

1. In VS Code install [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)
1. Clone the repo
1. Open the repo using the "Dev Containers: Open Folder in Container" command in VS Code
1. Run the code by executing `./script/run.sh`

N.B. On your first run, the script will need to download the embedding model
