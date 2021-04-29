from couchbase import search

from db import ClusterHolder
from db.buckets import Buckets
from core.config import BUCKETS


async def flush_db():
    for bucket_name in BUCKETS:
        bucket = await Buckets.get_bucket(bucket_name)
        results = bucket.flush()
    return results
