from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .tool import ToolInterface


class HitAKey(ToolInterface):
    """Click on a field and enter text"""

    name: str = "Hit A Key"
    description: str = (
        'Hit on of the keys,  Input format: {{"key":"esc"}} or {{"key":"enter"}}'
    )
    example_script: str = "keyborad_action"

    def process_tool_arg(self, **kwarg):
        key = kwarg["key"]
        return {"key": key}
