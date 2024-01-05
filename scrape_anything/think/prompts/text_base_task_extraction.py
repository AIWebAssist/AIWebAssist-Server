from .base_task_extraction import BaseTaskExtractionPrompt


class TaskExtractionTextBasePrompt(BaseTaskExtractionPrompt):
    prompt_template:str = """
Today is {today}, the site your user is looking on is '{site_url}'.

Here is a representation of the valuable elements existing on the screen:
{on_screen_data}

Current screen dimensions:
{screen_size}

Scroll Options: 
{scroll_ratio}

You should guide the user to complete the task '{task_to_accomplish}', the tools you can use are:
{tool_description}

Consider the previous executions to refine your response.
{previous_responses}

{guidelines}
---
Describe all Input Field:
  1. Element Index
  2. Coordinates
  3. Current Value
  4. Purpose

Describe all Buttons:
  1. Element Index
  2. Coordinates
  3. Purpose

Finally, describe your guideance to the user using the following format:

Question: <the input question you must answer>
Thought: <comment on what you want to do next>
Execution Status: <comment on if the your previous executions what is successful>
Current Task: <comment on given the task and the past execution, what it your current goal>
Action: <the action to take, exactly one element of [{tool_names}]>
Action Input: <the input to the action>
{observation_token}: <the change you expect to see after the action is executed>
"""
        

    def get_stop_patterns(self):
        return [f"\n{self.observation_token}", f"\n\t{self.observation_token}"]
