import time
import unittest
from fastapi.testclient import TestClient

from main import app
from tests.utils import initialize_database_for_test, remove_test_consequences
from tests.data import TagsData


client = TestClient(app)


class TestTags(unittest.TestCase):
    def test_list_tags(self):
        tags = TagsData.data
        response = client.get('/api/tags/')

        for tag in tags:
            self.assertIn(tag['name'], [db_attr['name'] for db_attr in response.json()])

    def test_read_tag(self):
        tags = TagsData.data
        tag = tags[1]
        response = client.get(f'/api/tags/{tag["id"]}/')
        self.assertEqual(tag['name'], response.json()['name'])

    def test_create_tag(self):
        tag = {
            'name': 'Tag-test-create',
            'attrs': [
                {
                    'name': 'att1',
                },
                {
                    'name': 'new-att'
                }
            ]
        }
        response = client.post('/api/tags/', json=tag)
        self.assertEqual(tag['name'], response.json()['name'])
        attrs = [name for name in tag['attrs']]
        for attr in attrs:
            self.assertIn(attr['name'], [attr_db['name'] for attr_db in response.json()['attrs']])
        self.assertIn('id', response.json())

    def test_delete_attribute(self):
        tags = TagsData.data
        tag = tags[1]
        response_delete = client.delete(f'/api/attributes/{tag["id"]}/')
        response_get = client.get(f'/api/attributes/{tag["id"]}/')
        self.assertEqual(204, response_delete.status_code)
        self.assertEqual(404, response_get.status_code)
