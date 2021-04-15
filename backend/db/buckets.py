from couchbase.exceptions import BucketNotFoundException

from db import ClusterHolder
from db.exceptions import BucketNotFound


class Buckets:
    __buckets = dict()

    def __init__(self, buckets_names: list):
        for bucket_name in buckets_names:
            self.__buckets[bucket_name] = ClusterHolder.cluster.bucket(bucket_name)

    @classmethod
    def get_bucket(cls, name):
        bucket = cls.__buckets.get(name)
        if not bucket:
            try:
                bucket = ClusterHolder.cluster.bucket(name)
            except BucketNotFoundException:
                raise BucketNotFound(name)
            cls.__buckets[name] = bucket
        return bucket
