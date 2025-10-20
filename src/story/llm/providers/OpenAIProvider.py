from ..LLMinfernce import LLMinfernce
from ..LLMEnums import OpenAIModelEnum
from openai import OpenAI 
import logging

class OpenAIProvider(LLMinfernce):
    def __init__(self, api_key: str, api_url: str = None,
                 input_defult_max_characters: int = 1000,
                 generate_defult_max_characters_output_tokens: int = 1000,
                 defult_generation_temperature: float = 0.1):
        self.api_key=api_key
        self.api_url=api_url
        self.input_defult_max_characters=input_defult_max_characters
        self.generate_defult_max_characters_output_tokens=generate_defult_max_characters_output_tokens
        self.defult_generation_temperature=defult_generation_temperature

        self.generation_model_id=None
        self.embedding_model_id=None
        self.embedding_size=None
        self.client = OpenAI(api_key=self.api_key, api_url=self.api_url
                             )
        
        
        self.logger = logging.getLogger(__name__)

    def set_generate_model(self, model_id: str) :
        self.generation_model_id=model_id


    def set_emmbed_model(self, model_id: str, embedding_size: int ) :
        self.embedding_model_id=model_id
        self.embedding_size=embedding_size




    def generate_text(self, prompt: str, chat_history: list=[], max_output_tokens: int = None, temperature: float = None) :
        if not self.client:
            self.logger.error("OpenAI client is not set.")

        if not self.generation_model_id:
            self.logger.error("Generation model ID is not set.")

        max_output_tokens= max_output_tokens if max_output_tokens is not None else self.generate_defult_max_characters_output_tokens
        temperature= temperature if temperature is not None else self.defult_generation_temperature



        chat_history.append(
            self.construct_prompt(prompts=prompt, role=OpenAIModelEnum.USER.value)
            )
        response = self.client.chat.completions.create(
            model=self.generation_model_id,
            messages=chat_history,
            max_tokens=max_output_tokens,
            temperature=temperature
        )
        if not response or not response.choices or len(response.choices) ==0 or not response.choices[0].message:
            self.logger.error("No response data received from OpenAI.")
            return None

        return response.choices[0].message.content
    
    def process_text(self, text: str) :
        return text[:self.input_defult_max_characters].strip()
    

    def embed_text(self, text: str, document_type: str=None) :
        if not self.client:
            self.logger.error("OpenAI client is not set.")

        if not self.embedding_model_id:
            self.logger.error("Embedding model ID is not set.")
        
        response = self.client.embeddings.create(
            input=text,
            model=self.embedding_model_id,
            user=self.user_id
        )
        if  not response or response.data or len(response.data) ==0 or not response.data[0].embedding:
            self.logger.error("No embedding data received from OpenAI.")
            return None
        return response.data[0].embedding
    def construct_prompt(self, prompts: str, role: str) :

        return{
            "role": role,
            "content": self.process_text(prompts)
        }
        
