from annoy import AnnoyIndex
from app.api.similarity.schemas import QueryNearestNeighbors,InsertNearestNeighbors
import os
from config.datatabase import collection




class IndexVector:
    def __init__(self, 
                vector_size,
                metric='angular',
                n_trees=30
                ):
        self.vector_size = vector_size
        self.metric = metric
        self.index = AnnoyIndex(self.vector_size, metric=self.metric)
        self.n_trees = n_trees



    def __getUserIndexPath(self, user_id):
        index_path = f'index/annoy_{user_id}/'
        #validar si existe carpeta index
        if not os.path.exists(index_path):
            os.makedirs(index_path)
        return index_path



    def buildByChunks(curosList, 
                      chunkSize , 
                      insert: InsertNearestNeighbors ):
        user_id = insert.user_id
        vector = insert.image_vector
        closet_id = insert.closet_id




    
    def queryNearestNeighbors(
            self, 
            query: QueryNearestNeighbors
            ):
        
        user_id = query.user_id
        closet_id = query.closet_id
        vector = query.image_vector
        n_neighbors = query.neighbors
        #carpeta index en raiz
        index_path = self.__getUserIndexPath(user_id)      

        if closet_id:
            index_filename = os.path.join(index_path, f'{user_id}_{closet_id}.ann')
        else:
            index_filename = os.path.join(index_path, f'{user_id}.ann')

        if not os.path.exists(index_filename):
            raise Exception(f'Index file {index_filename} does not exist')

        self.index.load(index_filename)
        nearest_neighbors = self.index.get_nns_by_vector(vector, n_neighbors)
        return nearest_neighbors
        