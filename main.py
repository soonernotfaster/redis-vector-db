import json
import time

import numpy as np
import pandas as pd
import requests
import redis
from redis.commands.search.field import (
    NumericField,
    TagField,
    TextField,
    VectorField
)
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from sentence_transformers import SentenceTransformer

client = redis.Redis(host="localhost",
                     port=6379, decode_responses=True)


def download_data() -> list[dict]:
    URL = (
        "https://raw.githubusercontent.com/bsbodden/redis_vss_getting_started"
        "/main/data/bikes.json"
    )

    response = requests.get(URL, timeout=10)
    return response.json()


def embed_descriptions() -> None:
    embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    # Sorting keys can improve performance with pipelining
    keys = sorted(client.keys("bikes:*"))

    descriptions = [item for sublist in client.json().mget(
        keys, "$.description") for item in sublist]

    def embed_it(desc):
        return embedder.encode(desc).astype(np.float32).tolist()

    embeddings = [embed_it(desc) for desc in descriptions]

    pipe = client.pipeline()
    for key, embedding in zip(keys, embeddings):
        pipe.json().set(key, "$.description_embedding", embedding)
    pipe.execute()


def seed_redis(data: list[dict]) -> None:
    print("data seeding")
    pipe = client.pipeline()
    for i, bike in enumerate(data, start=1):
        redis_key = f"bikes:{i:03}"
        print("key", redis_key)
        pipe.json().set(redis_key, "$", bike)
    res = pipe.execute()
    print(res)


def main() -> None:
    # data = download_data()
    # seed_redis(data)
    embed_descriptions()
    res = client.json().get("bikes:010")
    print(res)


if __name__ == "__main__":
    main()
