from uuid import uuid4

from db import ClusterHolder
from core.config import PRODUCTS_BUCKET
from models.product import ProductDB, BrandDB
from . import upsert, get, get_all, filter_query
from .utils import output_pydantic_model
from .brands import create_brand


def create_product(product):
    bucket = ClusterHolder.cluster.bucket(PRODUCTS_BUCKET)
    brand = create_brand(product.brand)
    product.brand = brand
    result_product = upsert(bucket, product, key=str(uuid4()))
    return result_product


def get_product(uuid):
    bucket = ClusterHolder.cluster.bucket(PRODUCTS_BUCKET)
    return get(bucket, uuid)


@output_pydantic_model(model=ProductDB)
def get_all_products():
    bucket = ClusterHolder.cluster.bucket(PRODUCTS_BUCKET)
    return get_all(bucket)


def get_product_by_name(name):
    bucket = ClusterHolder.cluster.bucket(PRODUCTS_BUCKET)
    return [item['product'] for item in filter_query(bucket, name=name)]


def get_brand_by_name(name):
    pass


def get_brand_by_uuid(uuid):
    pass
