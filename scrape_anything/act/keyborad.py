from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .tool import ToolInterface


class HitAKey(ToolInterface):
    """Click on a field and enter text"""

    name:str = "Hit A Key"
    description:str = "Hit on of the keys,  Input format: {{\"text\":\"esc\"}} or {{\"text\":\"enter\"}}"
    example_script:str = "keyborad_action"

    def use(self, web_driver: object, text: str) -> None:
        if text.lower() == "esc":
            webdriver.ActionChains(web_driver).send_keys(Keys.ESCAPE).perform()

        elif text.lower() == "enter":
            webdriver.ActionChains(web_driver).send_keys(Keys.ESCAPE).perform()


    def process_tool_arg(self,**kwarg):
      key = kwarg['key']
      return {
        "x":kwarg['x'],
        "y":kwarg['y'],
        "text":key
      }
