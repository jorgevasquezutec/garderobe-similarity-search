from annoy import AnnoyIndex
from app.api.similarity.schemas import QueryNearestNeighbors,InsertNearestNeighbors
import os
import app.api.similarity.repository as repository


class IndexVector:
    def __init__(self, 
                vector_size,
                metric='angular',
                n_trees=30,
                type = 'user'
                ):
        self.vector_size = vector_size
        self.metric = metric
        self.index = AnnoyIndex(self.vector_size, metric=self.metric)
        self.n_trees = n_trees
        self.type = type


    def __getUserIndexPath(self, owner_id):
        index_path = f'index/annoy_{owner_id}/'
        #validar si existe carpeta index
        if not os.path.exists(index_path):
            os.makedirs(index_path)
        return index_path



    def buildByChunks(self,chunkSize : int, owner_id : int,closet_id : int ) -> None:
     #carpeta index en raiz
        index_path = self.__getUserIndexPath(owner_id)

        if(self.type == 'user'):
             #count_items
            total_items = repository.get_user_items_count(owner_id)
            total_chunks = total_items // chunkSize
            #ReadByChunks and insert in index
            for i in range(total_chunks):
                chunk_items = repository.get_chunk_items_by_owner_id(owner_id,i,i*chunkSize)
                for item in chunk_items:
                    self.index.add_item(item['index_user'],item['image_vector'])
            self.index.build(self.n_trees)
            self.index.save(os.path.join(index_path, f'{owner_id}.ann'))
        else:
            total_items_closet = repository.get_closet_items_count(owner_id,closet_id)
            total_chunks_closet = total_items_closet // chunkSize
            #ReadByChunks and insert in index
            for i in range(total_chunks_closet):
                chunk_items = repository.get_chunk_items_by_onwer_id_and_closet_id(owner_id,closet_id,i,i*chunkSize)
                for item in chunk_items:
                    self.index.add_item(item['index_closet'],item['image_vector'])
            self.index.build(self.n_trees)
            self.index.save(os.path.join(index_path, f'{owner_id}_{closet_id}.ann'))

    
    def queryNearestNeighbors(
            self, 
            query: QueryNearestNeighbors
            ):
        
        owner_id = query.owner_id
        closet_id = query.closet_id
        vector = query.image_vector
        n_neighbors = query.neighbors
        #carpeta index en raiz
        index_path = self.__getUserIndexPath(owner_id)      

        if closet_id:
            index_filename = os.path.join(index_path, f'{owner_id}_{closet_id}.ann')
        else:
            index_filename = os.path.join(index_path, f'{owner_id}.ann')

        if not os.path.exists(index_filename):
            raise Exception(f'Index file {index_filename} does not exist')

        self.index.load(index_filename)
        nearest_neighbors = self.index.get_nns_by_vector(vector, n_neighbors)
        return nearest_neighbors
        