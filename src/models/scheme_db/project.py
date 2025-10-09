from pydantic import BaseModel, Field, validator
from typing import Optional, Union
from bson.objectid import ObjectId


class Project(BaseModel):
    _id: Optional[ObjectId]
    project_id: Union[str, int] = Field(...)

    @validator("project_id")
    def validate_project_id(cls, value):
      
        if not str(value).isalnum():
            raise ValueError("Project ID must not be empty and must be alphanumeric")
        return value

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def get_indexing(cls):
        return [
            {
                "key": [("project_id", 1)],
                "name": "project_id_index",
                "unique": True,
            }
        ]
