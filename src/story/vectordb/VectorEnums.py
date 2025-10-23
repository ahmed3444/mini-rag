from enum import Enum

class VectorDBEnums( Enum):
    QDRANT = "qdrant"
    PINECONE = "pinecone"
    


class DistanceMethodEnums( Enum):
    COSINE = "cosine"
    EUCLIDEAN = "euclidean"
    DOT_PRODUCT = "dot_product"
    DOT = "dot"
    