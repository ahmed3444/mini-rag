from .BaseController import BaseController
from src.models.scheme_db import Project,DataChunk
import json
class NLPController(BaseController):
    def __init__(self,vectordb_client,generation_client,embedding_client):
        super().__init__() 
        self.vectordb_client=vectordb_client
        self.generation_client=generation_client
        self.embedding_client=embedding_client
    def create_collection_name(self,project_id:str):
         return f"{project_id}_collection" 
    def reset_vector_db_collection(self,project:Project):
        collection_name=self.create_collection_name(project_id=project.project_id )
        return self.vectordb_client.delet_collection(collection_name=collection_name)
    
    def get_vector_db_collection_info(self,project:Project):
        collection_name=self.create_collection_name(project_id=project.project_id )
        return self.vectordb_client.get_collection_info(collection_name=collection_name) 
        return json.loads(json.dumps(collection_info,default=lambda x:x.__dict__))
    
    def index_info_vector_db(self,project:Project ,chunk:list[DataChunk],do_reset:bool=False):

        collection_name=self.create_collection_name(project_id=project.project_id )
        
        text=[c.chunk_text for c in chunk]
        metadata=[c.metadata for c in chunk]
        vector=[
            self.embedding_client.embed_text(text=text,document_type=DocumentTypeEnum.DOCUMENT.value )
        for text in text
        ]
        _=self.vectordb_client.create_collection(
            collection_name=collection_name,
            metadata=metadata,
            vector=vector,
        )

        _=self.vectordb_client.insert_many(
            collection_name=collection_name,
            documents=documents,
            metadata=metadata,
            vector=vector,
        )
        return True 


