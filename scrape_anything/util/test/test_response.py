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
    tool,tool_input = response.extract_tool_and_args(sample)

    assert tool == "Enter Text"
    assert tool_input == {"text":"sefi","x": 498.5,"y":400.5}


def test_if_llm_provide_one_extract():
    sample = """
    Thought: The previous action was to close the cookie settings dialogue and it was successful. Now that the screen is clear and accessible, I will proceed to search for the name 'sefi' by entering the text into the search bar.

    Action: Enter Text
    Action Input: {{"text":"sefi","x": 498.5,"y":400.5}}
    Observation: I expect to see the name 'sefi' appear in the Google search bar, indicating that the text has been successfully entered.
    """
    tool,tool_input = response.extract_tool_and_args(sample)

    assert tool == "Enter Text"
    assert tool_input == {"text":"sefi","x": 498.5,"y":400.5}

def test_if_llm_provids_not_action_raise_execption():
    sample = """
    Thought: The previous action was to close the cookie settings dialogue and it was successful. Now that the screen is clear and accessible, I will proceed to search for the name 'sefi' by entering the text into the search bar.

    Action Input: {{"text":"sefi","x": 498.5,"y":400.5}}
    Observation: I expect to see the name 'sefi' appear in the Google search bar, indicating that the text has been successfully entered.
    """

    with pytest.raises(ValueError):
         response.extract_tool_and_args(sample)

def test_if_llm_provids_not_action_input_no_failure():
    sample = """
    Thought: The previous action was to close the cookie settings dialogue and it was successful. Now that the screen is clear and accessible, I will proceed to search for the name 'sefi' by entering the text into the search bar.

    Action: Go Back
    Observation: I expect to see the name 'sefi' appear in the Google search bar, indicating that the text has been successfully entered.
    """

    tool,tool_input = response.extract_tool_and_args(sample)

    assert tool == "Go Back"
    assert tool_input == {}


def test_if_llm_provide_provide_final_answer():
    sample = """
    Thought: The previous action was to close the cookie settings dialogue and it was successful. Now that the screen is clear and accessible, I will proceed to search for the name 'sefi' by entering the text into the search bar.


    Observation: I expect to see the name 'sefi' appear in the Google search bar, indicating that the text has been successfully entered.
    Action: Final Answer
    Action Input: {{"text":"You should see the result in this page"}}
    
    """
    tool,tool_input = response.extract_tool_and_args(sample)
    
    assert tool == "Final Answer"
    assert tool_input == {"text":"You should see the result in this page"}


def test_final_answer_is_ignored_if_llm_provide_action_with_it():
    sample = """
    Thought: The user has instructed to search for their name "sefi" on Google. The name has been entered already during a previous interaction as seen in the provided image. The next step is to initiate the search by clicking on the Google Search button.

    Action: Enter Text
    Action Input: {{"text":"sefi","x": 498.5,"y":400.5}}
    Observation: Expect to see a transition to the search results page with listings relevant to the search term "sefi".
    Final Answer: Once the search results are displayed, inform the user that the task has been completed.

    """
    tool,tool_input = response.extract_tool_and_args(sample)

    assert tool == "Enter Text"
    assert tool_input == {"text":"sefi","x": 498.5,"y":400.5}


def test_extract_tool():
    sample = """
    Thought: The user wants to read their emails on Gmail. I have already clicked on the "Gmail" link in the previous iteration, which should have initiated navigation to the Gmail service. The user's expectation is to reach the Gmail inbox or sign-in page.

    Action: Refresh page

    Action Input: No input.

    Observation: I expect to either see the Gmail sign-in page or the user's inbox if they were already signed in, or potentially a loading page if the click operation is still in progress. If the refresh action leads to a re-prompt of the cookie settings, I may need to click 'Accept all' or 'Reject all' to proceed
    """

    tool,tool_input = response.extract_tool_and_args(sample)
    assert tool == "Refresh page"
    assert tool_input == {}


