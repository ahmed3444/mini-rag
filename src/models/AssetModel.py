from .BaseDataModel import BaseDataModel
from .scheme_db.asset import Asset

from bson import ObjectId

class AssetModel(BaseDataModel):
    def __init__(self, db_client: object = None):
        super().__init__(db_client=db_client)
        self.collection = self.db_client["assets"]

    @classmethod
    async def create_instance(cls, db_client: object):
        instance = cls(db_client)
        return instance

    async def create_asset(self, asset: Asset):
        """إضافة asset جديد"""
        doc = asset.dict() if hasattr(asset, "dict") else asset
        result = await self.collection.insert_one(doc)
        return str(result.inserted_id)

    async def get_all_project_assets(self, asset_project_id: str, asset_type: str):
        """جلب كل الأصول حسب المشروع والنوع"""
        cursor = self.collection.find({
            "asset_project_id": asset_project_id,
            "asset_type": asset_type
        })
        return await cursor.to_list(length=None)

    async def get_asset_record(self, asset_project_id: str, asset_name: str):
        """جلب أصل واحد"""
        return await self.collection.find_one({
            "asset_project_id": asset_project_id,
            "asset_name": asset_name
        })
