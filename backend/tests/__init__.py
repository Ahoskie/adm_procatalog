import asyncio
import pytest

from db.utils import flush_db
from db import initialize_cluster, initialize_buckets, ClusterHolder


def initialize_database_for_test():
    loop = asyncio.get_event_loop()
    ClusterHolder.cluster = loop.run_until_complete(initialize_cluster())
    loop.run_until_complete(initialize_buckets())


def flush_database():
    loop = asyncio.get_event_loop()

    async def async_flush_database():
        result = await flush_db()
        await asyncio.sleep(3)
        return result

    res = loop.run_until_complete(async_flush_database())
    return res


def fill_database():
    attributes = [Attribute(**attr) for attr in AttributesData.attributes]
    db_attrs = []
    for attr in attributes:
        db_attrs.append(create_attribute_in_db(attr))
    AttributesData.attributes = db_attrs
