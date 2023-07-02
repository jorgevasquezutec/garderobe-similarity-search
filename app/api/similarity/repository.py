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


def update_document(document: dict,onwer_id: int)-> None:
    collection.update_one(
        {"owner_id": onwer_id},
        {
            "$push": {
                "items": document
            }
        }
    )


def get_chunk_items_by_owner_id(owner_id: int, chunk_size: int, index_user: int)-> list:
    pipeline = [
        {"$match": {"owner_id": owner_id}},
        {"$project": {"items": {"$slice": ["$items", index_user, chunk_size]}}},
        {"$unwind": "$items"},
    ]
    result = collection.aggregate(pipeline)
    items = [item for item in result]
    return items

def get_chunk_items_by_onwer_id_and_closet_id(owner_id: int, closet_id: int, chunk_size: int, index_closet: int)-> list:
    pipeline = [
        {"$match": {"owner_id": owner_id}},
        {"$project": {"items": {"$slice": ["$items", index_closet, chunk_size]}}},
        {"$unwind": "$items"},
        {"$match": {"items.closet_id": closet_id}},
    ]
    result = collection.aggregate(pipeline)
    items = [item for item in result]
    return items
