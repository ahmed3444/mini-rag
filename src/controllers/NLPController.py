from .BaseController import BaseController
from src.models.scheme_db import Project
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
    
    def reset_vector_db_collection_info(self,project:Project):
        collection_name=self.create_collection_name(project_id=project.project_id )
        return self.vectordb_client.delete_collection_info(collection_name=collection_name)