from pydantic import BaseModel

class TaskExtractionVisionBasePrompt(BaseModel):

    final_answer_token:str = "Final Answer"
    observation_token:str = "Observation"
    #THOUGHT_TOKEN = "Thought:"

    prompt_template:str = f"""
Today is {{today}}, the site you're looking on is {{site_url}}.

Your user instraction is: "{{task_to_accomplish}}", attacted is the screen the user see and here are the relevent elements:
{{on_screen_data}}

You should guide the user to complete the task given to you using the following tools:
{{tool_description}}

--
Previous executions:
{{previous_responses}}
---

Use the following format:
Thought: Comment on what you want to do next.
Action: The action to take, exactly one element of [{{tool_names}}]
Action Input: The input to the action
{observation_token}: The change you expect to see after the action is executed.
{final_answer_token}: Your final message to the user if you think there task was accomplished.
    """

    def get_stop_patterns(self):
        return [f'\n{self.observation_token}', f'\n\t{self.observation_token}']

    def get_final_answer_token(self):
        return self.final_answer_token

    def format_prompt(self,**kwrgs):
        return  self.prompt_template.format(**kwrgs)
