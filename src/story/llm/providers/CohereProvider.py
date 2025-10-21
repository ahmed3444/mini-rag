from ..LLMinfernce import LLMinfernce
from ..LLMEnums import CohereModelEnum,DocumentTypeEnum
import logging
import cohere


class CohereProvider(LLMinfernce):
    def __init__(self, api_key: str,
                 input_defult_max_characters: int = 1000,
                 generate_defult_max_characters_output_tokens: int = 1000,
                 defult_generation_temperature: float = 0.1):
        self.api_key=api_key

        self.input_defult_max_characters=input_defult_max_characters
        self.generate_defult_max_characters_output_tokens=generate_defult_max_characters_output_tokens
        self.defult_generation_temperature=defult_generation_temperature
        self.generation_model_id=None
        self.embedding_model_id=None
        self.embedding_size=None
    
        self.client = cohere.Client(self.api_key)
        self.logger = logging.getLogger(__name__)
    def set_generate_model(self, model_id: str) :
        self.generation_model_id=model_id


    def set_emmbed_model(self, model_id: str, embedding_size: int ) :
        self.embedding_model_id=model_id
        self.embedding_size=embedding_size


    def set_emmbed_model(self, model_id: str, embedding_size: int ) :
        self.embedding_model_id=model_id
        self.embedding_size=embedding_size

    def process_text(self, text: str) :
        return text[:self.input_defult_max_characters].strip()
    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int=None, temperature: float=None) :
        if not self.client:
            self.logger.error("Cohere client is not initialized.")
            return None
        if not self.generation_model_id:
            self.logger.error("Generation model ID is not set.")
            return None
        response=self.client.chat(
            model=self.generation_model_id,
            chat_history=chat_history,
            messages=self.process_text(prompt),
            temperature=temperature if temperature is not None else self.defult_generation_temperature,
            max_tokens=max_output_tokens if max_output_tokens is not None else self.generate_defult_max_characters_output_tokens  
        )
        if not response or not response.text:
            self.logger.error("No response data received from Cohere.")
            return None
        return response.text

    def embed_text(self, text: str, document_type: str) :
        if not self.client:
            self.logger.error("Cohere client is not initialized.")
            return None
        if not self.embedding_model_id:
            self.logger.error("Embedding model ID is not set.")
            return None

        input_type=CohereModelEnum.DOCUMENT 
        if document_type == DocumentTypeEnum.QUERY.value:
            input_type=CohereModelEnum.QUERY
        response = self.client.embed(
            model=self.embedding_model_id,
            texts=[self.process_text(text)],
            input_type=input_type,
            embedding_types=['float'])
        if not response or not response.embeddings or len(response.embeddings) ==0:
            self.logger.error("No embedding data received from Cohere.")
            return None

        return response.embeddings[0]
    def construct_prompt(self, prompts: str, role: str) :