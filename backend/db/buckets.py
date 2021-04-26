from couchbase.exceptions import BucketNotFoundException, DocumentUnretrievableException
from couchbase.management.buckets import CreateBucketSettings, CreateBucketOptions

from db import ClusterHolder
from db.exceptions import BucketNotFound


class Buckets:
    __buckets = dict()

    @classmethod
    async def get_bucket(cls, name):
        bucket = cls.__buckets.get(name)
        if not bucket:
            try:
                bucket = ClusterHolder.cluster.bucket(name)
                await bucket.on_connect()
            except DocumentUnretrievableException:
                ClusterHolder.cluster.buckets().create_bucket(
                    CreateBucketSettings(name=name, ram_quota_mb=100, num_replicas=0),
                    CreateBucketOptions()
                )
                bucket = ClusterHolder.cluster.bucket(name)
                bucket.on_connect()
            cls.__buckets[name] = bucket
        return bucket
