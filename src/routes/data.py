from fastapi import FastAPI, APIRouter, Depends, UploadFile, status ,Request
from fastapi.responses import JSONResponse
import os
from .scheme_db import DataChunk

import aiofiles


from src.helpers.config import get_settings, Settings
from src.controllers import DataController, ProjectController,ProcessController
from src.models.enums.Response import ResponseStatus
from src.routes.schemes.data import ProcessRequest
from src.models.ProjectModel import ProjectModel
data_controller = DataController()
project_controller = ProjectController()


data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    is_valid, result_signal = data_controller.validate_upload_file(file=file)

    project_model=ProjectModel(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "message": result_signal,
                "project_id": project_id,
                "file_name": file.filename,
                "file_size": 0
            }
        )

    project_dir_path = ProjectController().get_project_path(project_id=project_id)
    file_path = data_controller.generate_unique_filename(
        long_file_name=file.filename,
        project_id=project_id
    )

    os.makedirs(project_dir_path, exist_ok=True)

    file_path,file_id = os.path.join(project_dir_path, file.filename)
    try:
        async with aiofiles.open(file_path, 'wb') as out_file:
            while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
                await out_file.write(chunk)

    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "message": "Error occurred while saving file",
                "signal": ResponseStatus.FILE_SAVE_ERROR,
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "is_valid": is_valid,
            "result_signal": result_signal,
            "project_id": str(project._id),
            "file_name": file.filename,
            "file_path": file_path,
            "file_id": file_id,

        }
    )

def generate_random_string(self, orig_file_string: str, project_id: str):
    random_filename = self.generate_random_string()
    project_path = ProjectController().get_project_path(project_id=project_id)
    cleaned_file_name = self.get_cleaned_file_name(orig_file_string=orig_file_string)
    new_file_path = os.path.join(project_path, random_filename + "_" + cleaned_file_name)


    while os.path.exists(new_file_path):
        random_filename = self.generate_random_string()
        new_file_path = os.path.join(project_path, random_filename + "_" + cleaned_file_name)
    return new_file_path




def get_cleaned_file_name(self, orig_file_string: str):
    return orig_file_string.replace(" ", "_").replace("/", "_").replace("\\", "_")



@data_router.post("/process/{project_id}")
async def process_endpoint(project_id:str,process_request:ProcessRequest):
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id=file_id) 
    file_chunks = process_controller.process_file_content(
        file_content=file_content,
          file_id=file_id,
            chunk_size=chunk_size,
              overlap_size=overlap_size
              )

    if file_chunks is None:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "signal": ResponseStatus.FILE_PROCESSING_ERROR,
            }
        )
    file_chunks_records=[
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_meta=chunk.metadata,
            chunk_order=index + 1,
            chunk_project_id=project._id
        )
        for index, chunk in enumerate(file_chunks)
    ]
    chunk_model = ChunkModel(db_client=request.app.db_client)
    no_records = chunk_model.insert_many_chunks(data_chunks=file_chunks_records)