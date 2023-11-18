from abc import abstractmethod
from pydantic import BaseModel
from typing import Tuple
import os

class LLMInterface(BaseModel):
    temperature: float = 0
    api_key:str = os.getenv("OPENAI_API") 

    @abstractmethod
    def make_a_decide_on_next_action(self,num_loops:int, output_folder:str,**prompt_params) -> Tuple[str,str,str,str]:     
        pass