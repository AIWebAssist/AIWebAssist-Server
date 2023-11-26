from .tool import ToolInterface

class GoBack(ToolInterface):
    """go back to previous page"""

    name:str = "Go Back"
    description:str = "Go back to the previous page,no input."
    example_script:str = "back"

    def process_tool_arg(self,**kwarg):
      return {}





class Refresh(ToolInterface):
    """go back to previous page"""

    name:str = "Refresh page"
    description:str = "refresh the current page,no input."
    example_script:str  = "refresh"

    def process_tool_arg(self,**kwarg):
      return {}
    

class FinalAnswer(ToolInterface):
    """the tool to use in the final answer"""

    name:str = "Final Guidance"
    description:str = "present on the screen final guidance to the user, Input format: {{\"message\":\"<text to present to the user>\"}} "
    example_script:str  = "show_guidance"

    def process_tool_arg(self,**kwarg):
      return {"message":kwarg['message']}

