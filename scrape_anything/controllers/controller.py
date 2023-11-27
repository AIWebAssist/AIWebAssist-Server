from abc import ABC, abstractmethod
from scrape_anything.act.tool import ToolInterface
from ..view import *
import os


class Controller(ABC):

    def __init__(self,user_task:str) -> None:
        self.user_task = user_task

    @abstractmethod
    def fetch_infomration_on_screen(self,output_folder:str,loop_num:int):
        pass


    def process_screen_data(self,incoming_data,output_folder,loop_num,file_name_html=None):

        raw_on_screen, viewpointscroll,viewportHeight,scroll_width,scroll_height = self.elements_to_table(incoming_data.raw_on_screen),incoming_data.viewpointscroll,incoming_data.viewportHeight,incoming_data.scroll_width,incoming_data.scroll_height
        width = incoming_data.width
        height = incoming_data.height
        url = incoming_data.url
        screenshot_path =  self.bytes_to_file(incoming_data.screenshot,os.path.join(output_folder,f"screenshot_{loop_num+1}.png"))

        scroll_ratio = f"On the Width Axis, {scroll_width}. On the Height Axis, {scroll_height}"
        screen_size = f"width={width},height={height}"
        # store the raw elements before processing
        self.dataframe_to_csv(raw_on_screen,f"{output_folder}/step_{loop_num+1}_raw.csv") 


        # minimize the data sent to the llm + enrich
        on_screen = minimize_and_enrich_page_data(raw_on_screen,viewpointscroll,viewportHeight,screenshot_path)
        # store the minimized elements
        self.dataframe_to_csv(on_screen,f"{output_folder}/step_{loop_num+1}_minimized.csv") 
        
        
        return on_screen,viewpointscroll,viewportHeight,screen_size,screenshot_path,file_name_html,scroll_ratio,url,self.user_task
    
    def bytes_to_file(self,screenshot_data,file_path):
        if not file_path.endswith(".png"):
            raise ValueError("must be a png.")

        import base64
        screenshot_binary = base64.b64decode(screenshot_data.split(',')[1])

        # Save the binary image to a file or process it as needed
        with open(file_path, 'wb') as f:
            f.write(screenshot_binary)
        
        return file_path
    
    def dataframe_to_csv(self,df,csv_filename):
        _df = df.copy()
        for column in _df.columns:
            if hasattr(_df[column],'str'):
                    _df[column] = _df[column].str.replace(",","<comma>").str.replace("\n","<new_line>")
        _df.to_csv(csv_filename,index=False,)

    def elements_to_table(self,logs):
        import pandas as pd
        import io
        try:
            df = pd.read_csv(io.StringIO(logs), sep=",",lineterminator="\n")
            for column in df.columns:
                if hasattr(df[column],'str'):
                    df[column] = df[column].str.replace("<comma>",",").str.replace("<new_line>","\n")
            return df
        except Exception as e:
            raise Exception("Can't parse script output.")

    def pickle(self,output_folder,loop_num,data):
        import pickle

        # Pickle the dictionary and save it to a file
        with open(f"{output_folder}/data_{loop_num}.pkl", 'wb') as file:
            pickle.dump(data, file)

    def unpickle(self,output_folder,loop_num):
        import pickle
        with open(f"{output_folder}/data_{loop_num}.pkl", 'rb') as file:
            return pickle.load(file)
        
    @abstractmethod
    def take_action(self,tool_executor:ToolInterface, tool_input:str,num_loops:int,output_folder:str):
        pass

    @abstractmethod
    def is_closed(self):
        pass
    
    @abstractmethod
    def close(self):
        pass
