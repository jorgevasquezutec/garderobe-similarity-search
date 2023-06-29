from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.utils.security import get_current_active_user
from app.api.similarity.schemas import ReponseQuery,QueryProduct,InsertProduct,ReponseInsert,ReponseDelete,DeleteProduct
from app.api.auth.schemas import User
from fastapi import Depends
from typing import Annotated


router = APIRouter()

@router.post("/query", response_model=ReponseQuery)
def query(
    *,
    query_product : QueryProduct,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return {
        "message": "Productos Encontrados",
        "data":[
            {
                "product_id": 1,
                "user_id": 1,
                "closet_id": 1
            },
            {
                "product_id": 2,
                "user_id": 1,
                "closet_id": 1
            }
        ]
    }

@router.post("/insert",response_model=ReponseInsert)
def insert(
     *,
     insert_product: InsertProduct,
     current_user: Annotated[User, Depends(get_current_active_user)]
):
    return {"message": "Producto Insertado"}

@router.post("/delete", response_model=ReponseDelete)
def delete(
    *,
    delete_product: DeleteProduct,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return {"message": "Producto Eliminado"}
