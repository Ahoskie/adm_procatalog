import asyncio

from db.utils import flush_db
from db import initialize_cluster, initialize_buckets, ClusterHolder
from tests.data import AttributesData, TagsData, BrandsData, ProductsData


def initialize_database_for_test():
    loop = asyncio.get_event_loop()

    async def prepare_database():
        ClusterHolder.cluster = await initialize_cluster()
        await initialize_buckets()

        for data_container in [AttributesData, TagsData, BrandsData, ProductsData]:
            await asyncio.sleep(5)
            await data_container.fill_database()

    loop.run_until_complete(prepare_database())


def remove_test_consequences():
    loop = asyncio.get_event_loop()

    async def teardown_database():
        await flush_db()
        await asyncio.sleep(3)
    loop.run_until_complete(teardown_database())
