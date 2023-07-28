from typing import List
from pydantic import BaseModel



class Owners(BaseModel):
    owner_id: int
    total_items : int


class OwnerItems(BaseModel):
    owner_id: int
    closet_id: int
    item_id: int
    image_path: str


class PaginationOwners(BaseModel):
    total: int
    page: int
    pages: int
    size: int
    items : List[Owners]

class PaginationOwnerItems(BaseModel):
    total: int
    page: int
    pages: int
    size: int
    items : List[OwnerItems]
