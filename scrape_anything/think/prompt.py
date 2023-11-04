FINAL_ANSWER_TOKEN = "Final Answer:"
OBSERVATION_TOKEN = "Observation:"
THOUGHT_TOKEN = "Thought:"

PROMPT_TEMPLATE = """
Today is {today}, the site you're looking on is {site_url}.

Here is a representation of the valuable elements existing on the screen:
{on_screen_data}

Current screen dimensions: 
{screen_size}

Scroll Options: 
{scroll_ratio}

You should guide the user to complete the task given to you using the following tools:
{tool_description}

--
Use the following format:

Question: The input question you must answer.
Thought: Comment on what you want to do next.
Input Field: The coordinates and the values of elements that accept input on screen and What there are used for? if None return ""
Buttons: The coordinates of the buttons on screen and what they are used for? if None return ""
Links: The coordinate of the links on the screen and what they are used for? if None return ""
Execution Status: Comment on if the your previous executions what is successful.
Action: The action to take, exactly one element of [{tool_names}]
Action Input: The input to the action
Observation: The change you expect to see after the action is executed.

Begin!
--
Task To Accomplish: {task_to_accomplish}
Previous executions:
{previous_responses}
"""

def get_stop_patterns():
    return [f'\n{OBSERVATION_TOKEN}', f'\n\t{OBSERVATION_TOKEN}']

def get_final_answer_token():
    return FINAL_ANSWER_TOKEN

def format_prompt(**kwrgs):
    return  PROMPT_TEMPLATE.format(**kwrgs)
