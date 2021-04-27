import time
import asyncio
from fastapi.testclient import TestClient

from main import app
from tests.data import TagsData
from models.tag import Tag
from services.tags import create_tag


client = TestClient(app)


def create_tag_in_db(tag):
    loop = asyncio.get_event_loop()

    async def async_create_tag():
        result = await create_tag(tag)
        await asyncio.sleep(0.5)
        return result

    tag = loop.run_until_complete(async_create_tag())
    return tag


def test_list_tags():
    tags = TagsData.data
    response = client.get('/api/tags/')
    for tag in tags:
        assert tag['name'] in [db_attr['name'] for db_attr in response.json()]


# def test_read_attribute():
#     attr = create_attribute(attributes[0])
#     time.sleep(1)
#     response = client.get(f'/api/attributes/{attr["id"]}/')
#     assert attr['name'] == response.json()['name']
#     flush_db()
#
#
# def test_create_attribute():
#     attr = attributes[0]
#     response = client.post('/api/attributes/', json=attr)
#     assert attr['name'] == response.json()['name']
#     assert 'id' in response.json()
#     flush_db()
#
#
# def test_create_existing_attribute():
#     attr = attributes[0]
#     client.post('/api/attributes/', json=attr)
#     response = client.post('/api/attributes/', json=attr)
#     assert 400 == response.status_code
#     flush_db()
#
#
# def test_delete_attribute():
#     attr = create_attribute(attributes[0])
#     time.sleep(1)
#     response_delete = client.delete(f'/api/attributes/{attr["id"]}/')
#     response_get = client.get(f'/api/attributes/{attr["id"]}/')
#     assert 204 == response_delete.status_code
#     assert 404 == response_get.status_code
#     flush_db()
