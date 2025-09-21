from .BaseController import BaseController
from .ProjectController import ProjectController  
import os
from langchain_community.document_loaders import TextLoader

from langchain_community.document_loaders import PyMuPDFLoader 
from langchain.text_splitter import RecursiveCharacterTextSplitter


from src.models.enums import ProcessingEnum
class ProjectController(BaseController):
    def __init__(self,project_id:str):
        super().__init__()
        self.project_id = project_id
        self.process_controller = ProjectController().get_process_controller(project_id=project_id)
    def get_file_extension(self, file_name: str) -> str:
        return os.path.splitext(file_name)[-1]
    def get_loader(self, file_name: str):
        extension = self.get_file_extension(file_name)
        if extension == ProcessingEnum.TEXT.value:
            return TextLoader(file_name, encoding="utf-8")
        if extension == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_name)
        return None

    def process_file_content(self, file_content: list, file_id: str,
                         chunk_size: int = 100, overlap_size: int = 20):

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )
        file_content_texts=[
            rec.page_content
             for rec in file_content 
        ]
        file_content_metadata=[
            rec.metadata
            for rec in file_content
        ]
        chunks= text_splitter.split_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )
        return chunks
