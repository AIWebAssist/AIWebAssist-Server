from scrape_anything.util import response
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


def test_if_llm_provide_provide_final_answer():
    sample = """
    Thought: The previous action was to close the cookie settings dialogue and it was successful. Now that the screen is clear and accessible, I will proceed to search for the name 'sefi' by entering the text into the search bar.


    Observation: I expect to see the name 'sefi' appear in the Google search bar, indicating that the text has been successfully entered.
    Final Answer: You should see the result in this page
    """
    final_token = "Final Answer"
    tool,tool_input = response.extract_tool_and_args(sample,final_token)
    
    assert tool == final_token
    assert tool_input == "You should see the result in this page"


def test_final_answer_is_ignored_if_llm_provide_action_with_it():
    sample = """
    Thought: The user has instructed to search for their name "sefi" on Google. The name has been entered already during a previous interaction as seen in the provided image. The next step is to initiate the search by clicking on the Google Search button.

    Action: Enter Text
    Action Input: {{"text":"sefi","x": 498.5,"y":400.5}}
    Observation: Expect to see a transition to the search results page with listings relevant to the search term "sefi".
    Final Answer: Once the search results are displayed, inform the user that the task has been completed.

    """
    final_token = "Final Answer"

    tool,tool_input = response.extract_tool_and_args(sample,final_token)

    assert tool == "Enter Text"
    assert json.loads(tool_input) == {"text":"sefi","x": 498.5,"y":400.5}


def test_extract_tool():
    sample = """
    Thought: The user has entered "Elon Musk twitter" into the Google search bar. The next step is to initiate the search by either clicking on the "Google Search" button or pressing the "enter" key.

    Action: Hit A Key
    Action Input: {"key":"enter"}
    Observation: After hitting the "enter" key, I expect to see a Google search results page, with possible links to Elon Musk's Twitter profile or his latest tweets.
    Final Answer: If this action leads to the search results page as intended, I would let the user know to look for the most recent tweet from Elon Musk's Twitter profile in the search results.
    """

    tool,tool_input = response.extract_tool_and_args(sample,"Final Answer")
    assert tool == "Hit A Key"
    assert json.loads(tool_input) == {"key":"enter"}
