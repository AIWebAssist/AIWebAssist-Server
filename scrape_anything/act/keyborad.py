from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .tool import ToolInterface


class HitAKey(ToolInterface):
    """Press a key on the keyboard"""

    name: str = "Hit A Key"
    description: str = (
        'Press one of the keys. Input format: {"key": "esc"} or {"key": "enter"}'
    )
    example_script: str = "keyboard_action"

    def process_tool_arg(self, **kwargs):
        key = kwargs["key"]
        return {"key": key}
