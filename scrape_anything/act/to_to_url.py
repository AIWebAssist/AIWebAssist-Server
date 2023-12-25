from .tool import ToolInterface


class GoToURL(ToolInterface):
    """Go to a specific url address"""

    name: str = "Go to a specific url web address"
    description: str = (
        'Change the url to a provied URL. Input format: {{"url":"<place_url_here>"}}'
    )
    click_on_screen: str = True
    example_script: str = "go_to_url"

    def process_tool_arg(self, **kwarg):
        url = kwarg["url"]
        return {"text": url}


class FinalAnswer(ToolInterface):
    """Go to a specific url address"""

    name: str = "Your final message to the user if you think there is not more Actions to accomplished. "
    description: str = 'Present to the user the final message. Input format: {{"text":"<final_message_here>"}}'
    click_on_screen: str = True
    example_script: str = "show_guidance"

    def process_tool_arg(self, **kwarg):
        text = kwarg["text"]
        return {"text": text}
