from .BaseDataModel import BaseDataModel
from .scheme_db import DataChunk
from .enums.DataBaseEnum import DataBaseEnum
from pymongo import InsertOne
from bson.objectid import ObjectId
from .scheme_db import Asset  # Add this import if Asset is defined in scheme_db


class AssetModel(BaseDataModel):
    def __init__(self, db_client: object):
        super().__init__(db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTIONS_ASSET_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        all_collections= await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTIONS_ASSET_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTIONS_ASSET_NAME.value]
            indexes = Asset.get_indexing()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"] 
                )

    async def create_asset(self, asset: Asset) :
        result = await self.collection.insert_one(asset.dict(by_alias=True, exclude_unset=True))
        asset.id = result.inserted_id
        return asset

    async def get_all_assets(self, asset_project_id: str):
        return await self.collection.find(
            {
                "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id
            }
        )