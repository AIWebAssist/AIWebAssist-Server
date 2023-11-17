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
