from scrape_anything.tools import ToolBox
import json

NO_INPUT_INSTRACTION = "no input"
INSTRACTION_TO_REPLACED_WITH_NUMBER = "<place_num_here>"
INSTRACTION_TO_REPLACED_WITH_STRING = "<text_to_enter>"
def test_tool_parsing_with_description():
    for tool in ToolBox().tools:
       
        if NO_INPUT_INSTRACTION not in tool.description:
            excepted_format = "{"+tool.description.split("{")[-1].split("}")[0]+"}"
            excepted_format_after_populated = excepted_format.replace(
                    INSTRACTION_TO_REPLACED_WITH_NUMBER,"1").replace(
                    INSTRACTION_TO_REPLACED_WITH_STRING,"ENTERD TEXT")
            
            json_tools = json.loads(excepted_format_after_populated)
            tool.process_tool_arg(**json_tools)




