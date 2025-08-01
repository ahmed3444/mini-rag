from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
import aiofiles

from src.helpers.config import get_settings, Settings
from src.controllers import DataController, ProjectController

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "data"],
)

@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)):
    is_valid, result_signal = DataController().validate_upload_file(file=file)

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
    os.makedirs(project_dir_path, exist_ok=True)

    file_path = os.path.join(project_dir_path, file.filename)

    async with aiofiles.open(file_path, 'wb') as out_file:
        while chunk := await file.read(app_settings.FILE_CHUNK_SIZE):
            await out_file.write(chunk)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "is_valid": is_valid,
            "result_signal": result_signal,
            "project_id": project_id,
            "file_name": file.filename,
            "file_path": file_path
        }
    )

# الوظائف اللي تحت مش مكانها هنا، تنقل لـ class أو module تاني مناسب
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
