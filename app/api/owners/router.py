from fastapi import APIRouter, Form, Depends, HTTPException, File, UploadFile
from app.utils.security import get_current_active_user
from app.api.owners.schemas import PaginationOwnerItems, PaginationOwners
from app.api.auth.schemas import User
from fastapi import Depends, Query, Path
from typing import Annotated, Union
import app.api.owners.service as owners_service


router = APIRouter()


@router.get('', response_model=PaginationOwners)
def all(*,
        page: int = Query(0, ge=0),
        size: int = Query(10, ge=1),
        owner_id: int = Query(None, ge=0),
        current_user: Annotated[User, Depends(get_current_active_user)]
        ):
    res = owners_service.getOnwers(page, size, owner_id)
    # print(res)
    return PaginationOwners(**res)


@router.get('/{owner_id}/items', response_model=PaginationOwnerItems)
def items(*,
          page: int = Query(0, ge=0),
          size: int = Query(10, ge=1),
          owner_id: int = Path(..., ge=0),
          closet_id: int = Query(None, ge=0),
          current_user: Annotated[User, Depends(get_current_active_user)]
          ):
    res = owners_service.getOwnerItems(owner_id, page, size, closet_id)
    return PaginationOwnerItems(**res)
