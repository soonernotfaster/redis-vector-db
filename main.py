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


embedder = SentenceTransformer("msmarco-distilbert-base-v4")
VECTOR_DIMENSION = 768


def embed_descriptions() -> None:
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


def add_index():
    index_name = "idx:bikes_vss"
    try:
        client.ft(index_name).dropindex()
    except:
        pass

    pipe = client.pipeline()
    pipe.ft(index_name) \
        .create_index(
            (
                TextField("$.model", no_stem=True, as_name="model"),
                TextField("$.brand", no_stem=True, as_name="brand"),
                NumericField("$.price", as_name="price"),
                TagField("$.type", as_name="type"),
                TextField("$.description", as_name="description"),
                VectorField(
                    "$.description_embeddings",
                    "FLAT",
                    {
                        "TYPE": "FLOAT32",
                        "DIM": VECTOR_DIMENSION,
                        "DISTANCE_METRIC": "COSINE",
                    },
                    as_name="vector",
                ),
            ),
            definition=IndexDefinition(
                prefix=["bikes:"], index_type=IndexType.JSON),
    )
    res = pipe.execute()

    print(res)


def query():
    queries = [
        "Bike for small kids",
        "Best Mountain bikes for kids",
        "Cheap Mountain bike for kids",
        "Female specific mountain bike",
        "Road bike for beginners",
        "Commuter bike for people over 60",
        "Comfortable commuter bike",
        "Good bike for college students",
        "Mountain bike for beginners",
        "Vintage bike",
        "Comfortable city bike",
    ]

    def embed_it(desc):
        return embedder.encode(desc).astype(np.float32).tolist()

    query = (
        Query("*=>[KNN 3 @embedding $query_vector AS vector_distance]")
        .return_fields('score', 'id', 'brand', 'model', 'description')
        .dialect(2)
    )
    print("embedding", np.array(embed_it("bike for young at heart")))
    res = client.ft("idx:bikes_vss").search(
        query, {"query_vector": np.array(embed_it("Cheap Mountain bike for kids")).tobytes()}).docs
    print(res)


def main() -> None:
    data = download_data()
    seed_redis(data)
    embed_descriptions()
    res = client.json().get("bikes:010")
    print(res)
    add_index()
    query()


if __name__ == "__main__":
    main()
