from typing import List, Dict
from pydantic import BaseModel

from scrape_anything.browser import *
from scrape_anything.view import *
from scrape_anything.act import *
from scrape_anything.controllers import EnabledActions

class ToolBox(BaseModel):
    supoorted_tools: List[ToolInterface] = [ClickOnCoordinates(),EnterText(),GoBack(),ScrollRight(),ScrollUp(),ScrollDown(),Refresh(),HitAKey()]
    tools: List[ToolInterface] = EnabledActions.filter_enabled(supoorted_tools)
    
    final_answer_tool:ToolInterface = FinalAnswer


    @property
    def tool_description(self) -> str:
        return "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])

    @property
    def tool_names(self) -> str:
        return ",".join([tool.name for tool in self.tools])

    @property
    def tool_by_names(self) -> Dict[str, ToolInterface]:
        return {tool.name: tool for tool in self.tools}


    def get_tool(self, tool:str, final_answer_token:str) -> ToolInterface:
        if tool == final_answer_token:
            return FinalAnswer

        if tool not in self.tool_by_names:
            raise ValueError(f"unknown tool:{tool}")

        return self.tool_by_names[tool]