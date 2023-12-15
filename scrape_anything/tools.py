from typing import List, Dict
from pydantic import BaseModel

from scrape_anything.util.browser import *
from scrape_anything.view import *
from scrape_anything.act import *
from scrape_anything.controllers import EnabledActions
from scrape_anything.util import Logger,parse_json

class ToolBox(BaseModel):
    supoorted_tools: List[ToolInterface] = [ClickOnCoordinates(),EnterText(),GoBack(),ScrollRight(),ScrollUp(),ScrollDown(),Refresh(),HitAKey(),FinalAnswer()]
    tools: List[ToolInterface] = EnabledActions.filter_enabled(supoorted_tools)
    
    # tools that are abstracted from the agent
    final_answer_tool:ToolInterface = FinalAnswer()


    @property
    def tool_description(self) -> str:
        return "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])

    @property
    def tool_names(self) -> str:
        return ",".join([tool.name for tool in self.tools])

    @property
    def tool_by_names(self) -> Dict[str, ToolInterface]:
        return {tool.name: tool for tool in self.tools}


    def extract(self, tool:str, tool_input:str) -> ToolInterface:

        Logger.info(f"tool={tool},tool_input={tool_input}")

        if tool not in self.tool_by_names:            
            Logger.error(f"tool={tool}, is not in {self.tool_by_names}")
            raise ValueError(f"unknown tool:{tool}")
        
        # grub the tool
        tool_executor = self.tool_by_names[tool]
        # compare tool to tool input
        json_tool_input = parse_json(tool_input)
        Logger.info(f"after processing tool inputs = {json_tool_input}")

        tool_input = tool_executor.process_tool_arg(**json_tool_input)
        return tool_executor, tool_input