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
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    # print(file)
    #query
    data = similarity_service.search_item(file,owner_id,closet_id)

    return {
        "message": "Itemos Encontrados",
        "data":[
            {
                "item_id": 1,
                "owner_id": 1,
                "closet_id": 1
            },
            {
                "item_id": 2,
                "owner_id": 1,
                "closet_id": 1
            }
        ]
    }

@router.post("/insert",response_model=ReponseInsert)
def insert(
     *,
     insert_item: InsertItem,
     current_user: Annotated[User, Depends(get_current_active_user)]
):
    item = similarity_service.insert_item_with_s3_image(insert_item)
    return {"message": "Item Insertado"}
    

@router.post("/delete", response_model=ReponseDelete)
def delete(
    *,
    delete_item: DeleteItem,
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    
    similarity_service.delete_item(
        delete_item.owner_id,
        delete_item.closet_id,
        delete_item.item_id)

    return {"message": "Itemo Eliminado"}



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