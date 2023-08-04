from fastapi import APIRouter, Depends, HTTPException
from app.utils.security import get_current_active_user
from app.api.similarity.schemas import ReponseQuery, QueryBody, InsertItem, ReponseInsert, ReponseDelete, DeleteItem
from app.api.auth.schemas import User
from fastapi import Depends
from typing import Annotated
import app.api.similarity.services.service as similarity_service

router = APIRouter()


@router.post("/query", response_model=ReponseQuery)
def query(
    *,
    queryBody: QueryBody = Depends(),
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    try:
        data = similarity_service.search_item(
            owner_id=queryBody.owner_id,
            closet_id=queryBody.closet_id,
            file=queryBody.file,
            nearest_neighbors=queryBody.nearest_neighbors
        )
        res: ReponseQuery = {
            "message": "Items Encontrados",
            "data": data
        }
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/insert", response_model=ReponseInsert)
def insert(
    *,
    insert_item: InsertItem,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    try:
        item = similarity_service.insert_item_with_s3_image(insert_item)
        return {"message": "Item Insertado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/delete", response_model=ReponseDelete)
def delete(
    *,
    delete_item: DeleteItem,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    try:
        similarity_service.delete_item(
            delete_item.owner_id,
            delete_item.closet_id,
            delete_item.item_id)
        return {"message": "Item Eliminado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
