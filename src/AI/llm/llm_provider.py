import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

class LLMProvider:
    def __init__(self):
        self.llm_model_name = str(os.getenv('LLM_MODEL_NAME'))
        self.llm_temperature = float(os.getenv('LLM_TEMPERATURE'))
        
    def llm_client(self):
        try:
            llm = ChatOllama(
                model=self.llm_model_name,
                validate_model_on_init=True,
                temperature=self.llm_temperature,
            )
            
            return llm
        except Exception as e:
            print(f"Error initializing Ollama llm_client", str(e))
            raise Exception(f"Error initializing Ollama llm_client", str(e))
        