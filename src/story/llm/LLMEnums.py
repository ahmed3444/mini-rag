from eunm import Enum
class LLMPEnum( Enum):
    OPENAI = "OPENAI"
    ANTHROPIC = "ANTHROPIC"
    COHERE = "COHERE"
    AI21 = "AI21"
    CUSTOM = "CUSTOM"

class OpenAIModelEnum( Enum):
    SYSTEM="system"
    USER="user"
    ROLE="role"
    ASSISTANT="assistant"


class CohereModelEnum( Enum):
    SYSTEM="system"
    USER="user"
    ROLE="role"
    ASSISTANT="assistant"
    DOCUMENT="search_document"
    QUERY="search_query"    
class DocumentTypeEnum( Enum):
    DOCUMENT="document"
    QUERY="query"
