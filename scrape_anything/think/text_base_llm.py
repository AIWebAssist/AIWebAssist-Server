import openai

from .base_llm import LLMInterface
from ..util.io import to_text_file
from .prompts.text_base_task_extraction import TaskExtractionTextBasePrompt
from ..util import extract_tool_and_args,Logger

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
        return response.choices[0].message.content
    
    
    def make_a_decide_on_next_action(self,num_loops:int, output_folder:str,**prompt_params):
        Logger.info("calling make a decision.")
        # foramt prompt    
        prompt = self.prompt_manager.format_prompt(**prompt_params)
        final_answer_token = self.prompt_manager.get_final_answer_token()

        # store prompt
        to_text_file(prompt,f"{output_folder}/step_{str(num_loops)}_prompt.txt")

        # call LLM
        Logger.info("calling LLM.")
        generated = self.generate(prompt).replace("N/A","")
        Logger.info("got response from LLM.")

        # store reponse
        to_text_file(generated,f"{output_folder}/step_{str(num_loops)}_response.txt")

        Logger.info(f"extracting tool from = {generated}")
        tool, tool_input = extract_tool_and_args(generated,final_answer_token)
        Logger.info(f"extracted tools are tool={tool} and tool_input={tool_input}")

        return generated, tool, tool_input, final_answer_token