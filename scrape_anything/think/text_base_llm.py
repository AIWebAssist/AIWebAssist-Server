import openai

from .base_llm import LLMInterface
from .prompts.text_base_task_extraction import TaskExtractionTextBasePrompt
from ..util import extract_tool_and_args,Logger,DataBase

class TextOnlyLLM(LLMInterface):
    model: str = 'gpt-3.5-turbo'
    prompt_manager:TaskExtractionTextBasePrompt = TaskExtractionTextBasePrompt()

    def generate(self, prompt: str):
        assert self.api_key != None, "please provide API key"

        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            stop=self.prompt_manager.get_stop_patterns()
        )
        return self.safe_extract_response(response.to_dict(),'choices',0,'message','content')
    
    
    def make_a_decide_on_next_action(self,num_loops:int, output_folder:str, **prompt_params):
        Logger.info("calling make a decision.")
        # foramt prompt    
        prompt = self.prompt_manager.format_prompt(**prompt_params)

        # store prompt
        DataBase.store_prompt(prompt,call_in_seassion=num_loops, session_id=output_folder)

        # call LLM
        Logger.info("calling LLM.")
        generated = self.generate(prompt)
        Logger.info("got response from LLM.")


        return generated