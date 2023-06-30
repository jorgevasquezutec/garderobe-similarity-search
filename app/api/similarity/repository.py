from app.config.datatabase import collection
from app.api.similarity.schemas import InsertProduct
from app.utils.aws import s3_client
from app.api.similarity.services.index_vector import IndexVector
from app.api.similarity.services.feature_extractor import feature_extractor
from pymongo.client_session import ClientSession




def insert_product(product:InsertProduct):
    user_id = product.user_id
    closet_id = product.closet_id
    image_path = product.image_path
    product_id = product.product_id
    #obtener imagen 
    image = s3_client.load_image(image_path)
    if image is None:
        raise Exception(f'Image {image_path} does not exist')
    
    #obtener vector
    image_vector = feature_extractor.get_vector(image)

    #existe documento con user_id en collection

    document = collection.find_one({"user_id":user_id})
    product = {
        "product_id": product_id,
        "image_vector": image_vector,
        "image_path": image_path,
        "closet_id": closet_id,
        "index": 0
    }


    if document is None:
        #crear documento
        document = {
            "user_id": user_id,
            "products": [product],
            "closet_index": [
                {
                    "closet_id": closet_id,
                    "products": [product]
                }
            ]
        }
        collection.insert_one(document)
    else:
        pass



    
    

