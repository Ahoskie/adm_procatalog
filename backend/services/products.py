from uuid import uuid4

from couchbase.exceptions import DocumentNotFoundException

from db.buckets import Buckets
from db.exceptions import UniqueConstraintViolation
from core.config import PRODUCTS_BUCKET, BRANDS_BUCKET, TAGS_BUCKET
from services import upsert, get, get_all, delete, custom_query, fulltext_in_bucket, update, filter_query
from services.utils import get_or_create, get_document_if_exists
from services.exceptions import DocumentNotFound, InvalidVariantAttribute
from models.attribute import AttributeWithValueDB
from models.product import VariantDB
from models.tag import TagDBNoAttributes


async def validate_product_variants(product_variants: list, tags: list):
    tags_names = [tag['name'] for tag in tags]

    tags_attrs = await custom_query(
        query_string=f'SELECT ARRAY_FLATTEN(ARRAY_AGG(t.attrs), 1) FROM tag AS t WHERE t.name IN {tags_names}'
    )
    tags_attrs = tags_attrs[0]['$1'] if tags_attrs[0]['$1'] else []
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
        variant_from_db = VariantDB(id=str(uuid4()), attributes_values=attrs_from_db, name=variant.name)
        variants_from_db.append(variant_from_db)
    return variants_from_db


async def get_validated_product(product):
    if product.brand:
        brand = await get_or_create(await Buckets.get_bucket(BRANDS_BUCKET), product.brand)
        product.brand = brand

    tags = list()
    if product.tags:
        for tag in product.tags:
            db_tag = await get_document_if_exists(await Buckets.get_bucket(TAGS_BUCKET), tag)
            if not db_tag:
                raise DocumentNotFound(tag.name)
            tags.append(TagDBNoAttributes(**db_tag).dict())
    product.tags = tags

    if product.variants:
        product.variants = await validate_product_variants(product.variants, tags)
    return product


async def create_product(product):
    bucket = await Buckets.get_bucket(PRODUCTS_BUCKET)
    result = await custom_query(query_string=f'SELECT * FROM {bucket.name} AS p WHERE p.name="{product.name}" '
                                             f'AND p.brand.name="{product.brand.name}"')
    if result:
        raise UniqueConstraintViolation(['name', 'brand'])
    product = await get_validated_product(product)
    result_product = await upsert(bucket, product, key=str(uuid4()))
    return result_product


async def get_all_products(skip=0, limit=30):
    bucket = await Buckets.get_bucket(PRODUCTS_BUCKET)
    return await get_all(bucket, skip=skip, limit=limit)


async def get_product_by_uuid(uuid):
    bucket = await Buckets.get_bucket(PRODUCTS_BUCKET)
    try:
        product = await get(bucket, uuid)
    except DocumentNotFoundException:
        raise DocumentNotFound(uuid)
    return product


async def update_product_by_uuid(uuid, product):
    bucket = await Buckets.get_bucket(PRODUCTS_BUCKET)
    db_product = await get(bucket, uuid)
    name = db_product['name']
    brand_name = db_product['brand']['name']
    if product.name:
        name = product.name
    if product.brand:
        brand_name = product.brand.name
    if name != db_product['name'] or brand_name != db_product['brand']['name']:
        result = await custom_query(query_string=f'SELECT * FROM {bucket.name} AS p WHERE p.name="{name}" '
                                                 f'AND p.brand.name="{brand_name}"')
        if result:
            raise UniqueConstraintViolation(['name', 'brand'])
    product = await get_validated_product(product)
    result_product = await update(bucket, product, str(uuid))
    return result_product


async def remove_product_by_uuid(uuid):
    bucket = await Buckets.get_bucket(PRODUCTS_BUCKET)
    try:
        return await delete(bucket, uuid)
    except DocumentNotFoundException:
        raise DocumentNotFound(uuid)


def fulltext_find_product(limit=30, search_string=''):
    bucket = Buckets.get_bucket(PRODUCTS_BUCKET)
    return fulltext_in_bucket(bucket, limit=limit, search_string=search_string)
