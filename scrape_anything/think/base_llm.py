from abc import abstractmethod
from pydantic import BaseModel
from typing import Tuple
from scrape_anything.util import LlmProviderError
import os

class LLMInterface(BaseModel):
    temperature: float = 0
    api_key:str = os.getenv("OPENAI_API") 

    @abstractmethod
    def make_a_decide_on_next_action(self,num_loops:int, output_folder:str,**prompt_params) -> Tuple[str,str,str,str]:     
        pass

    def safe_extract_response(self,response,*args):
        temp_response = response.copy()
        for arg in args:
            if isinstance(arg,int) and isinstance(temp_response,list) and arg < len(temp_response):
                temp_response = temp_response[arg]
            elif isinstance(arg,str) and isinstance(temp_response,dict) and arg in temp_response:
                temp_response = temp_response[arg]
            else:
                raise LlmProviderError(f"call failed to LLM provider, key {arg} missing from {response}.")
            
        return temp_response