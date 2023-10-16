"""DATABASE
MongoDB database initialization
"""

# # Installed # #
from pymongo import MongoClient,ASCENDING
from pymongo.collection import Collection
from pymongo.database import Database


# # Package # #
from .settings import mongo_settings as settings

__all__ = ("client", "collection","database")

client = MongoClient(settings.URI)
collection: Collection = client[settings.DATABASE][settings.COLLECTION]
database: Database = client[settings.DATABASE]
# collection.create_index([
#     ("owner_id", ASCENDING),
# ], unique=True)
