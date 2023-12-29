from .base_task_extraction import BaseTaskExtractionPrompt


class TaskExtractionVisionBasePrompt(BaseTaskExtractionPrompt):
    
    prompt_template:str = """
Today is {today}, the site you're looking on is {site_url}.

Your user instraction is: "{task_to_accomplish}", attacted is the screen the user see and here are the relevent elements:
{on_screen_data}

You should guide the user to complete the task given to you using the following tools:
{tool_description}

{guidelines}
--
Previous executions:
{previous_responses}
---

Use the following format:
Thought: Comment on what you want to do next.
Action: The action to take, exactly one element of [{tool_names}]
Action Input: The input to the action
{observation_token}: The change you expect to see after the action is executed.
    """
        

    def get_stop_patterns(self):
        return [f"\n{self.observation_token}", f"\n\t{self.observation_token}"]
