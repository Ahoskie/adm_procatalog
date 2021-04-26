import time
from fastapi.testclient import TestClient

from main import app
from db import initialize_cluster, initialize_buckets, ClusterHolder
from models.tag import Tag
from db.buckets import Buckets
from core.config import TAGS_BUCKET, ATTRIBUTE_BUCKET
from services import get, upsert
from tests import flush_db


client = TestClient(app)

cluster = initialize_cluster()
ClusterHolder.cluster = cluster
initialize_buckets()


tags = [
    {
        'name': 'Tag1',
        'attrs': [
            {
                'name': 'att1'
            },
            {
                'name': 'att2'
            }
        ]
    },
    {
        'name': 'Tag2',
        'attrs': [
            {
                'name': 'att3'
            },
            {
                'name': 'att4'
            }
        ]
    },
    {
        'name': 'Tag3',
        'attrs': [
            {
                'name': 'att2'
            },
            {
                'name': 'att5'
            }
        ]
    },
    {
        'name': 'Tag4',
        'attrs': [
            {
                'name': 'att3'
            },
            {
                'name': 'att6'
            },
            {
                'name': 'att7'
            }
        ]
    },
]


def create_tag(tag):
    client.post('/api/tags/', json=tag)


def test_list_attributes():
    for tag in tags:
        create_tag(tag)
        time.sleep(1)
    response = client.get('/api/tags/')
    for tag in tags:
        assert tag.name in [db_attr['name'] for db_attr in response.json()]
    flush_db(client)


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
