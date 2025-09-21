from .BaseDataModel import BaseDataModel
from .scheme_db import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from pymongo import InsertOne
from bson.objectid import ObjectId
def ChunkModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.DATA_CHUNKS.value]
    
    async def create_data_chunk(self, data_chunk: DataChunk) :
        result = await self.collection.insert_one(data_chunk.dict())
        data_chunk._id = result.inserted_id

        return data_chunk
    async def get_data_chunks_by_project_id(self, chunk_id: str):
        cursor = await self.collection.find({"_id": chunk_id})


        data_chunks = []
        async for document in cursor:
            data_chunks.append(DataChunk(**document))

        return data_chunks
    async def insert_many_chunks(self, data_chunks: list[DataChunk],batch_size: int = 100):
        for i in range(0, len(data_chunks), batch_size):
            batch = data_chunks[i:i + batch_size]
            operations = [InsertOne(chunk.dict()) for chunk in batch]
            await self.collection.bulk_write(operations)
    async def delete_chunks_by_project_id(self, project_id: str):
        result = await self.collection.delete_many({"chunk_project_id": ObjectId(project_id)})
        return result.deleted_count
    
