import requests

from .base_llm import LLMInterface
from ..util.io import to_text_file
from .prompts.vision_base_task_extraction import TaskExtractionVisionBasePrompt
from ..util import extract_tool_and_args,Logger,file_to_bytes,DataBase

class VisionBaseLLM(LLMInterface):
    model: str = 'gpt-4-vision-preview'
    prompt_manager:TaskExtractionVisionBasePrompt = TaskExtractionVisionBasePrompt()


    def generate(self, prompt: str, screenshot:str):
        assert self.api_key != None, "please provide API key"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        base64_image = file_to_bytes(screenshot)

        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": f"{prompt}"
                    },
                    {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                    }
                ]
                }
            ],
            "max_tokens": 300
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json()

        return response['choices'][0]['message']['content']
    
        
    def make_a_decide_on_next_action(self,num_loops:int, output_folder:str,**prompt_params):
        Logger.info("calling make a decision.")
        # foramt prompt         
        prompt = self.prompt_manager.format_prompt(**prompt_params)
        final_answer_token = self.prompt_manager.get_final_answer_token()

        # store prompt
        DataBase.store_prompt(prompt,num_loops=num_loops, session_id=output_folder)

        Logger.info("calling LLM.")
        generated = self.generate(prompt,prompt_params.pop("screenshot_png"))
        Logger.info("got response from LLM.")

        # store reponse
        DataBase.store_response(generated,num_loops=num_loops, session_id=output_folder)

        Logger.info(f"extracting tool from = {generated}")
        tool, tool_input = extract_tool_and_args(generated.replace("N/A",""),final_answer_token)
        Logger.info(f"extracted tools are tool={tool} and tool_input={tool_input}")
        
        return generated, tool, tool_input, final_answer_token