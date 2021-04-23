import time

from db.buckets import Buckets
from core.config import BUCKETS


def flush_db():
    for bucket_name in BUCKETS:
        bucket = Buckets.get_bucket(bucket_name)
        bucket.flush()
    time.sleep(1)
