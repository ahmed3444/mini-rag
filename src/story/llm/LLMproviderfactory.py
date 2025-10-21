from .LLMEnums import LLMProviderEnum
from .providers.OpenAIProvider import OpenAIProvider
from .providers.CohereProvider import CohereProvider
class LLMProviderFactory:
    def __init__(self, config: dict):
        self.config = config
    def create(self,provider: str):
        if provider == LLMProviderEnum.OPENAI.value:
            return OpenAIProvider(
                api_key=self.config.get("OPENAI_API_KEY"),
                api_url=self.config.get("OPENAI_API_URL"),
                input_defult_max_characters=self.config.get("INPUT_DEFAULT_MAX_CHARACTERS",1000),
                generate_defult_max_characters_output_tokens=self.config.get("GENERATION_DEFAULT_MAX_TOKENS",1000),
                defult_generation_temperature=self.config.get("GENERATION_DEFAULT_TEMPERATURE",0.1)
            )
        elif provider == LLMProviderEnum.COHERE.value:
            return CohereProvider(
                api_key=self.config.get("COHERE_API_KEY"),
                input_defult_max_characters=self.config.get("INPUT_DEFAULT_MAX_CHARACTERS",1000),
                generate_defult_max_characters_output_tokens=self.config.get("GENERATION_DEFAULT_MAX_TOKENS",1000),
                defult_generation_temperature=self.config.get("GENERATION_DEFAULT_TEMPERATURE",0.1)
            )
        return None
       
