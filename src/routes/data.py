from fastapi import APIRouter, Depends, UploadFile, status, Request


from fastapi.responses import JSONResponse
import os
import aiofiles
import logging

from src.helpers.config import get_settings, Settings
from src.controllers import DataController, ProjectController, ProcessController
from src.models.enums.Response import ResponseSignal
from src.routes.schemes.data import ProcessRequest
from src.models.ProjectModel import ProjectModel
from src.models.ChunkModel import ChunkModel
from src.models.scheme_db import DataChunk, Asset
from src.models.enums.AssetTypeEnum import AssetTypeEnum

from src.models.AssetModel import AssetModel


logger = logging.getLogger('uvicorn.error')

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: int, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
        
    project_model = await ProjectModel.create_instance(
    db_client=request.app.state.db_client
)


    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    # validate the file properties
    data_controller = DataController()
    is_valid, result_signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result_signal
            }
        )

    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
            }
        )

    asset_model = await AssetModel.create_instance(
        db_client=request.app.state.db_client
    )

    asset_resource = Asset(
        asset_project_id= project_id,
        asset_type=AssetTypeEnum.FILE.value,
        asset_name=file_id,
        asset_size=os.path.getsize(file_path)
    )

    asset_record = await asset_model.create_asset(asset=asset_resource)

    return JSONResponse(
        content={
            "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id": str(asset_record.asset_id),
        }
    )

@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: int, process_request: ProcessRequest):
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset


    return JSONResponse(
        content={
            "signal": ResponseSignal.PROCESSING_SUCCESS.value,
        }
    )

@data_router.post("/process-and-push/{project_id}")
async def process_and_push_endpoint(request: Request, project_id: int, process_request: ProcessRequest):
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset



    return JSONResponse(
        content={
            "signal": ResponseSignal.PROCESS_AND_PUSH_WORKFLOW_READY.value,
        }
    )