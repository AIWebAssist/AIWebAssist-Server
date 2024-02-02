from typing import List, Dict
from pydantic import BaseModel

from scrape_anything.util.browser import *
from scrape_anything.view import *
from scrape_anything.act import *
from scrape_anything.controllers import EnabledActions
from scrape_anything.util import Logger
from scrape_anything.util.stractures import ToolDescriptionPromptValues


class ToolBox(BaseModel):
    supoorted_tools: List[ToolInterface] = [
        ClickOnCoordinates(),
        EnterText(),
        GoBack(),
        ScrollRight(),
        ScrollUp(),
        ScrollDown(),
        ScrollLeft(),
        Refresh(),
        HitAKey(),
        MessageUser(),
        FinalMessage(),
        GoToURL(),
    ]
    tools: List[ToolInterface] = EnabledActions.filter_enabled(supoorted_tools)

    @property
    def tool_description(self) -> str:
        return ToolDescriptionPromptValues(self.tools)

    @property
    def tool_names(self) -> str:
        return ",".join([tool.name for tool in self.tools])

    @property
    def tool_by_names(self) -> Dict[str, ToolInterface]:
        return {tool.name.lower(): tool for tool in self.tools}

    def extract_tool_by_name(self, tool_name):
        """clean tool name from invalid characther"""
        normlized_tool_name = tool_name.replace(".", "").lower()

        if normlized_tool_name not in self.tool_by_names:
            Logger.error(f"tool={normlized_tool_name}, is not in {self.tool_by_names}")
            raise ValueError(f"unknown tool:{normlized_tool_name}")

        return self.tool_by_names[normlized_tool_name]

    def extract(self, tool_name: str, tool_input: str) -> ToolInterface:
        Logger.info(f"tool={tool},tool_input={tool_input}")

        # grub the tool
        tool_executor = self.extract_tool_by_name(tool_name)
        # compare tool to tool input
        Logger.info(f"after processing tool inputs = {tool_input}")

        tool_input = tool_executor.process_tool_arg(**tool_input)
        return tool_executor, tool_input
