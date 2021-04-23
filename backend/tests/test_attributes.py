import time
from fastapi.testclient import TestClient

from main import app
from db import initialize_cluster, initialize_buckets, ClusterHolder
from db.buckets import Buckets
from core.config import ATTRIBUTE_BUCKET
from services import get, upsert
from tests import flush_db


client = TestClient(app)

cluster = initialize_cluster()
ClusterHolder.cluster = cluster
initialize_buckets()


attributes = [
    {
        'name': 'Attr1'
    },
    {
        'name': 'Attr2'
    },
    {
        'name': 'Attr3'
    },
    {
        'name': 'Attr4'
    },
    {
        'name': 'Attr5'
    }
]


def create_attribute(attr):
    bucket = Buckets.get_bucket(ATTRIBUTE_BUCKET)
    db_attr = upsert(bucket, attr)
    attr['id'] = db_attr['id']
    return attr


def test_list_attributes():
    for attr in attributes:
        create_attribute(attr)
        time.sleep(1)
    response = client.get('/api/attributes/')
    for attr in attributes:
        assert attr['name'] in [db_attr['name'] for db_attr in response.json()]
    flush_db()


def test_read_attribute():
    attr = create_attribute(attributes[0])
    time.sleep(1)
    response = client.get(f'/api/attributes/{attr["id"]}/')
    assert attr['name'] == response.json()['name']
    flush_db()


def test_create_attribute():
    attr = attributes[0]
    response = client.post('/api/attributes/', json=attr)
    assert attr['name'] == response.json()['name']
    assert 'id' in response.json()
    flush_db()


def test_create_existing_attribute():
    attr = attributes[0]
    client.post('/api/attributes/', json=attr)
    response = client.post('/api/attributes/', json=attr)
    assert 400 == response.status_code
    flush_db()


def test_delete_attribute():
    attr = create_attribute(attributes[0])
    time.sleep(1)
    response_delete = client.delete(f'/api/attributes/{attr["id"]}/')
    response_get = client.get(f'/api/attributes/{attr["id"]}/')
    assert 204 == response_delete.status_code
    assert 404 == response_get.status_code
    flush_db()
