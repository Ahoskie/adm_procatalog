from typing import List, Optional
from pydantic import BaseModel


class Search(BaseModel):
    search_string: str
