from fastapi import APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
import os
import aiofiles
import logging

from src.helpers.config import get_settings, Settings
from src.controllers import DataController, ProjectController, ProcessController
from src.models.enums.Response import ResponseStatus
from src.routes.schemes.data import ProcessRequest
from src.models.ProjectModel import ProjectModel
from src.models.ChunkModel import ChunkModel
from src.models.scheme_db import DataChunk

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    # get or create project
    project_model = await ProjectModel.create_instance(db_client=request.app.mongodb_client)

    project = await project_model.get_project_or_create_one(project_id=project_id)

    # validate file
    data_controller = DataController()
    is_valid, result_signal = data_controller.validate_upload_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": result_signal
            }
        )

    # build unique file path
    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filename(
        orig_file_name=file.filename,
        project_id=project_id
    )

    os.makedirs(project_dir_path, exist_ok=True)

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error(f"Error while uploading file: {e}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "signal": ResponseStatus.FILE_SAVE_ERROR,
            }
        )

    return JSONResponse(
        content={
            "signal": ResponseStatus.FILE_UPLOAD_SUCCESS,
            "file_id": file_id,
            "file_name": file.filename,
            "project_id": str(project._id)
        }
    )


@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: str, process_request: ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.reset_previous_chunks

    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id=file_id)
    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size,
    )

    if file_chunks is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "signal": ResponseStatus.FILE_PROCESSING_ERROR,
            }
        )

    # save chunks in DB
    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    file_chunks_records = [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_meta=chunk.metadata,
            chunk_order=index + 1,
            chunk_project_id=project._id,
        )
        for index, chunk in enumerate(file_chunks)
    ]

    no_records = chunk_model.insert_many_chunks(data_chunks=file_chunks_records)

    return JSONResponse(
        content={
            "signal": ResponseStatus.PROCESSING_SUCCESS,
            "file_id": file_id,
            "Inserted_chunks": no_records,
        }
    )
