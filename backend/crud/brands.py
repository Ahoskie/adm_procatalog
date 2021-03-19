from uuid import uuid4

from db import ClusterHolder
from core.config import BRANDS_BUCKET
from . import upsert, get, get_all, filter_query
from models.product import ProductDB, BrandDB

from .utils import output_pydantic_model, get_document_if_exists


@output_pydantic_model(model=BrandDB)
def create_brand(brand):
    bucket = ClusterHolder.cluster.bucket(BRANDS_BUCKET)
    documents = get_document_if_exists(bucket, brand)
    if not documents:
        result_brand = upsert(bucket, brand)
    else:
        result_brand = documents[0]
    return result_brand
