from couchbase import search

from db import ClusterHolder
from db.buckets import Buckets
from core.config import BUCKETS


def fulltext_search(index, limit=30, search_string=''):
    query_string = search.QueryStringQuery(search_string)
    results = ClusterHolder.cluster.search_query(index, query_string, limit=limit)
    r_list = []
    for r in results:
        r_list.append(r)
    return r_list


async def flush_db():
    for bucket_name in BUCKETS:
        bucket = await Buckets.get_bucket(bucket_name)
        await bucket.flush()
