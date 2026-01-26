from pydantic import BaseModel
from typing import Optional

class PuchRequest(BaseModel):
    project_id: str
    do_reset: Optional[int] = 0
    page_no: Optional[int] = 1
    page_size: Optional[int] = 50

class SearchRequest(BaseModel):
    project_id: str
    query: str
    page_no: Optional[int] = 1
    page_size: Optional[int] = 50