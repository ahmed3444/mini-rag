from .BaseController import BaseController
from .ProcessController import ProcessController   
class ProcessController(BaseController):
    def __init__(self,project_id:str):
        super().__init__()
        self.project_id = project_id
        self.process_controller = ProcessController().get_process_controller(project_id=project_id)
    def get_file_extension(self, file_name: str) -> str:
        return os.path.splitext(file_name)[-1]
