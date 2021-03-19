from typing import List
from pydantic import BaseModel
from uuid import UUID

from .brand import Brand, BrandDB
from .tag import Tag, TagDB, TagDBNoAttributes, TagNoAttributes
from .attribute import AttributeWithValue, AttributeWithValueDB


class Variant(BaseModel):
    attributes_values: List[AttributeWithValue]


class VariantDB(Variant):
    id: UUID
    attributes_values: List[AttributeWithValueDB]


class Product(BaseModel):
    name: str
    brand: Brand
    tags: List[TagNoAttributes]
    variants: List[Variant]


class ProductDB(Product):
    id: UUID
    brand: BrandDB
    tags: List[TagDBNoAttributes]
    variants: List[VariantDB]
