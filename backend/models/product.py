from typing import List, Optional
from pydantic import BaseModel
from uuid import UUID

from models.brand import Brand, BrandDB
from models.tag import TagDBNoAttributes, TagNoAttributes
from models.attribute import AttributeWithValue, AttributeWithValueDB


class Variant(BaseModel):
    name: str
    attributes_values: List[AttributeWithValue]


class VariantDB(Variant):
    id: UUID
    attributes_values: List[AttributeWithValueDB]


class Product(BaseModel):
    name: str
    image_link: str
    brand: Brand
    tags: List[TagNoAttributes]
    variants: List[Variant]


class ProductPartialUpdate(BaseModel):
    name: Optional[str]
    image_link: Optional[str]
    brand: Optional[Brand]
    tags: Optional[List[TagNoAttributes]]
    variants: Optional[List[Variant]]


class ProductDB(Product):
    id: UUID
    brand: BrandDB
    tags: List[TagDBNoAttributes]
    variants: List[VariantDB]
