from fastapi import APIRouter,Form, Depends, HTTPException, File, UploadFile
from app.utils.security import get_current_active_user
from app.api.similarity.schemas import ReponseQuery,QueryItem,InsertItem,ReponseInsert,ReponseDelete,DeleteItem
from app.api.auth.schemas import User
from fastapi import Depends
from typing import Annotated,Union
import app.api.similarity.services.service as similarity_service


router = APIRouter()

@router.post("/query", response_model=ReponseQuery)
def query(
    *,
    file: Annotated[UploadFile, File()],
    owner_id: Annotated[int, Form(...)],
    closet_id: Annotated[int, Form(...)] = None,
    nearest_neighbors: Annotated[int, Form(...)] = 5,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    try:
        
        data = similarity_service.search_item(file,owner_id,closet_id,nearest_neighbors)
        res : ReponseQuery = {
            "message": "Items Encontrados",
            "data": data
        }
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/insert",response_model=ReponseInsert)
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
        return {"message": "Itemo Eliminado"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




# @router.post("/query/")
# async def create_file(
#     # file: Annotated[bytes, File()],
#     file: Annotated[UploadFile, File()],
#     token: Annotated[str, Form()],
# ):
#     return {
#         "file_size": len(file),
#         "token": token,
#         "fileb_content_type": fileb.content_type,
#     }