from fastapi import FastAPI, APIRouter ,status,Request
from fastapi.response import JSONResponse
from routes.schemes.nlp import PushRequest
from src.models.ProjectModel import ProjectModel
import logging
logger=logging.getLogger('unicorn_error')
nlp_router=APIRouter(
    prefix='/api/v1/nlp',
    tags=['api_v1','nlp']
)

@nlp_router.post("/index/push/{project_id}")
async def push_index(project_id:str, request:Request ,push_request:PushRequest):
    project_model= await ProjectModel.create_instance(db_client=request.app.bd_client)
    project =project_model.get_project_or_create_one(
        project_id
        )

