"""DATABASE
MongoDB database initialization
"""

# # Installed # #
from pymongo import MongoClient,ASCENDING
from pymongo.collection import Collection


# # Package # #
from .settings import mongo_settings as settings

__all__ = ("client", "collection")

client = MongoClient(settings.URI)
collection: Collection = client[settings.DATABASE][settings.COLLECTION]
# collection.create_index([
#     ("owner_id", ASCENDING),
# ], unique=True)
