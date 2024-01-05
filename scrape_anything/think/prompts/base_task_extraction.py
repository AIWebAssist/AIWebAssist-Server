from pydantic import BaseModel

class BaseTaskExtractionPrompt(BaseModel):
    observation_token: str = "Observation"
    guidelines:str = """
Guidelines:
    - make sure to describe the tool to be used by the shortest path to the goal.
    - if you need any infromation from the user, ask him to include the infomration in the task, don't ask for passwords or usernames.
"""
    prompt_template:str = ""
    

    def format_prompt(self, **kwrgs):
        return self.prompt_template.format(observation_token=self.observation_token,guidelines=self.guidelines,**kwrgs)