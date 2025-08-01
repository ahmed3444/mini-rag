from .BaseController import BaseController
from fastapi import HTTPException, UploadFile
from src.models.enums.Response import ResponseStatus




class DataController(BaseController):
    def __init__(self):
        super().__init__()

    def validate_upload_file(self,file: UploadFile):
        if file.content_type not in self.settings.FILE_EXTENSIONS:
            return False,ResponseStatus.FILE_IS_NOT_TYPE
        if file.size > self.settings.FILE_MAX_SIZE * 1024 * 1024 :
            return False,ResponseStatus.FILE_SIZE_EXCEEDS_LIMIT
        return True,"file is valid"
    