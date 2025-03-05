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

client = redis.Redis(host="localhost", port=6379, decode_responses=True)


def main() -> None:
    print(client)


if __name__ == "__main__":
    main()
