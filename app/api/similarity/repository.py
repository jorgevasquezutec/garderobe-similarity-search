from app.config.database import collection


def get_user_items_count(user_id: int)-> int:
    count_pipeline = [
        {"$match": {"owner_id": user_id}},
        {"$project": {"items_count": {"$size": "$items"}}},
        {"$group": {"_id": None, "total_count": {"$sum": "$items_count"}}}
    ]
    result = collection.aggregate(count_pipeline)
    count = next(result, {"total_count": 0})["total_count"]
    return count


def get_closet_items_count(user_id: int, closet_id: int)-> int:
    count_pipeline = [
        {"$match": {"owner_id": user_id}},
        {"$project": {"total_count": {"$size": {"$filter": {"input": "$items", "as": "item", "cond": {"$eq": ["$$item.closet_id", closet_id]}}}}}}
    ]
    result = collection.aggregate(count_pipeline)
    count = next(result, {"total_count": 0})["total_count"]
    return count

def get_document_by_id(user_id: int)-> dict:
    document = collection.find_one({"owner_id":user_id},{"items":0})
    return document

def insert_document(document: dict)-> None:
    collection.insert_one(document)


 
def get_items_by_indexs(owner_id, closet_id, indexs:list)-> list:

    cond = {"$and":[
        { "$in": ["$$item.index_closet", indexs]},
        {"$eq": ["$$item.closet_id", closet_id]}
    ]} if closet_id else {"$in": ["$$item.index_user", indexs]}
    index_key = "index_user" if closet_id is None else "index_closet"

    pipeline =[
    {"$match": {"owner_id": owner_id}},
    {"$project": {
        "items": { 
            "$filter": { 
                    "input": "$items",
                    "as": "item", 
                   "cond": cond
                }}
        
    }},
    {"$unwind": "$items"}
]
    result = collection.aggregate(pipeline)
    #order by index_user same as indexs
    items = [{
        "item_id": item["items"]["item_id"],
        "owner_id": owner_id,
        "image_path": item["items"]["image_path"],
        "closet_id": item["items"]["closet_id"],
        "index_user": item["items"]["index_user"],
        "index_closet": item["items"]["index_closet"],
    } for item in result]
    sorted_items = sorted(items, key=lambda x: indexs.index(x[index_key]))
    # print(sorted_items)
    return sorted_items



def update_document(document: dict,onwer_id: int)-> None:
    collection.update_one(
        {"owner_id": onwer_id},
        {
            "$push": {
                "items": document
            }
        }
    )

def delete_item_by_onwner_id_closet_id_item_id(onwer_id: int,closet_id: int, item_id: int)-> None:
    # document have items array , delete item in array where item_id = item_id , owner_id = owner_id and closet_id = closet_id

    collection.update_one(
        {"owner_id": onwer_id, "items.item_id": item_id,
            "items.closet_id":  closet_id
            },
        {
            "$pull": {
                "items": {
                    "item_id": item_id,
                    "closet_id": closet_id
                }
            }
        }
    )
    reindex_all_index_user_field_by_onwer_id(onwer_id,1000)
    reindex_all_index_closet_field_by_onwer_id_and_closet_id(onwer_id,closet_id,1000)




def get_chunk_items_by_owner_id(owner_id: int, chunk_size: int, index_user: int)-> list:
    # print(owner_id,chunk_size,index_user)
    if(chunk_size == 0 and index_user == 0):
        return []

    pipeline = [
        {"$match": {"owner_id": owner_id}},
        {"$project": {"items": {"$slice": ["$items", index_user, chunk_size]}}},
        {"$unwind": "$items"},
    ]
    result = collection.aggregate(pipeline)
    items = [item for item in result]
    return items

def get_chunk_items_by_onwer_id_and_closet_id(owner_id: int, closet_id: int, chunk_size: int, index_closet: int)-> list:
    if(chunk_size == 0 and index_closet == 0):
        return []
    
    pipeline = [
    {"$match": {"owner_id": owner_id}},
    {"$project": {
        "items": { 
            "$slice": [ 
                { "$filter": { 
                    "input": "$items",
                    "as": "item", 
                   "cond": {"$eq": ["$$item.closet_id", closet_id]}
                }}, 
                index_closet,chunk_size
            ] 
        } 
    }},
    {"$unwind": "$items"}
]
    result = collection.aggregate(pipeline)
    items = [item for item in result]
    return items


def reindex_all_index_user_field_by_onwer_id(
        owner_id: int,
        chunk_size: int
                                             
    )-> None:
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
        chunk_items = get_chunk_items_by_owner_id(owner_id,chunk_size,i*chunk_size)
        for index,item in enumerate(chunk_items):
            collection.update_one(
                 {
                    "owner_id": owner_id, "items.item_id": item['items']['item_id'],
                    "items.closet_id":  item['items']['closet_id']
                },
                {
                    "$set": {
                        "items.$.index_user": i*chunk_size + index
                    }
                }
            )
    


def reindex_all_index_closet_field_by_onwer_id_and_closet_id(
        owner_id: int, 
        closet_id:int,
        chunk_size: int
        )-> None:
    total_items_closet = get_closet_items_count(owner_id,closet_id)
    total_chunks_closet = total_items_closet // chunk_size

    if total_chunks_closet == 0:
        chunk_size = total_items_closet
        total_chunks_closet = 1

    for i in range(total_chunks_closet):
        chunk_items = get_chunk_items_by_onwer_id_and_closet_id(owner_id,closet_id,chunk_size,i*chunk_size)
        for index,item in enumerate(chunk_items):
            collection.update_one(
                {
                    "owner_id": owner_id, "items.item_id": item['items']['item_id'],
                    "items.closet_id":  item['items']['closet_id']
                },
                {
                    "$set": {
                        "items.$.index_closet": i*chunk_size + index
                    }
                }
            )
    
    