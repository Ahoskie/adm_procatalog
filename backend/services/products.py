from uuid import uuid4

from couchbase.exceptions import DocumentNotFoundException

from db.buckets import Buckets
from core.config import PRODUCTS_BUCKET, BRANDS_BUCKET, TAGS_BUCKET
from services import upsert, get, get_all, delete, custom_query, fulltext_in_bucket
from services.utils import get_or_create, get_document_if_exists
from services.exceptions import DocumentNotFound, InvalidVariantAttribute
from models.attribute import AttributeWithValueDB
from models.product import VariantDB
from models.tag import TagDBNoAttributes


def validate_product_variants(product_variants: list, tags: list):
    tags_names = [tag['name'] for tag in tags]

    tags_attrs = custom_query(
        Buckets.get_bucket(TAGS_BUCKET),
        query_string=f'SELECT ARRAY_FLATTEN(ARRAY_AGG(t.attrs), 1) FROM tag AS t WHERE t.name IN {tags_names}'
    )[0]['$1']
    tags_attrs = tags_attrs if tags_attrs else []
    available_attrs = dict()
    for attr in tags_attrs:
        available_attrs[attr['name']] = attr

    variants_from_db = list()
    for variant in product_variants:
        attrs_from_db = list()
        for variant_attr in variant.attributes_values:
            if variant_attr.name not in available_attrs:
                raise InvalidVariantAttribute(variant_attr.name, available_attrs=tags_attrs)
            attr_id = available_attrs[variant_attr.name]['id']
            attr_from_db = AttributeWithValueDB(id=attr_id, **variant_attr.dict())
            attrs_from_db.append(attr_from_db)
        variant_from_db = VariantDB(id=str(uuid4()), attributes_values=attrs_from_db)
        variants_from_db.append(variant_from_db)
    return variants_from_db


def get_validated_product(product):
    brand = get_or_create(Buckets.get_bucket(BRANDS_BUCKET), product.brand)
    product.brand = brand

    tags = list()
    for tag in product.tags:
        db_tag = get_document_if_exists(Buckets.get_bucket(TAGS_BUCKET), tag)
        if not db_tag:
            raise DocumentNotFound(tag.name)
        tags.append(TagDBNoAttributes(**db_tag).dict())
    product.tags = tags

    if product.variants:
        product.variants = validate_product_variants(product.variants, tags)
    return product


def create_product(product):
    bucket = Buckets.get_bucket(PRODUCTS_BUCKET)
    product = get_validated_product(product)
    result_product = upsert(bucket, product, key=str(uuid4()))
    return result_product


def get_all_products(skip=0, limit=30):
    bucket = Buckets.get_bucket(PRODUCTS_BUCKET)
    return get_all(bucket, skip=skip, limit=limit)


def get_product_by_uuid(uuid):
    bucket = Buckets.get_bucket(PRODUCTS_BUCKET)
    try:
        product = get(bucket, uuid)
    except DocumentNotFoundException:
        raise DocumentNotFound(uuid)
    return product


def update_product_by_uuid(uuid, product):
    bucket = Buckets.get_bucket(PRODUCTS_BUCKET)
    product = get_validated_product(product)
    result_product = upsert(bucket, product, str(uuid))
    return result_product


def remove_product_by_uuid(uuid):
    bucket = Buckets.get_bucket(PRODUCTS_BUCKET)
    try:
        return delete(bucket, uuid)
    except DocumentNotFoundException:
        raise DocumentNotFound(uuid)


def fulltext_find_product(limit=30, search_string=''):
    bucket = Buckets.get_bucket(PRODUCTS_BUCKET)
    return fulltext_in_bucket(bucket, limit=limit, search_string=search_string)
