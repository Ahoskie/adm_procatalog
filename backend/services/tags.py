from db.buckets import Buckets
from core.config import TAGS_BUCKET, ATTRIBUTE_BUCKET
from services import upsert, get, get_all, update, delete, filter_query
from services.utils import get_document_if_exists, get_or_create, get_or_bulk_create
from services.exceptions import DocumentAlreadyExists, DocumentNotFound
from models.tag import TagNoAttributes, TagDB


def create_tag(tag):
    bucket = Buckets.get_bucket(TAGS_BUCKET)
    tags = filter_query(bucket, name=tag.name)
    if tags:
        raise DocumentAlreadyExists(tag.name)
    tag.attrs = get_or_bulk_create(Buckets.get_bucket(ATTRIBUTE_BUCKET), tag.attrs)
    return upsert(bucket, tag)


def get_all_tags(skip=0, limit=0):
    bucket = Buckets.get_bucket(TAGS_BUCKET)
    documents = get_all(bucket, skip=skip, limit=limit)
    return documents


def get_tag_by_id(tag_id):
    bucket = Buckets.get_bucket(TAGS_BUCKET)
    document = get(bucket, tag_id)
    return document


def update_tag_by_id(tag_id, tag):
    bucket = Buckets.get_bucket(TAGS_BUCKET)
    tag.attrs = get_or_bulk_create(Buckets.get_bucket(ATTRIBUTE_BUCKET), tag.attrs)
    updated_tag = update(bucket, tag, tag_id)
    if not updated_tag:
        raise DocumentNotFound(tag_id)
    return updated_tag


def remove_tag_by_id(tag_id):
    bucket = Buckets.get_bucket(TAGS_BUCKET)
    return delete(bucket, tag_id)
