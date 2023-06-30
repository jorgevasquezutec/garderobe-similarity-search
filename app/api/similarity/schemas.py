from typing import List
from pydantic import BaseModel




class Product(BaseModel):
    user_id: int
    product_id: int
    image_path: str
    image_vector: List[float]
    closet_id: int

class Closet(BaseModel):
    closet_id: int
    path_model: str
    products: List[Product]
    user_id: int

class Collection(BaseModel):
    user_id: int
    path_model: str
    products: List[Product]
    closet_index: List[Closet]


class ProductReponse(BaseModel):
    product_id: int
    user_id: int
    closet_id: int


class ReponseQuery(BaseModel):
    message: str
    data: List[ProductReponse]

class ReponseInsert(BaseModel):
    message: str

class ReponseDelete(BaseModel):
    message: str

class QueryProduct(BaseModel):
    user_id: int
    image_path: str
    neighbors: int = 5
    closet_id: int = None



class InsertNearestNeighbors(BaseModel):
    user_id: int
    image_vector: List[float]
    closet_id: int = None

class QueryNearestNeighbors(BaseModel):
    user_id: int
    image_vector: List[float]
    neighbors: int = 5
    closet_id: int = None

class InsertProduct(BaseModel):
    user_id: int
    product_id: int
    image_path: str
    closet_id: int


class DeleteProduct(BaseModel):
    user_id: int
    product_id: int
    closet_id: int

