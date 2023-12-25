class ExecutionError(ValueError):
    """This execption thorwn when the tool execution fails"""

    pass


class LlmProviderError(ValueError):
    """This execption thorwn when the llm provider fails to generate response"""

    pass
