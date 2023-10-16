from app.config.database import collection, database


def get_item(owner_id: int, closet_id: int, item_id: int) -> dict:

    query={}

    if(closet_id is not None):
        query["closet_id"] = closet_id
    if(item_id is not None):
        query["item_id"] = item_id

    print(query)
    
    document = database[f'items_{owner_id}'].find_one(query)
    return document

def get_items(page: int =0 , size: int = 10 , owner_id: int = None) -> list:
    collections = database.list_collection_names()
    #get collection with prefix items_
    items_collections = [collection for collection in collections if collection.startswith('items_')]

    if owner_id:
        items_collections = [collection for collection in items_collections if collection.split('_')[1] == owner_id]


    response = []
    for collection in items_collections:
        icollection = database[collection]
        total = icollection.count_documents({})
        response.append({
            "owner_id": collection.split('_')[1],
            "total_items": total
        })
    
    filter = response[page*size:page*size+size]
    #response page with size 
    return {
        "items": filter,
        "total": total,
        "page": page,
        "pages":  (total + size - 1) // size,
        "size": size
    }

def get_items_user_paginate(owner_id: int, page: int = 0, size: int = 10, closet_id: int = None) -> list:
    collection = database[f'items_{owner_id}']
    query = {}
    if closet_id:
        query["closet_id"] = closet_id
    items = collection.find(query).skip(page*size).limit(size)
    total = collection.count_documents(query)
    return {
        "items": [{
            "item_id": item["item_id"],
            "owner_id": owner_id,
            "image_path": item["image_path"],
            "closet_id": item["closet_id"]
        } for item in items],
        "total": total,
        "page": page,
        "pages":  (total + size - 1) // size,
        "size": size
    }

def get_user_items_count(owner_id: int) -> int:
    collection = database[f'items_{owner_id}']
    total = collection.count_documents({})
    return total


def get_closet_items_count(owner_id: int, closet_id: int) -> int:
    collection = database[f'items_{owner_id}']
    total = collection.count_documents({"closet_id": closet_id})
    return total

def insert_document(document: dict) -> None:
    owner_id = document['owner_id']
    items = document['items']
    collection = database[f'items_{owner_id}']
    collection.insert_many(items)

def get_items_by_indexs(owner_id: int, closet_id: int, indexs: list) -> dict:
    collection = database[f'items_{owner_id}']
    query = {}
    if closet_id:
        query["closet_id"] = closet_id
        if indexs:
            query["index_closet"] = {"$in": indexs}
    else:
        if indexs:
            query["index_user"] = {"$in": indexs}
    items = collection.find(query)
    return [{
        "item_id": item["item_id"],
        "owner_id": owner_id,
        "image_path": item["image_path"],
        "closet_id": item["closet_id"]
    } for item in items]
    
def delete_item_by_onwner_id_closet_id_item_id(onwer_id: int, closet_id: int, item_id: int) -> None:
    collection = database[f'items_{onwer_id}']
    collection.delete_one({"item_id": item_id, "closet_id": closet_id})


    reindex_all_index_user_field_by_onwer_id(onwer_id, 1000)
    reindex_all_index_closet_field_by_onwer_id_and_closet_id(
        onwer_id, closet_id, 1000)


def get_chunk_items_by_owner_id(owner_id: int, chunk_size: int, index_user: int) -> list:
    if (chunk_size == 0 and index_user == 0):
        return []
    collection = database[f'items_{owner_id}']
    items = collection.find().skip(index_user).limit(chunk_size)

    return list(items)


def get_chunk_items_by_onwer_id_and_closet_id(owner_id: int, closet_id: int, chunk_size: int, index_closet: int) -> list:
    if (chunk_size == 0 and index_closet == 0):
        return []
    
    collection = database[f'items_{owner_id}']
    items = collection.find({"closet_id": closet_id}).skip(index_closet).limit(chunk_size)
    return list(items)


def reindex_all_index_user_field_by_onwer_id(
        owner_id: int,
        chunk_size: int

) -> None:
    total_items = get_user_items_count(owner_id)
    total_chunks = total_items // chunk_size

    '''
        i = 1 ; chunk_size = 10
        1*10 + 0 = 10
        1*10 + 1 = 11

    '''
    if total_chunks == 0:
        chunk_size = total_items
        total_chunks = 1

    for i in range(total_chunks):
        chunk_items = get_chunk_items_by_owner_id(
            owner_id, chunk_size, i*chunk_size)
        for index, item in enumerate(chunk_items):
            database[f'items_{owner_id}'].update_one({
                "item_id": item['item_id'],
                "closet_id":  item['closet_id']
            },{
                "$set": {
                    "index_user": i*chunk_size + index
                }
            })

def reindex_all_index_closet_field_by_onwer_id_and_closet_id(
        owner_id: int,
        closet_id: int,
        chunk_size: int
) -> None:
    total_items_closet = get_closet_items_count(owner_id, closet_id)
    total_chunks_closet = total_items_closet // chunk_size

    if total_chunks_closet == 0:
        chunk_size = total_items_closet
        total_chunks_closet = 1

    for i in range(total_chunks_closet):
        chunk_items = get_chunk_items_by_onwer_id_and_closet_id(
            owner_id, closet_id, chunk_size, i*chunk_size)
        for index, item in enumerate(chunk_items):
            database[f'items_{owner_id}'].update_one({
                "item_id": item['item_id'],
                "closet_id":  item['closet_id']
            },{
                "$set": {
                    "index_closet": i*chunk_size + index
                }
            })
