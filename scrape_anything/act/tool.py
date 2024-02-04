from pydantic import BaseModel
from scrape_anything.util.browser import action_with_js_code
import os


class ToolInterface(BaseModel):
    name: str
    description: str
    click_on_screen: bool = False
    example_script: str = ""

    def is_click_on_screen(self) -> bool:
        return self.click_on_screen

    def use(self, web_driver: object, **kwarg) -> str:
        self.process_tool_arg(**kwarg)
        web_driver.execute_script(self.example_script, active=True, **kwarg)

    def process_tool_arg(self, **_):
        return {}

    def example(self, web_driver, *arg, **kwarg):
        self.process_tool_arg(**kwarg)
        web_driver.execute_script(self.example_script, active=False, **kwarg)