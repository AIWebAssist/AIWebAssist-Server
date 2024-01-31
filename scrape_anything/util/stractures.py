from typing import List
from enum import Enum
import json
from abc import ABC,abstractmethod


class ToolDescriptionPromptValues:
    def __init__(self, tools: List) -> None:
        self.tools = tools

    def __str__(self) -> str:
        return "\n".join([f"{tool.name}: {tool.description}" for tool in self.tools])

class ExecutionStringMethod(Enum):
    JSON = "to_json"
    NL = "to_nl"

class ExecutionStatusPromptValues:
    def __init__(self) -> None:
        self.previous_executions = list()
        self.how = ExecutionStringMethod.NL

    def is_empty(self):
        return len(self.previous_executions) == 0

    def append(self, execution_status):
        self.previous_executions.append(execution_status)

    def on_new_screenshot(self, is_screen_changed):
        self.previous_executions[-1].on_screen_changed(is_screen_changed)

    def __str__(self) -> str:
        method_name = self.how.value
        func = getattr(self, method_name,None)
        if func is None:
            raise ValueError()
        return func()
    
    def to_json(self):
        exections = ",\n".join(list(map(str, self.previous_executions)))
        return f"""[
{exections}
]"""
    
    def to_nl(self):
        return "\n".join(list(map(lambda x: x.to_nl(), self.previous_executions)))


class ExecutionStep(ABC):
    def __init__(self, num_loop, action_description) -> None:
        self.num_loop = num_loop
        self.action_description = action_description
        self.screen_changed = None
        self.how = ExecutionStringMethod.NL

    def on_screen_changed(self, is_screen_changed):
        self.screen_changed = is_screen_changed

    def values(self):
        response = {
            "iteration_number": self.num_loop - 1,
            "action_goal": self.action_description,
        }
        if self.screen_changed is not None:
            response["is_screen_changed_after_action"] = self.screen_changed
        return response

    def __str__(self) -> str:
        method_name = self.how.value
        func = getattr(self, method_name,None)
        if func is None:
            raise ValueError()
        return func()
    
    def to_json(self):
        return json.dumps(self.values(), indent=2)
    
    @abstractmethod
    def to_nl(self):
        pass


class FailedLLMUnderstandingStepExecution(ExecutionStep):
    def __init__(self, num_loop, raw, error_message, action_description) -> None:
        super(FailedLLMUnderstandingStepExecution, self).__init__(
            num_loop, action_description
        )
        self.error_message = error_message
        self.raw = raw

    def values(self):
        return {
            **super(FailedLLMUnderstandingStepExecution, self).values(),
            "execution_success": False,
            "parsing_success": False,
            "related_data": self.raw,
            "error_message": self.error_message,
        }
    
    def to_nl(self):
        return f"On Iteration #{self.num_loop - 1} you've failed to {self.action_description} because your response '{self.error_message}'"


class FailedStepExecution(ExecutionStep):
    def __init__(
        self, num_loop, error_message, tool, tool_input, action_description
    ) -> None:
        super(FailedStepExecution, self).__init__(num_loop, action_description)
        self.error_message = error_message
        self.tool = tool
        self.tool_input = tool_input

    def values(self):
        return {
            **super(FailedStepExecution, self).values(),
            "execution_success": False,
            "parsing_success": True,
            "related_data": {"tool": self.tool, "tool_input": self.tool_input},
            "error_message": self.error_message,
        }
    
    def to_nl(self):
        message = f"On Iteration #{self.num_loop - 1} you've failed to {self.action_description} because the tool you've offerd {self.tool} with the params {self.tool_input} wasn't able to be executed because '{self.error_message}'"
        if self.screen_changed is not None and self.screen_changed:
            message+= "however, the screen changed."
        return message


class SuccessfulStepExecution(ExecutionStep):
    def __init__(self, num_loop, tool, tool_input, action_description) -> None:
        super(SuccessfulStepExecution, self).__init__(num_loop, action_description)
        self.tool = tool
        self.tool_input = tool_input

    def values(self):
        return {
            **super(SuccessfulStepExecution, self).values(),
            "execution_success": True,
            "related_data": {"tool": self.tool, "tool_input": self.tool_input},
        }
    
    def to_nl(self):
        if self.screen_changed is not None and self.screen_changed:
            return f"On Iteration #{self.num_loop - 1} you've successfully completed this action '{self.action_description}'"
        elif self.screen_changed is None:
            return f"On Iteration #{self.num_loop - 1} you've successfully completed this action, waiting for screen data to validate."
        else:
            return f"On Iteration #{self.num_loop - 1} action '{self.action_description}' wasn't successfully since the screen wasn't affected."


class DataFramePromptValues:
    def __init__(self, on_screen) -> None:
        self.on_screen = on_screen

    def __str__(self) -> str:
        return self.on_screen.rename_axis("index").to_csv(float_format=f"%.2f")
