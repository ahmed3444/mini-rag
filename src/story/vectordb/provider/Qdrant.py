from story.vectordb.VectorDBinferance import VectorDBInferance
from story.vectordb.VectorEnums import VectorDBEnums, DistanceMethodEnums
import logging
from qdrant_client import QdrantClient,models


logger = logging.getLogger(__name__)


class QdrantVectorDB(VectorDBInferance):
    def __init__(self, db_path: str, distance_method: str):

        self.db_path = db_path
        self.distance_method = None
        self.client = None
        if distance_method in DistanceMethodEnums.COSINE.value:
            self.distance_method = distance_method
        elif distance_method in DistanceMethodEnums.EUCLIDEAN.value:
            self.distance_method = distance_method
        elif distance_method in DistanceMethodEnums.DOT_PRODUCT.value:
            self.distance_method = distance_method
        elif distance_method in DistanceMethodEnums.DOT.value:
            self.distance_method = distance_method


    def connect(self):
        self.client = QdrantClient(path=self.db_path)
        self.client.connect()
    def disconnect(self):
        self.client=None

    def is_connection_exists(self, collection_name: str) -> bool:
        return self.client.has_collection(collection_name=collection_name)
    
    def list_all_collections(self) -> list[str]:
        return self.client.get_collections().collections
    

    def get_collection_info(self, collection_name: str) -> dict:
        return self.client.get_collection(collection_name=collection_name).dict()
    

    def create_collection(self, collection_name: str, embedding_size: int, do_reset: bool = False):

        if do_reset :
            _ =  self.delete_collection(collection_name=collection_name)

        if not self.is_connection_exists(collection_name):
            _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    embedding_size=embedding_size,
                    distance=self.distance_method
                )
            )
            return True
        return False
    def insert_one_vector(self, collection_name: str
                       , texts: str ,vectors: list
                       , metadata: dict = None ,record_id: str = None):

        if not self.is_connection_exists(collection_name):
            logger.error(f"Collection {collection_name} does not exist.")
            return False
        try:
            _ = self.client.upload_records(
                collection_name=collection_name,
                records=[models.Record(
                    id=record_id,
                    vector=vectors,
                    payload={
                        "text": texts,
                        "metadata": metadata
                    }

                )
            ]
            )
        except Exception as e:
            logger.error(f"Error inserting vector: {e}")
        
        return True
    def insert_many_vectors(self, collection_name: str
                            , texts: list[str] ,vectors: list[list]
                            , metadatas: list[dict] = None ,record_ids: list[str] =None,batch_size: int=50):

        if metadatas is None:
            metadatas = [None] * len(vectors)
        if record_ids is None:
            record_ids = [None] * len(vectors)

        for i in range(0,len(texts),batch_size):
            batch_end=i+batch_size
            batch_texts=texts[i:batch_end]
            batch_vectors=vectors[i:batch_end]  
            batch_metadatas=metadatas[i:batch_end]
            batch_record_ids=record_ids[i:batch_end]

            batch_record=[
                models.Record(
                    id=batch_record_ids[idx],
                    vector=batch_vectors[idx],
                    payload={
                        "text": batch_texts[idx],
                        "metadata": batch_metadatas[idx]
                    }
                ) for idx in range(len(batch_vectors))
            ]
            try:
                _ = self.client.upload_records(
                    collection_name=collection_name,
                    records=batch_record
                )
            except Exception as e:
                logger.error(f"Error inserting batch starting at index {i}: {e}")
                return False
    def search_vectors(self, collection_name: str
                       , query_vector: list
                       , top_k: int
                       , filter_metadata: dict = None) -> list[dict]:
        return self.client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=top_k,
            query_filter=filter_metadata
        )