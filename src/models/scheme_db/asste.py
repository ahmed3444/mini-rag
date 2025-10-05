from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from datetime import datetime

class Asset(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    asste_project_id: ObjectId
    asste_type: str=Field(..., min_length=1)
    asste_name: str=Field(..., min_length=1)
    asste_size: int = Field(..., ge=0)

    asste_config: Optional[dict] = Field(default=None)
    asste_pushed_out: datetime = Field(default_factory=datetime.utcnow)


    class Config:
        arbitrary_types_allowed = True


    @classmethod
    def get_index(cls, db_client, asset_id: ObjectId):
        return[
            {
                "key": [("asste_project_id", 1)],
                "name": "asste_project_id_idx",
                "unique": False
            },
            {
                "key": [("asste_name", 1)],
                "name": "asste_name_idx",
                "unique": True
            }
        ]