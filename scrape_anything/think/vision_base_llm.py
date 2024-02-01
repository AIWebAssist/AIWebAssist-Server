import requests

from .base_llm import LLMInterface
from ..util.io import to_text_file
from .prompts.vision_base_task_extraction import TaskExtractionVisionBasePrompt
from ..util import extract_tool_and_args, Logger, file_to_bytes, DataBase


class VisionBaseLLM(LLMInterface):
    prompt_manager: TaskExtractionVisionBasePrompt = TaskExtractionVisionBasePrompt()

    def generate(
        self, prompt: str, screenshot: str, model: str = "gpt-4-vision-preview"
    ):
        assert self.api_key != None, "please provide API key"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        base64_image = file_to_bytes(screenshot)

        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{prompt}"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            "max_tokens": 300,
        }
        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
        ).json()

        return self.safe_extract_response(response, "choices", 0, "message", "content")

    def make_a_decide_on_next_action(
        self, num_loops: int, output_folder: str, **prompt_params
    ):
        Logger.info("calling make a decision.")
        # foramt prompt
        prompt = self.prompt_manager.format_prompt(**prompt_params)

        # store prompt
        DataBase.store_prompt(prompt, call_in_seassion=num_loops, context=output_folder)

        Logger.info("calling LLM.")
        generated = self.generate(prompt, prompt_params.pop("screenshot_png"))
        Logger.info("got response from LLM.")

        return generated
