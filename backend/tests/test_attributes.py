import pytest
from fastapi.testclient import TestClient
import asyncio
from httpx import AsyncClient

from main import app
from tests import initialize_database_for_test, teardown
from tests.data import AttributesData


@pytest.fixture(scope="session", autouse=True)
def run_around_tests(request):
    initialize_database_for_test()
    yield
    teardown()


client = TestClient(app)


@pytest.mark.asyncio
async def test_list_attributes():
    attributes = AttributesData.data
    async with AsyncClient(app=app, base_url='http://192.168.20.84:8000') as a_client:
        response = await a_client.get('/api/attributes/')
    print(response)
    print(attributes)
    for attr in attributes:
        assert attr['name'] in [db_attr['name'] for db_attr in response.json()]


def test_read_attribute():
    attributes = AttributesData.data
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
    attributes = AttributesData.data
    attr = attributes[0]
    response = client.post('/api/attributes/', json=attr)
    assert 400 == response.status_code


def test_delete_attribute():
    attributes = AttributesData.data
    attr = attributes[0]
    response_delete = client.delete(f'/api/attributes/{attr["id"]}/')
    response_get = client.get(f'/api/attributes/{attr["id"]}/')
    assert 204 == response_delete.status_code
    assert 404 == response_get.status_code
