from fastapi import FastAPI, APIRouter ,status,Request
from fastapi.response import JSONResponse
from routes.schemes.nlp import PushRequest,SearchRequest
from src.models.ProjectModel import ProjectModel
from src.controllers.NLPController import NLPController
from src.models.scheme_db.ChunkModel import ChunkModel
from src.models.enums.Response import ResponseSignal
import logging
logger=logging.getLogger('unicorn_error')
nlp_router=APIRouter(
    prefix='/api/v1/nlp',
    tags=['api_v1','nlp']
)

@nlp_router.post("/index/push/{project_id}")
async def push_index(project_id:str, request:Request ,push_request:PushRequest):
    project_model= await ProjectModel.create_instance(db_client=request.app.db_client)
    project =project_model.get_project_or_create_one(
        project_id
        )

    if not project:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "Signal":ResponseSignal.PROJECT_NOT_FOUND_ERROR.value,  
                
            }
        ) 
    nlp_controller=NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client
    )
    has_reccord=True
    page_no=1
    while has_records:
        page_chunks = chunk_model.get_poject_chunks(project_id=project.id, page_no=page_no)
        if len(page_chunks):
            page_no += 1

        if not page_chunks or len(page_chunks) == 0:
            has_records = False
            break

    is_inserted = nlp_controller.index_into_vector_db(
        project=project,
        chunks=page_chunks,
        do_reset=push_request.do_reset
    )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "Signal":ResponseSignal.SUCCESS.value,  
            
        }
    )
@nlp_router.get("/index/info/{project_id}")
async def get_project_index_info(project_id:str, request:Request):
    project_model= await ProjectModel.create_instance(db_client=request.app.db_client)
    project =project_model.get_project_or_create_one(
        project_id=project_id
        )
    nlp_controller=NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client
    )
    collection_info = nlp_controller.get_vector_db_collection_info(project=project)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "Signal":ResponseSignal.SUCCESS.value,  
            "collection_info":collection_info
        }
    )
@nlp_router.post("/index/search/{project_id}")
async def search_index(project_id:str, request:Request,search_request:SearchRequest):
    project_model= await ProjectModel.create_instance(db_client=request.app.db_client)
    project =project_model.get_project_or_create_one(
        project_id=project_id
        )
    nlp_controller=NLPController(
        vectordb_client=request.app.vectordb_client,
        generation_client=request.app.generation_client,
        embedding_client=request.app.embedding_client
    )
    search_result = nlp_controller.search_index(
        project=project,
        search_request=search_request
    )

    

