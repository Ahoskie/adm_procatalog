from pydantic import BaseModel


class Search(BaseModel):
    search_string: str
