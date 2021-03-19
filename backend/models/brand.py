from pydantic import BaseModel


class Brand(BaseModel):
    name: str


class BrandDB(Brand):
    id: int
