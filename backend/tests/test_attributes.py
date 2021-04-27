import pytest
from fastapi.testclient import TestClient
import asyncio

from main import app
from models.attribute import Attribute
from services.attributes import create_attribute
from tests import initialize_database_for_test, flush_database


@pytest.fixture(scope="session", autouse=True)
def run_around_tests(request):
    initialize_database_for_test()
    flush_database()


client = TestClient(app)


def create_attribute_in_db(attr):
    loop = asyncio.get_event_loop()

    async def async_create_attribute():
        result = await create_attribute(attr)
        await asyncio.sleep(0.5)
        return result

    attr = loop.run_until_complete(async_create_attribute())
    return attr


def setup_module(module):
    attributes = [Attribute(**attr) for attr in AttributesData.attributes]
    db_attrs = []
    for attr in attributes:
        db_attrs.append(create_attribute_in_db(attr))
    AttributesData.attributes = db_attrs


def test_list_attributes():
    attributes = AttributesData.attributes
    response = client.get('/api/attributes/')
    for attr in attributes:
        assert attr['name'] in [db_attr['name'] for db_attr in response.json()]


def test_read_attribute():
    attributes = AttributesData.attributes
    attr = attributes[0]
    response = client.get(f'/api/attributes/{attr["id"]}/')
    assert attr['name'] == response.json()['name']


def test_create_attribute():
    attr = {
        'name': 'Attribute-test-create'
    }
    response = client.post('/api/attributes/', json=attr)
    assert attr['name'] == response.json()['name']
    assert 'id' in response.json()


def test_create_existing_attribute():
    attributes = AttributesData.attributes
    attr = attributes[0]
    response = client.post('/api/attributes/', json=attr)
    assert 400 == response.status_code


def test_delete_attribute():
    attributes = AttributesData.attributes
    attr = attributes[0]
    response_delete = client.delete(f'/api/attributes/{attr["id"]}/')
    response_get = client.get(f'/api/attributes/{attr["id"]}/')
    assert 204 == response_delete.status_code
    assert 404 == response_get.status_code
