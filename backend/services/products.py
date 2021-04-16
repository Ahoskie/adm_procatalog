from uuid import uuid4

from couchbase.exceptions import DocumentNotFoundException

from db.buckets import Buckets
from core.config import PRODUCTS_BUCKET, BRANDS_BUCKET, TAGS_BUCKET
from services import upsert, get, get_all, filter_query, update, delete, custom_query
from services.utils import get_or_create
from services.exceptions import DocumentNotFound, DocumentAlreadyExists, InvalidVariantAttribute
from models.attribute import AttributeWithValueDB
from models.tag import TagDBNoAttributes


def create_product(product):
    bucket = Buckets.get_bucket(PRODUCTS_BUCKET)
    brand = get_or_create(Buckets.get_bucket(BRANDS_BUCKET), product.brand)
    product.brand = brand

    tags = list()
    for tag in product.tags:
        db_tag = TagDBNoAttributes(**get_or_create(Buckets.get_bucket(TAGS_BUCKET), tag))
        tags.append(db_tag.dict())
    product.tags = tags

    tags_names = [f'{tag["name"]}' for tag in tags]
    tags_attributes = custom_query(
        Buckets.get_bucket(TAGS_BUCKET),
        query_string=f'SELECT ARRAY_FLATTEN(ARRAY_AGG(t.attrs), 1) FROM tag AS t WHERE t.name IN {tags_names}'
    )[0]['$1']
    if tags_attributes:
        for variant in product.variants:
            variant_attrs = list()
            for attr in variant.attributes_values:
                if attr.name not in [tag_attr['name'] for tag_attr in tags_attributes]:
                    raise InvalidVariantAttribute(attr, available_attrs=tags_attributes)
                attr_id = [attribute['id'] for attribute in tags_attributes if attribute['name'] == attr.name][0]
                db_attr = AttributeWithValueDB(**attr.dict(), id=attr_id)
                variant_attrs.append(db_attr)
            variant.attributes_values = variant_attrs
            # variant.id = str(uuid4())
    result_product = upsert(bucket, product, key=str(uuid4()))
    return result_product


def get_all_products():
    bucket = Buckets.get_bucket(PRODUCTS_BUCKET)
    return get_all(bucket)


def get_product_by_uuid(uuid):
    bucket = Buckets.get_bucket(PRODUCTS_BUCKET)
    try:
        product = get(bucket, uuid)
    except DocumentNotFoundException:
        raise DocumentNotFound(uuid)
    return product


def update_product_by_uuid(uuid, product):
    bucket = Buckets.get_bucket(PRODUCTS_BUCKET)
    stored_product = get_product_by_uuid(uuid)
    update_data = product.dict(exclude_unset=True)
    # updated_product = Product(**stored_product).copy(update=update_data)
    # return update(bucket, product, uuid)


def remove_product_by_uuid(uuid):
    bucket = Buckets.get_bucket(PRODUCTS_BUCKET)
    try:
        return delete(bucket, uuid)
    except DocumentNotFoundException:
        raise DocumentNotFound(uuid)
