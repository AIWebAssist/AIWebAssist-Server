import openai
import os

from pydantic import BaseModel
from typing import List
from .io import to_text_file
from .prompts.text_base_task_extraction import TaskExtractionTextBasePrompt
from .response import extract_tool_and_args,parse_json

class ChatLLM(BaseModel):
    model: str = 'gpt-3.5-turbo'
    temperature: float = 0
    api_key:str = os.getenv("OPENAI_API") 
    prompt_manager:TaskExtractionTextBasePrompt = TaskExtractionTextBasePrompt()

    def _generate(self, prompt: str):
        assert self.api_key != None, "please provide API key"

        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            stop=self.prompt_manager.get_stop_patterns()
        )
        return response.choices[0].message.content
    

    def generate(self,prompt: str, output_folder:str,num_loops:int):
        to_text_file(prompt,f"{output_folder}/step_{str(num_loops)}_prompt.txt")
        generated = self._generate(prompt)

        to_text_file(generated,f"{output_folder}/step_{str(num_loops)}_response.txt")
        return generated
    
    def make_a_decide_on_next_action(self,num_loops:int, output_folder:str,**prompt_params) -> str:     
        prompt = self.prompt_manager.format_prompt(**prompt_params)
        final_answer_token = self.prompt_manager.get_final_answer_token()

        generated = self.generate(prompt,output_folder,num_loops).replace("N/A","")

        tool, tool_input = extract_tool_and_args(generated,final_answer_token)

        return generated, tool, parse_json(tool_input), final_answer_token