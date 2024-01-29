from .base_task_extraction import BaseTaskExtractionPrompt


class TaskExtractionTextBasePrompt(BaseTaskExtractionPrompt):
    prompt_template: str = """
Today is {today}, the site your user is looking on is '{site_url}'.

Here is a representation of the valuable elements existing on the screen:
{on_screen_data}

Current screen dimensions:
width={width} ,height={height}

Scroll Options: 
{scroll_ratio}

You should guide the user to complete the task  '{task_to_accomplish}', the tools you can use are:
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

Finally, describe your guidance to the user using the following format:

Execution Status: <comment on if the your previous executions what is successful, when making a decision consider if the the screenshot should've changed after the previous action>
Overall Task Status: <given the user task and the past execution, comment if the overall user task is completed>
Current Action Goal: <given the user task and the past execution, comment on what is the goal of the CURRENT action you are offering to the user>
Action: <the action to take, exactly one element of [{tool_names}]>
Action Input: <the input to the action you provided, MUST be a json form>
Next Action Goal: <given the user task, the past execution and current task, comment on what will be the goal of the next action you will offer.>
{observation_token}: <the change you expect to see after the action is executed>
--
The current iteration number is {step_num}.
"""

    def get_stop_patterns(self):
        return [f"\n{self.observation_token}", f"\n\t{self.observation_token}"]
