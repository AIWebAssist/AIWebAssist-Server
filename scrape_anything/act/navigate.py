from .tool import ToolInterface

class GoBack(ToolInterface):
    """Go back to the previous page"""

    name: str = "Go Back"
    description: str = "Navigate back to the previous page. No input is required."
    example_script: str = "back"

    def process_tool_arg(self, **kwargs):
        return {}


class Refresh(ToolInterface):
    """Refresh the current page"""

    name: str = "Refresh page"
    description: str = "Refresh the current page. No input is required."
    example_script: str = "refresh"

    def process_tool_arg(self, **kwargs):
        return {}


class FinalMessage(ToolInterface):
    """The tool to use for the final answer"""

    name: str = "Final Guidance"
    description: str = 'Present final guidance on the screen to the user. This tool should be used when the users task is completed. Input format: {"message": "<text_to_display>"}'
    example_script: str = "show_final_guidance"

    def process_tool_arg(self, **kwargs):
        return {"message": kwargs["message"]}
