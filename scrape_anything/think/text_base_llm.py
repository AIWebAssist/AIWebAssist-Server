import openai

from .base_llm import LLMInterface
from .prompts.base_task_extraction import BaseTaskExtractionPrompt
from .prompts.text_base_task_extraction import TaskExtractionTextBasePrompt
from ..util import extract_tool_and_args, Logger, DataBase
from scrape_anything.tools import FinalMessage


class TextOnlyLLM(LLMInterface):
    prompt_manager: BaseTaskExtractionPrompt = TaskExtractionTextBasePrompt()

    def generate(self, prompt: str, model: str):
        assert self.api_key != None, "please provide API key"

        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=self.temperature,
            stop=self.prompt_manager.get_stop_patterns(),
        )
        return self.safe_extract_response(
            response.to_dict(), "choices", 0, "message", "content"
        )

    def make_a_decide_on_next_action(
        self, num_loops: int, output_folder: str, **prompt_params
    ):
        Logger.info("calling make a decision.")
        # foramt prompt
        prompt = self.prompt_manager.format_prompt(step_num=num_loops, **prompt_params,final_anser_name=FinalMessage().name)

        # store prompt
        DataBase.store_prompt(
            prompt, call_in_seassion=num_loops, context=output_folder
        )

        # call LLM
        Logger.info("calling LLM.")
        try:
            generated = self.generate(prompt, model="gpt-3.5-turbo")
        except openai.InvalidRequestError:
            Logger.info("context to large, tring with 16k version.")
            generated = self.generate(prompt, model="gpt-3.5-turbo-16k")

        Logger.info("got response from LLM.")

        return generated
