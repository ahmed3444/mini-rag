from .VectorEnums import VectorDBEnums
from .provider.Qdrant import QdrantVectorDB
from controllers.BaseController import BaseController

class VectorDBProviderFactory:
    def __init__(self, config: dict):
        self.config = config
        self.base_controller = BaseController()

    def create(self,provider: str):
        if provider == VectorDBEnums.QDRANT.value:
            database_path = self.base_controller.get_vector_db_instance(db_name=self.config.VECTOR_DB_PATH)
            return QdrantVectorDB(
                db_path=database_path,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD
            )
        return None


