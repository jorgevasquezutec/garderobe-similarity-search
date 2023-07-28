
import app.api.similarity.repository as similarity_repository


def getOnwers(page: int = 0,
              size: int = 10,
              owner_id: int = None
              ):
    return similarity_repository.get_items(page, size, owner_id)


def getOwnerItems(owner_id: int,
                  page: int = 0,
                  size: int = 10,
                  closet_id: int = None
                  ):
    return similarity_repository.get_items_user_paginate(owner_id, page, size, closet_id)
