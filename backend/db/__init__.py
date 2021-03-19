import time
from couchbase.cluster import Cluster, ClusterOptions, PasswordAuthenticator
from couchbase.exceptions import BucketNotFoundException
from couchbase.management.buckets import CreateBucketSettings, CreateBucketOptions

from core.config import COUCHBASE_USER, COUCHBASE_PASSWORD, COUCHBASE_IP, BUCKETS


class ClusterHolder:
    cluster: Cluster = None


def initialize_cluster():
    max_tries = 5
    cluster = None
    for i in range(max_tries):
        try:
            cluster = Cluster(COUCHBASE_IP,
                              ClusterOptions(
                                  PasswordAuthenticator(COUCHBASE_USER, COUCHBASE_PASSWORD))
                              )
            return cluster
        except Exception:
            time.sleep(1)
    if not cluster:
        print('ERROR: Could not connect to the cluster.')


def initialize_buckets():
    cluster = ClusterHolder.cluster
    if cluster:
        for bucket_name in BUCKETS:
            try:
                bucket = cluster.bucket(bucket_name)
            except BucketNotFoundException:
                cluster.buckets().create_bucket(
                    CreateBucketSettings(name=bucket_name, ram_quota_mb=100, num_replicas=0),
                    CreateBucketOptions()
                )
                time.sleep(1)
                bucket = cluster.bucket(bucket_name)
                result = bucket.query(
                    f'CREATE PRIMARY INDEX `{bucket_name}_index` ON `{bucket_name}` USING GSI',
                )
                result.execute()
                result.fetch()
