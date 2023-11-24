from scrape_anything.think import response
import json
import pytest

def test_if_llm_provide_more_then_one_extract_first():
    sample = """
    Thought: The previous action was to close the cookie settings dialogue and it was successful. Now that the screen is clear and accessible, I will proceed to search for the name 'sefi' by entering the text into the search bar.

    Action: Enter Text
    Action Input: {{"text":"sefi","x": 498.5,"y":400.5}}
    Observation: I expect to see the name 'sefi' appear in the Google search bar, indicating that the text has been successfully entered.

    ---
    Thought: After entering the search query, the next logical step is to execute the search by clicking the "Google Search" button or by pressing the "enter" key.

    Action: Hit A Key
    Action Input: {{"key":"enter"}}
    Observation: I expect the Google search to be conducted and the search results page for the query 'sefi' to be displayed.
    """
    tool,tool_input = response.extract_tool_and_args(sample,"FINAL")

    assert tool == "Enter Text"
    assert json.loads(tool_input) == {"text":"sefi","x": 498.5,"y":400.5}


def test_if_llm_provide_one_extract():
    sample = """
    Thought: The previous action was to close the cookie settings dialogue and it was successful. Now that the screen is clear and accessible, I will proceed to search for the name 'sefi' by entering the text into the search bar.

    Action: Enter Text
    Action Input: {{"text":"sefi","x": 498.5,"y":400.5}}
    Observation: I expect to see the name 'sefi' appear in the Google search bar, indicating that the text has been successfully entered.
    """
    tool,tool_input = response.extract_tool_and_args(sample,"FINAL")

    assert tool == "Enter Text"
    assert json.loads(tool_input) == {"text":"sefi","x": 498.5,"y":400.5}

def test_if_llm_provids_not_action_raise_execption():
    sample = """
    Thought: The previous action was to close the cookie settings dialogue and it was successful. Now that the screen is clear and accessible, I will proceed to search for the name 'sefi' by entering the text into the search bar.

    Action Input: {{"text":"sefi","x": 498.5,"y":400.5}}
    Observation: I expect to see the name 'sefi' appear in the Google search bar, indicating that the text has been successfully entered.
    """

    with pytest.raises(ValueError):
         response.extract_tool_and_args(sample,"FINAL")

def test_if_llm_provids_not_action_input_no_failure():
    sample = """
    Thought: The previous action was to close the cookie settings dialogue and it was successful. Now that the screen is clear and accessible, I will proceed to search for the name 'sefi' by entering the text into the search bar.

    Action: Go Back
    Observation: I expect to see the name 'sefi' appear in the Google search bar, indicating that the text has been successfully entered.
    """

    tool,tool_input = response.extract_tool_and_args(sample,"FINAL")

    assert tool == "Go Back"
    assert json.loads(tool_input) == {}
