from typing import List
from pydantic import BaseModel
from uuid import UUID


class Attribute(BaseModel):
    name: str


class AttributeDB(BaseModel):
    id: int


class AttributeWithValue(Attribute):
    value: str


class AttributeWithValueDB(AttributeWithValue):
    id: int
