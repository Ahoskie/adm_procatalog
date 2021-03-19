from couchbase.cluster import Bucket
from pydantic import BaseModel

from . import filter_query


def output_pydantic_model(model: BaseModel):
    def generate_model(func):
        def wrapper(*args, **kwargs):
            db_result = func(*args, **kwargs)
            if type(db_result) == list:
                return [model.parse_obj(db_dict) for db_dict in func()]
            return model.parse_obj(db_result)
        return wrapper
    return generate_model


def get_document_if_exists(bucket: Bucket, model: BaseModel):
    data = model.dict()
    result = filter_query(bucket, **data)
    return result if result else None
