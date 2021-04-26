import time
from couchbase.cluster import ClusterOptions, PasswordAuthenticator
from acouchbase.cluster import Cluster
from couchbase.exceptions import BucketNotFoundException, NetworkException
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
                              options=ClusterOptions(
                                  PasswordAuthenticator(COUCHBASE_USER, COUCHBASE_PASSWORD))
                              )
            return cluster
        except Exception:
            time.sleep(1)
    if not cluster:
        print('ERROR: Could not connect to the cluster.')


async def initialize_buckets():
    from db.buckets import Buckets
    cluster = ClusterHolder.cluster
    if cluster:
        for bucket_name in BUCKETS:
            try:
                max_tries = 5
                for i in range(max_tries):
                    try:
                        bucket = cluster.bucket(bucket_name)
                        break
                    except NetworkException:
                        time.sleep(0.5)
                await bucket.on_connect()
            except BucketNotFoundException:
                cluster.buckets().create_bucket(
                    CreateBucketSettings(name=bucket_name, ram_quota_mb=100, num_replicas=0),
                    CreateBucketOptions()
                )
                bucket = cluster.bucket(bucket_name)
                await bucket.on_connect()
            query_string = f'SELECT * FROM system:indexes WHERE name="{bucket_name}_index"'

            max_tries = 5
            for i in range(max_tries):
                try:
                    query_results = cluster.query(query_string)
                    indexes = [row async for row in query_results]
                    if not indexes:
                        result = cluster.query(
                            f'CREATE PRIMARY INDEX `{bucket_name}_index` ON `{bucket_name}` USING GSI',
                        )
                        await result.rows()
                    await Buckets.get_bucket(bucket_name)
                except Exception as e:
                    print(e)
                    time.sleep(1)
