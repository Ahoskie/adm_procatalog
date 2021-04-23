from typing import Optional
from pydantic import BaseModel


class Brand(BaseModel):
    name: str


class BrandPartialUpdate(BaseModel):
    name: Optional[str]


class BrandDB(Brand):
    id: int
