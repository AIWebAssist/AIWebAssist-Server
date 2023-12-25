from .tool import ToolInterface


class ClickOnCoordinates(ToolInterface):
    """Click on certain coordinate on the screen"""

    name: str = "Click on coordinates on the screen"
    description: str = 'click on the horizontal axis and the vertical axis, x is horizontal,y is vertical. Input format: {{"x": <place_num_here>,"y":<place_num_here>}}'
    click_on_screen: bool = True
    example_script: str = "click_coordinates"

    def process_tool_arg(self, **kwarg):
        return {
            "x": kwarg["x"],
            "y": kwarg["y"],
        }


class EnterText(ToolInterface):
    """Click on a field and enter text"""

    name: str = "Enter Text"
    description: str = 'Click on a field and enter text, Input format: {{"text":"<text_to_enter>","x": <place_num_here>,"y":<place_num_here>}}'
    click_on_screen: bool = True
    example_script: str = "click_coordinates_add_text"

    def process_tool_arg(self, **kwarg):
        text = kwarg["text"]
        return {"x": kwarg["x"], "y": kwarg["y"], "text": text}
