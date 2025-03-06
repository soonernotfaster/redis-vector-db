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


def download_data() -> list[dict]:
    URL = (
        "https://raw.githubusercontent.com/bsbodden/redis_vss_getting_started"
        "/main/data/bikes.json"
    )

    response = requests.get(URL, timeout=10)
    return response.json()


def seed_redis(data: list[dict]) -> None:
    client = redis.Redis(host="localhost",
                         port=6379, decode_responses=True)
    print(client)
    client.set("test", "secret-foo")
    # print(client.get("test"))
    # pipe = client.pipeline()
    # for i, bike in enumerate(data, start=1):
    #     redis_key = f"bikes:{i:03}"
    #     pipe.json().set(redis_key, "$", bike)
    # res = pipe.execute()

    # print(res)


def main() -> None:
    data = download_data()
    seed_redis(data)
    # print(client)


if __name__ == "__main__":
    main()
