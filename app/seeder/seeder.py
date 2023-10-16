from app.config.database import database,collection
from app.api.similarity.services.index_vector import IndexVector
from app.config.settings import model_settings

def run():
    index_vector_items = collection.find()
    for item in index_vector_items:
        # print(item['owner_id'])
        # drop collection
        owner_id = item['owner_id']
        items = item['items']
        all_closets_unique = set([item['closet_id'] for item in items])
        # print(list(all_closets_unique))
        owner_collection = database[f'items_{owner_id}']
        #if onwer_collection exists drop 
        owner_collection.delete_many({})
        #create owner_collection

        owner_collection.insert_many(items)
        user_index_vector = IndexVector(model_settings.FEAUTRE_LENGTH)
        user_index_vector.buildByChunks(1000,owner_id,0)

        for closet_id in all_closets_unique:
            closet_index_vector = IndexVector(model_settings.FEAUTRE_LENGTH,type='closet')
            closet_index_vector.buildByChunks(1000,owner_id,closet_id)






if __name__ == "__main__":
    run()