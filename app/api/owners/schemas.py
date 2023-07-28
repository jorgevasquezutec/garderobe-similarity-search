from typing import List
from pydantic import BaseModel, Field



class Owners(BaseModel):
    owner_id: int = Field(description="Id del dueño")
    total_items : int= Field(description="Total de items")


class OwnerItems(BaseModel):
    owner_id: int = Field(description="Id del dueño")
    closet_id: int = Field(description="Id del closet")
    item_id: int = Field(description="Id del item")
    image_path: str = Field(description="Ruta de la imagen en s3")


class PaginationOwners(BaseModel):
    total: int = Field(description="Total de dueños")
    page: int =  Field(description="Numero de página")
    pages: int = Field(description="Total de páginas")
    size: int = Field(description="Tamaño de la página")
    items : List[Owners] = Field(description="Lista de dueños")

class PaginationOwnerItems(BaseModel):
    total: int = Field(description="Total de items")
    page: int = Field(description="Numero de página")
    pages: int = Field(description="Total de páginas")
    size: int = Field(description="Tamaño de la página")
    items : List[OwnerItems] = Field(description="Lista de items")
