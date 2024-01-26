from pydantic import BaseModel


class BaseTaskExtractionPrompt(BaseModel):
    observation_token: str = "Observation"
    guidelines: str = """
Guidelines:
    - When processing previous execution, consider if you expect the screen to change after the action.
    - In your response, make sure to describe the tool to be used by the shortest path to complete the user goal.
    - In your response, if you need any infromation from the user ask him to include the infomration in the task. Don't ask for passwords or usernames.
"""
    prompt_template: str = ""

    def format_prompt(self, **kwrgs):
        return self.prompt_template.format(
            observation_token=self.observation_token,
            guidelines=self.guidelines,
            **kwrgs
        )
