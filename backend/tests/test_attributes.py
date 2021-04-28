import time
import unittest
from fastapi.testclient import TestClient

from main import app
from tests.utils import initialize_database_for_test, remove_test_consequences
from tests.data import AttributesData


client = TestClient(app=app)


class TestAttributes(unittest.TestCase):
    def test_list_attributes(self):
        response = client.get('/api/attributes/')
        self.assertEqual(response.status_code, 200)

    def test_read_attribute(self):
        attributes = AttributesData.data
        attr = attributes[1]
        response = client.get(f'/api/attributes/{attr["id"]}/')
        self.assertEqual(attr['name'], response.json()['name'])

    def test_create_attribute(self):
        attr = {
            'name': 'Attribute-test-create'
        }
        response = client.post('/api/attributes/', json=attr)
        self.assertEqual(attr['name'], response.json()['name'])
        self.assertIn('id', response.json())

    def test_create_existing_attribute(self):
        attributes = AttributesData.data
        attr = attributes[0]
        response = client.post('/api/attributes/', json=attr)
        self.assertEqual(400, response.status_code)

    def test_update_attribute(self):
        attr = {
            'name': 'Attribute-for-update',
        }
        response_post = client.post('/api/attributes/', json=attr)
        attr_db = response_post.json()

        attr_upd = {
            'name': 'Attribute-for-update_upd',
        }
        response_patch = client.patch(f'/api/attributes/{attr_db["id"]}/', json=attr_upd)
        self.assertEqual(200, response_patch.status_code)
        self.assertNotEqual(attr_db['name'], response_patch.json()['name'])

    def test_delete_attribute(self):
        attributes = AttributesData.data
        attr = attributes[0]
        response_delete = client.delete(f'/api/attributes/{attr["id"]}/')
        response_get = client.get(f'/api/attributes/{attr["id"]}/')
        self.assertEqual(204, response_delete.status_code)
        self.assertEqual(404, response_get.status_code)

