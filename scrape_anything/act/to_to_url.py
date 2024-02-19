from .tool import ToolInterface


class GoToURL(ToolInterface):
    """Navigate to a specific URL address"""

    name: str = "Go to a specific URL web address"
    description: str = 'Change the URL to a provided address. Input format: {"url": "<place_url_here>"}'
    click_on_screen: bool = False
    example_script: str = "go_to_url"

    def process_tool_arg(self, **kwargs):
        url = kwargs["url"]
        return {"url": url}


class MessageUser(ToolInterface):
    """Display text to the user"""

    name: str = "Textual Guidance"
    description: str = (
        'Present a message to the user. Input format: {"text": "<text_to_display>"}'
    )
    click_on_screen: bool = False
    example_script: str = "show_guidance"

    def process_tool_arg(self, **kwargs):
        text = kwargs["text"]
        return {"text": text}
