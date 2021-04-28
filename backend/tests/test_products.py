import time
import unittest
from fastapi.testclient import TestClient

from main import app
from tests.data import ProductsData


client = TestClient(app=app)


class TestProducts(unittest.TestCase):
    def test_list_products(self):
        response = client.get('/api/products/')
        self.assertEqual(response.status_code, 200)

    def test_read_product(self):
        products = ProductsData.data
        product = products[1]
        response = client.get(f'/api/products/{product["id"]}/')
        self.assertEqual(product['name'], response.json()['name'])

    def test_create_product(self):
        product = {
            'name': 'Product-create-test',
            'brand': {
                'name': 'Brand1'
            },
            'tags': [],
            'variants': []
        }
        response = client.post('/api/products/', json=product)
        self.assertEqual(product['name'], response.json()['name'])
        self.assertIn('id', response.json())

    def test_create_existing_product(self):
        products = ProductsData.data
        product = products[0]
        response = client.post('/api/products/', json=product)
        self.assertEqual(400, response.status_code)

    def test_delete_product(self):
        products = ProductsData.data
        product = products[0]
        response_delete = client.delete(f'/api/products/{product["id"]}/')
        response_get = client.get(f'/api/products/{product["id"]}/')
        self.assertEqual(204, response_delete.status_code)
        self.assertEqual(404, response_get.status_code)
