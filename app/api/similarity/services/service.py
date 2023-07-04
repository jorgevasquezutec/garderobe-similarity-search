import io
import app.api.similarity.repository as repository
from app.api.similarity.schemas import InsertItem,Item, QueryNearestNeighbors
from app.utils.aws import s3_client
from app.api.similarity.services.index_vector import IndexVector
from app.api.similarity.services.feature_extractor import feature_extractor
from app.config.settings import model_settings
from PIL import Image


#insert_item_with_s3_image
def insert_item_with_s3_image(item:InsertItem):
    owner_id = item.owner_id
    closet_id = item.closet_id
    image_path = item.image_path
    item_id = item.item_id
    #obtener imagen 
    image = s3_client.load_image(image_path)
    if image is None:
        raise Exception(f'Image {image_path} does not exist')
    
    image_vector = feature_extractor.extract(image)

    #falta hacerlo mas optimo.
    # document = collection.find_one({"owner_id":owner_id},{"items":0})
    document = repository.get_document_by_id(owner_id)
    item : Item = {
        "item_id": item_id,
        "image_vector": image_vector.tolist(),
        "image_path": image_path,
        "closet_id": closet_id,
        "index_user": 0,
        "index_closet": 0,
    }

    if document is None:
        #crear documento
        document = {
            "owner_id": owner_id,
            "items": [item],
        }
        repository.insert_document(document)
        # collection.insert_one(document)
    else:
        #get last count items in document
       
        item['index_user'] = repository.get_user_items_count(owner_id)
        item['index_closet'] = repository.get_closet_items_count(owner_id,closet_id)
        #actualizar documento
        repository.update_document(item,owner_id)


    # #create index_vector
    user_index_vector = IndexVector(model_settings.FEAUTRE_LENGTH)
    user_index_vector.buildByChunks(1000,owner_id,closet_id)

    # #craete index_vector closet

    closet_index_vector = IndexVector(model_settings.FEAUTRE_LENGTH,type='closet')
    closet_index_vector.buildByChunks(1000,owner_id,closet_id)

    return item


def insert_item(item:InsertItem):
    pass    



def search_item(file, owner_id, closet_id=None, nearest_neighbors=5):
    file_pillow = Image.open(io.BytesIO(file.file.read()))
    vector = feature_extractor.extract(file_pillow)
    dict : QueryNearestNeighbors = {
        "owner_id": owner_id,
        "closet_id": closet_id,
        "image_vector": vector.tolist(),
        "neighbors": nearest_neighbors,
    }
    # print(dict)
    type = 'closet' if closet_id else 'user'
    index_vector = IndexVector(model_settings.FEAUTRE_LENGTH,type=type)
    ids = index_vector.queryNearestNeighbors(dict)
    # print(ids)

    if ids:
        items = repository.get_items_by_indexs(owner_id,closet_id,ids)
        return items
    
    return []



def delete_item(owner_id,closet_id,item_id):
    repository.delete_item_by_onwner_id_closet_id_item_id(owner_id,closet_id,item_id)


    
    #delete index_vector
    user_index_vector = IndexVector(model_settings.FEAUTRE_LENGTH)
    user_index_vector.buildByChunks(1000,owner_id,closet_id)

    #craete index_vector closet

    closet_index_vector = IndexVector(model_settings.FEAUTRE_LENGTH,type='closet')
    closet_index_vector.buildByChunks(1000,owner_id,closet_id) 
    

