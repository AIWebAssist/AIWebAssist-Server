
from .io import to_text_file


class DataBase():


    def store_prompt(prompt:str,session_id:str,call_in_seassion:int):
        to_text_file(prompt,f"{session_id}/step_{str(call_in_seassion)}_prompt.txt")

    def store_response(response:str,session_id:str,call_in_seassion:int):
        to_text_file(response,f"{session_id}/step_{str(call_in_seassion)}_response.txt")