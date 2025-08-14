from .BaseController import BaseController
from fastapi import HTTPException, UploadFile
from src.models.enums.Response import ResponseStatus
from .ProjectController import ProjectController
import re
import os




class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_upload_file(self,file: UploadFile):
        if file.content_type not in self.settings.FILE_EXTENSIONS:
            return False,ResponseStatus.FILE_IS_NOT_TYPE
        if file.size > self.settings.FILE_MAX_SIZE * 1024 * 1024 :
            return False,ResponseStatus.FILE_SIZE_EXCEEDS_LIMIT
        return True,"file is valid"
    
    def generate_unique_filename(self, orig_file_name: str, project_id: str):
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        cleaned_file_name = self.get_cleaned_file_name(orig_file_string=orig_file_name)
        new_file_path = os.path.join(project_path, random_key + "_" + cleaned_file_name)
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(project_path, random_key + "_" + cleaned_file_name)
        return new_file_path ,random_key + "_" + cleaned_file_name
    

    def get_cleaned_file_name(self, orig_file_string: str):
        cleaned_file_name = re.sub(r'[^\w. ]', '_', orig_file_string)
        return cleaned_file_name.strip('_.')

