from .base_task_extraction import BaseTaskExtractionPrompt


class TaskExtractionTextBasePrompt(BaseTaskExtractionPrompt):
    prompt_template: str = """
Today is {today}. 
Your goal is to guide the user browsing the web to complete the task he will describe to you, additionally, you will be provided with information about the webpage and past executions of yourself and their success states.

{guidelines}

<START SITE DETAILS>
The URL in the naviagation bar: '{site_url}'.
CSV representation of the valuable elements existing on the screen:
{on_screen_data}

Screen window dimensions:
width={width} ,height={height}

Borwser scroll bar options: 
{scroll_ratio}

<END SITE DETAILS>

<START TOOLS YOU CAN USE>
{tool_description}
<END TOOLS YOU CAN USE>

<START PAST EXECUTIONS>
{previous_responses}
<END PAST EXECUTIONS>

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

Execution Status: <given the user task and the previous executions, were past executions was successful? What are the implications on the user task?>
Overall Task Status: <given the user task and the past execution, comment if the overall user task was completed, Yes or No. If No, provide a reason>
Current Action Goal: <given the overall task status, comment on what action you will offer the user to do, just one step.>
Action: <given the overall task status, the action to take, exactly one element of [{tool_names}], if the user task is completed, guide the user to view it with {final_anser_name}>
Action Input: <the input to the action you provided, MUST be a JSON form>
Next Action Goal: <given the user task, the past execution, and the current task, comment on what will be the goal of the next action you will offer.>
{observation_token}: <the change you expect to see after the action is executed>
--
The current iteration number is {step_num}, and the task described by the user is '{task_to_accomplish}'. 
"""

    def get_stop_patterns(self):
        return [f"\n{self.observation_token}", f"\n\t{self.observation_token}"]
