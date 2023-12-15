
from .io import to_text_file,pickle,dataframe_to_csv
from .browser import bytes_to_file
import os


class FileSystemDataBase:

    @classmethod
    def get_session_id(cls,uuid_str=None):
        import uuid
        import datetime

        # Generate a UUID and replace dashes with underscores
        uuid_str = uuid_str if uuid_str else str(uuid.uuid4()).replace("-", "_")

        # Get the current date and time
        current_datetime = datetime.datetime.now()

        # Format the date and time as a string
        datetime_str = current_datetime.strftime("%H_%M_%S_%Y_%m_%d")

        # Combine the UUID and datetime
        current = f"{datetime_str}x{uuid_str}"
        output_folder = os.path.join("outputs","datebase",current)
        os.makedirs(output_folder)
        return output_folder

    # prompt call E2E
    @classmethod
    def store_prompt(cls,prompt:str,session_id:str,call_in_seassion:int):
        to_text_file(prompt,f"{session_id}/step_{str(call_in_seassion)}_prompt.txt")

    @classmethod
    def store_response(cls,response:str,session_id:str,call_in_seassion:int):
        to_text_file(response,f"{session_id}/step_{str(call_in_seassion)}_response.txt")

    # Server call E2E
    @classmethod
    def store_client_raw_request(cls,obj,session_id:str,call_in_seassion:int):
        pickle(obj,f"{session_id}/step_{call_in_seassion}_raw_request.pkl")

    @classmethod
    def store_screenshot(cls,screenshot_stream,session_id:str,call_in_seassion:int):
        return bytes_to_file(screenshot_stream,os.path.join(session_id,f"step_{call_in_seassion+1}_screenshot.png"))

    @classmethod
    def store_server_response(cls,obj,session_id:str,call_in_seassion:int):
        pickle(obj,f"{session_id}/step_{call_in_seassion}_raw_response.pkl")

    # Html Elements filltering E2E
    @classmethod
    def store_html_elements(cls,raw_on_screen,session_id:str,call_in_seassion:int):
        dataframe_to_csv(raw_on_screen,f"{session_id}/step_{call_in_seassion+1}_raw.csv") 

    @classmethod
    def store_filltered_html_elements(cls,raw_on_screen,session_id:str,call_in_seassion:int):
        dataframe_to_csv(raw_on_screen,f"{session_id}/step_{call_in_seassion+1}_minimized.csv")

    # Agent call E2E
    @classmethod
    def store_exection_status(cls,status_message,session_id:str,call_in_seassion:int):
        to_text_file(status_message,f"{session_id}/step_{str(call_in_seassion)}_execution_status.txt")

class DataBase:

    data_base = FileSystemDataBase()

    @classmethod
    def get_session_id(cls,uuid_str=None):
        return cls.data_base.get_session_id(uuid_str=uuid_str)

    # prompt call E2E
    @classmethod
    def store_prompt(cls,prompt:str,session_id:str,call_in_seassion:int):
        cls.data_base.store_prompt(prompt,session_id,call_in_seassion)

    @classmethod
    def store_response(cls,response:str,session_id:str,call_in_seassion:int):
        cls.data_base.store_response(response,session_id,call_in_seassion)

    # Server call E2E
    @classmethod
    def store_client_raw_request(cls,obj,session_id:str,call_in_seassion:int):
        cls.data_base.store_client_raw_request(obj,session_id,call_in_seassion)

    @classmethod
    def store_screenshot(cls,screenshot_stream,session_id:str,call_in_seassion:int):
        return cls.data_base.store_screenshot(screenshot_stream,session_id,call_in_seassion)

    @classmethod
    def store_server_response(cls,obj,session_id:str,call_in_seassion:int):
        cls.data_base.store_server_response(obj,session_id,call_in_seassion)

    # Html Elements filltering E2E
    @classmethod
    def store_html_elements(cls,raw_on_screen,session_id:str,call_in_seassion:int):
        cls.data_base.store_html_elements(raw_on_screen,session_id,call_in_seassion)

    @classmethod
    def store_filltered_html_elements(cls,raw_on_screen,session_id:str,call_in_seassion:int):
        cls.data_base.store_filltered_html_elements(raw_on_screen,session_id,call_in_seassion)

    @classmethod
    def store_exection_status(cls,status_message,session_id:str,call_in_seassion:int):
        cls.data_base.store_exection_status(status_message,session_id,call_in_seassion)