from pydantic import BaseModel, Field, validator
from typing import Optional
from bson.objectid import ObjectId


class Project(BaseModel):
    id:Optional[ObjectId] = Field(None,alias = "_id")
    project_id:str=Field(...,min_length=1)
    @validator('project_id')
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError('Project ID must be alphanumeric')
        return value
    
    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True
    }

    @classmethod
    def get_indexes(cls):

        return [
            {
                "key": [
                    ("project_id", 1)
                ],
                "name": "project_id_index_1",
                "unique": True
            }
        ]
