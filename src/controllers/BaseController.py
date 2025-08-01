from src.helpers.config import get_settings, Settings
import os


class BaseController:
    def __init__(self):
        self.settings = get_settings()
        self.app_name = self.settings.App_NAME
        self.app_version = self.settings.App_VERSION    
        self.base_dir= os.path.dirname(os.path.dirname(__file__))
        self.file_dir= os.path.join(
            self.base_dir,
              "assets/files"
              )
        