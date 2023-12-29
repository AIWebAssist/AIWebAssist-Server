from pydantic import BaseModel

class BaseTaskExtractionPrompt(BaseModel):
    observation_token: str = "Observation"
    guidelines:str = """
Guidelines:
    - make sure to describe the tool to be used by the shortest path to the goal.
"""
    prompt_template:str = ""
    

    def format_prompt(self, **kwrgs):
        return self.prompt_template.format(observation_token=self.observation_token,guidelines=self.guidelines,**kwrgs)