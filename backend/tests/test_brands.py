import time
import unittest
from fastapi.testclient import TestClient

from main import app
from tests.utils import initialize_database_for_test, remove_test_consequences
from tests.data import BrandsData


client = TestClient(app=app)


class TestBrands(unittest.TestCase):
    def test_list_brands(self):
        response = client.get('/api/brands/')
        self.assertEqual(response.status_code, 200)

    def test_read_brand(self):
        brands = BrandsData.data
        brand = brands[1]
        response = client.get(f'/api/brands/{brand["id"]}/')
        self.assertEqual(brand['name'], response.json()['name'])

    def test_create_brand(self):
        brand = {
            'name': 'Brand-test-create'
        }
        response = client.post('/api/brands/', json=brand)
        self.assertEqual(brand['name'], response.json()['name'])
        self.assertIn('id', response.json())

    def test_create_existing_brand(self):
        brands = BrandsData.data
        brand = brands[0]
        response = client.post('/api/brands/', json=brand)
        self.assertEqual(400, response.status_code)

    def test_update_brand(self):
        brand = {
            'name': 'Brand-for-update',
        }
        response_post = client.post('/api/brands/', json=brand)
        brand_db = response_post.json()

        brand_upd = {
            'name': 'Brand-for-update_upd',
        }
        response_patch = client.patch(f'/api/brands/{brand_db["id"]}/', json=brand_upd)
        self.assertEqual(200, response_patch.status_code)
        self.assertNotEqual(brand_db['name'], response_patch.json()['name'])

    def test_delete_brand(self):
        brands = BrandsData.data
        brand = brands[0]
        response_delete = client.delete(f'/api/brands/{brand["id"]}/')
        response_get = client.get(f'/api/brands/{brand["id"]}/')
        self.assertEqual(204, response_delete.status_code)
        self.assertEqual(404, response_get.status_code)
