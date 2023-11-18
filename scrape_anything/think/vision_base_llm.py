import requests
import base64


from .base_llm import LLMInterface
from .io import to_text_file
from .prompts.vision_base_task_extraction import TaskExtractionVisionBasePrompt
from .response import extract_tool_and_args,parse_json

class VisionBaseLLM(LLMInterface):
    model: str = 'gpt-4-vision-preview'
    prompt_manager:TaskExtractionVisionBasePrompt = TaskExtractionVisionBasePrompt()


    def generate(self, prompt: str, screenshot:str):
        assert self.api_key != None, "please provide API key"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        base64_image = self.encode_image(screenshot)

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
    
    def encode_image(self,image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        
    def make_a_decide_on_next_action(self,num_loops:int, output_folder:str,**prompt_params):     
        prompt = self.prompt_manager.format_prompt(**prompt_params)
        final_answer_token = self.prompt_manager.get_final_answer_token()

        to_text_file(prompt,f"{output_folder}/step_{str(num_loops)}_prompt.txt")
        generated = self.generate(prompt,prompt_params.pop("screenshot_png")).replace("N/A","")
        to_text_file(generated,f"{output_folder}/step_{str(num_loops)}_response.txt")

        tool, tool_input = extract_tool_and_args(generated,final_answer_token)

        return generated, tool, parse_json(tool_input), final_answer_token