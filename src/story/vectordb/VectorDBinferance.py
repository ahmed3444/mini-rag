from abc import ABC, abstractmethod
from typing import List
class VectorDBinference(ABC):
    @abstractmethod
    def connect(self) :
        pass
    @abstractmethod
    def disconnect(self) :
        pass
    @abstractmethod
    def is_connection_exists(self, collection_name: str)-> bool:
        pass
    @abstractmethod
    def list_all_collections(self) -> List[str]:
        pass

    @abstractmethod
    def get_collection_info(self, collection_name: str) -> dict:
        pass
    
    @abstractmethod
    def create_collection(self, collection_name: str, embedding_size: int, do_reset: bool = False) :
        pass    


    @abstractmethod
    def delete_collection(self, collection_name: str):
        pass


    @abstractmethod
    def insert_one_vector(self, collection_name: str
                       , texts: str ,vectors: list
                       , metadata: dict = None ,record_id: str = None) :

        pass
    @abstractmethod
    def insert_many_vectors(self, collection_name: str
                            , texts: List[str] ,vectors: List[list]
                            , metadatas: List[dict] = None ,record_ids: List[str] =None) :
        pass
    @abstractmethod
    def search_vectors(self, collection_name: str, vector: list
                       , top_k: int = 5, filter: dict = None) :
        pass

    