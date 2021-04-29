from couchbase import search

from db import ClusterHolder
from db.buckets import Buckets
from core.config import BUCKETS


async def fulltext_search(bucket, search_string='', skip=0, limit=30):
    cluster = ClusterHolder.cluster
    # creating a search string with every word wrapped in %word%
    search_string = ' '.join([f'%{string}%' for string in search_string.split(' ')])

    query_string = f'SELECT b.name FROM {bucket.name} AS b WHERE ANY suf IN SUFFIXES(LOWER())'
    query_results = cluster.query( + f' LIMIT {limit} OFFSET {}')

    query_string = search.QueryStringQuery(search_string)
    # results = ClusterHolder.cluster.search_query(index, query_string, limit=limit)
    r_list = []
    return r_list


async def flush_db():
    for bucket_name in BUCKETS:
        bucket = await Buckets.get_bucket(bucket_name)
        results = bucket.flush()
    return results
