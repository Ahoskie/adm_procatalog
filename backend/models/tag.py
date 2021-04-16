from typing import List
from pydantic import BaseModel

from .attribute import Attribute, AttributeDB


class Tag(BaseModel):
    name: str
    attrs: List[Attribute]


class TagDB(Tag):
    id: int
    attrs: List[AttributeDB]


class TagNoAttributes(BaseModel):
    name: str


class TagDBNoAttributes(TagNoAttributes):
    id: int
