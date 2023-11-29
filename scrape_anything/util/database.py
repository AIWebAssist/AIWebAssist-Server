
from .io import to_text_file,pickle,dataframe_to_csv
from .browser import bytes_to_file
import os

class DataBase:

    @staticmethod
    def store_prompt(prompt:str,session_id:str,call_in_seassion:int):
        to_text_file(prompt,f"{session_id}/step_{str(call_in_seassion)}_prompt.txt")

    @staticmethod
    def store_response(response:str,session_id:str,call_in_seassion:int):
        to_text_file(response,f"{session_id}/step_{str(call_in_seassion)}_response.txt")

    @staticmethod
    def store_client_raw_request(obj,session_id:str,call_in_seassion:int):
        pickle(obj,f"{session_id}/step_{call_in_seassion}_raw_request.pkl")

    @staticmethod
    def store_html_elements(raw_on_screen,session_id:str,call_in_seassion:int):
        dataframe_to_csv(raw_on_screen,f"{session_id}/step_{call_in_seassion+1}_raw.csv") 

    @staticmethod
    def store_filltered_html_elements(raw_on_screen,session_id:str,call_in_seassion:int):
        dataframe_to_csv(raw_on_screen,f"{session_id}/step_{call_in_seassion+1}_minimized.csv")

    @staticmethod
    def store_screenshot(screenshot_stream,session_id:str,call_in_seassion:int):
        return bytes_to_file(screenshot_stream,os.path.join(session_id,f"step_{call_in_seassion+1}_screenshot.png"))

    @staticmethod
    def store_exection_status(status_message,session_id:str,call_in_seassion:int):
        to_text_file(status_message,f"{session_id}/step_{str(call_in_seassion)}_execution_status.txt")