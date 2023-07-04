from typing import List
from pydantic import BaseModel
import numpy as np



class Item(BaseModel):
    owner_id: int
    item_id: int
    image_path: str
    image_vector: List[float]
    closet_id: int
    index_user: int
    index_closet: int


class ItemReponse(BaseModel):
    item_id: int
    owner_id: int
    closet_id: int
    image_path: str


class ReponseQuery(BaseModel):
    message: str
    data: List[ItemReponse]

class ReponseInsert(BaseModel):
    message: str

class ReponseDelete(BaseModel):
    message: str

class QueryItem(BaseModel):
    owner_id: int
    image_path: str
    neighbors: int = 5
    closet_id: int = None


class InsertNearestNeighbors(BaseModel):
    owner_id: int
    image_vector: List[float]
    closet_id: int = None

class QueryNearestNeighbors(BaseModel):
    owner_id: int
    image_vector: List[float]
    neighbors: int = 5
    closet_id: int = None

class InsertItem(BaseModel):
    owner_id: int
    item_id: int
    image_path: str
    closet_id: int


class DeleteItem(BaseModel):
    owner_id: int
    item_id: int
    closet_id: int

