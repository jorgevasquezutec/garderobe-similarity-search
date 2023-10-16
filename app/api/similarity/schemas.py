from typing import List
from pydantic import BaseModel , Field ,validator
import numpy as np
from typing import Annotated,Union
from fastapi import UploadFile, File, Form


class Item(BaseModel):
    owner_id: int
    item_id: int
    image_path: str
    image_vector: List[float]
    closet_id: int
    index_user: int
    index_closet: int


class ItemReponse(BaseModel):
    item_id: Annotated[int, Field(..., description="Id del item")]
    owner_id: Annotated[int, Field(..., description="Id del dueño")]
    closet_id: Annotated[int, Field(..., description="Id del closet")]
    image_path: Annotated[str, Field(..., description="Ruta de la imagen en s3")]


class ReponseQuery(BaseModel):
    message: Annotated[str, Field(..., description="Mensaje de respuesta")] = "Items Encontrados"
    data: List[ItemReponse]

class ReponseInsert(BaseModel):
    message: Annotated[str, Field(..., description="Mensaje de respuesta")] = "Item Insertado"

class ReponseDelete(BaseModel):
    message: Annotated[str, Field(..., description="Mensaje de respuesta")] = "Item Eliminado"

class QueryBody(BaseModel):
    file :Annotated[UploadFile, File(description="Imagen a buscar")]
    owner_id: Annotated[int, Form(..., description="Id del usuario")]
    closet_id: Annotated[int, Form(..., description="Id del closet")] = None
    nearest_neighbors: Annotated[int, Form(..., description="Numero de vecinos mas cercanos")] = 5



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
    owner_id: Annotated[int, Field(..., description="Id del dueño")]
    item_id: Annotated[int, Field(..., description="Id del item")]
    image_path: Annotated[str, Field(..., description="Ruta de la imagen en s3")]
    closet_id: Annotated[int, Field(..., description="Id del closet")] = None


class DeleteItem(BaseModel):
    owner_id: Annotated[int, Field(..., description="Id del dueño")]
    item_id: Annotated[int, Field(..., description="Id del item")]
    closet_id: Annotated[int, Field(..., description="Id del closet")] = None

    @validator('owner_id', 'item_id', 'closet_id', pre=True, always=True)
    def check_nonzero_values(cls, v, values):
        if v is not None and v == 0:
            raise ValueError("El valor no puede ser 0")
        return v

