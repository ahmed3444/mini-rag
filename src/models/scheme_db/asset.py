from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime

class Asset(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    asset_project_id: ObjectId
    asset_type: str=Field(..., min_length=1)
    asset_name: str=Field(..., min_length=1)
    asset_size: int = Field(..., ge=0)

    asset_config: Optional[dict] = Field(default=None)
    asset_pushed_out: datetime = Field(default_factory=datetime.utcnow)


    class Config:
        arbitrary_types_allowed = True


    @classmethod
    def get_index(cls, db_client, asset_id: ObjectId):
        return[
            {
                "key": [("asset_project_id", 1)],
                "name": "asset_project_id_idx",
                "unique": False
            },
            {
                "key": [("asset_name", 1)],
                "name": "asset_name_idx",
                "unique": True
            }
        ]