from .BaseDataModel import BaseDataModel
from .scheme_db import Project
from .enums.DataBaseEnum import DataBaseEnum
class ProjectModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECTS_NAME.value]
    
    async def create_project(self, project: Project) :
        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True))

        project._id = result.inserted_id

        return project 
    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        await instance.init_collection()
        return instance
    
    async def init_collection(self):
        all_collections= await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_PROJECTS_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECTS_NAME.value]
            indexes = Project.get_indexing()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"] 
                )


        

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
    


 