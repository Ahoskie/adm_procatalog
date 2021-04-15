from db import ClusterHolder
from core.config import TAGS_BUCKET
from . import upsert, get, get_all, filter_query
from models.tag import TagNoAttributes, TagDB

from .utils import output_pydantic_model, get_document_if_exists


@output_pydantic_model(model=TagDB)
def create_tag(tag):
    bucket = ClusterHolder.cluster.bucket(TAGS_BUCKET)
    documents = get_document_if_exists(bucket, tag)
    if documents:
        return
    return upsert(bucket, tag)


@output_pydantic_model(model=TagNoAttributes)
def get_or_create_tags(tags: list):
    bucket = ClusterHolder.cluster.bucket(TAGS_BUCKET)
    documents = get_document_if_exists(bucket, brand)
    if not documents:
        result_brand = upsert(bucket, brand)
    else:
        result_brand = documents[0]
    return result_brand
