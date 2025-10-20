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
