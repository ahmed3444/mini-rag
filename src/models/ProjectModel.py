from .BaseDataModel import BaseDataModel
from .scheme_db import Project
from .enums.DataBaseEnum import DataBaseEnum
class ProjectModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECTS_NAME.value]
    
    async def create_project(self, project: Project) :
        result = await self.collection.insert_one(project.dict())
        project._id = result.inserted_id

        return project 
    

    async def get_project_or_create_one(self, project_id: str) :

        record = await self.collection.find_one({"project_id": project_id})
        if record is None:
            new_project = Project(project_id=project_id)
            created_project = await self.create_project(new_project)
            return created_project

        return Project(**record)
    
    async def get_all_project(self, page: int = 1, page_size: int = 10):
        total_documents = total_documents // page_size
        if total_documents % page_size > 0:
            total_documents += 1
        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size) 

        projects = []
        async for document in cursor:
            projects.append(Project(**document))

        return projects,total_documents
    


 