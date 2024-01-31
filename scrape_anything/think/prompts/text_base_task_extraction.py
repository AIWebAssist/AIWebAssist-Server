from .base_task_extraction import BaseTaskExtractionPrompt


class TaskExtractionTextBasePrompt(BaseTaskExtractionPrompt):
    prompt_template: str = """
Today is {today}, the site your user is looking on is '{site_url}'. Your Goal is to guide the user browsering the web to complete is task.

Here is a representation of the valuable elements existing on the screen:
{on_screen_data}

Current screen dimensions:
width={width} ,height={height}

Scroll Options: 
{scroll_ratio}

The tools you can use are:
{tool_description}

Previous executions:
{previous_responses}

{guidelines}
---
Describe all Input Fields:
  1. Element Index
  2. Coordinates
  3. Current Value
  4. Purpose

Describe all Buttons:
  1. Element Index
  2. Coordinates
  3. Purpose

Finally, describe your guidance to the user using the following format:

Execution Status: <given the user task and the previous executions was successful and what is the implications on the user task?>
Overall Task Status: <given the user task and the past execution, comment if the overall user task is completed, Yes or No, if No, provide a reason>
Current Action Goal: <given the user task and execution status, comment on what is the goal of the action you are CURRENTLY offering to the user to do>
Action: <the action to take, exactly one element of [{tool_names}], if the task is completed guide the user to view it with {final_anser_name}>
Action Input: <the input to the action you provided, MUST be a json form>
Next Action Goal: <given the user task, the past execution and current task, comment on what will be the goal of the next action you will offer.>
{observation_token}: <the change you expect to see after the action is executed>
--
The current iteration number is {step_num}, the task described by the user is '{task_to_accomplish}', 
"""

    def get_stop_patterns(self):
        return [f"\n{self.observation_token}", f"\n\t{self.observation_token}"]
