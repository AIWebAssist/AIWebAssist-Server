from abc import ABC, abstractmethod
from scrape_anything.act.tool import ToolInterface
from ..view import *
from ..util import dataframe_to_csv, bytes_to_file, elements_to_table, DataBase
import pandas as pd


class Controller(ABC):
    def __init__(self, user_task: str) -> None:
        self.user_task = user_task

    @abstractmethod
    def fetch_infomration_on_screen(self, output_folder: str, loop_num: int):
        pass

    @abstractmethod
    def on_action_extraction_failed(self, loop_num: int):
        pass

    @abstractmethod
    def on_action_extraction_fatal(self, loop_num: int):
        pass

    def process_elements(
        self,
        raw_on_screen,
        output_folder,
        loop_num,
        viewpointscroll,
        viewportHeight,
        screenshot_path,
    ):
        DataBase.store_html_elements(raw_on_screen, output_folder, loop_num)
        # minimize the data sent to the llm + enrich
        on_screen = minimize_and_enrich_page_data(
            raw_on_screen, viewpointscroll, viewportHeight, screenshot_path
        )
        # store the minimized elements
        DataBase.store_filltered_html_elements(on_screen, output_folder, loop_num)

        return on_screen

    def process_screen_data(
        self, incoming_data, output_folder, loop_num, file_name_html=None
    ):
        DataBase.store_client_raw_request(
            incoming_data, session_id=output_folder, call_in_seassion=loop_num
        )

        raw_on_screen, viewpointscroll, viewportHeight, scroll_width, scroll_height = (
            elements_to_table(incoming_data.raw_on_screen),
            incoming_data.viewpointscroll,
            incoming_data.viewportHeight,
            incoming_data.scroll_width,
            incoming_data.scroll_height,
        )
        width = incoming_data.width
        height = incoming_data.height
        url = incoming_data.url
        screenshot_path = DataBase.store_screenshot(
            incoming_data.screenshot,
            session_id=output_folder,
            call_in_seassion=loop_num,
        )

        scroll_ratio = (
            f"On the Width Axis, {scroll_width}. On the Height Axis, {scroll_height}"
        )
        screen_size = f"width={width},height={height}"

        # process the elements
        on_screen = self.process_elements(
            raw_on_screen,
            output_folder,
            loop_num,
            viewpointscroll,
            viewportHeight,
            screenshot_path,
        )

        return (
            on_screen,
            viewpointscroll,
            viewportHeight,
            screen_size,
            screenshot_path,
            incoming_data.screenshot.split(",")[1],
            file_name_html,
            scroll_ratio,
            url,
            self.user_task,
        )

    def extract_from_agent_memory(self,on_screen:pd.DataFrame,screenshot_png:str,output_folder:str,num_loops:int):
        prev_on_screen:pd.DataFrame = None
        if num_loops > 1:
            prev_on_screen:pd.DataFrame = DataBase.get_last_minimized_on_screen(output_folder,num_loops)
        dataframe_changed = dataframe_diff(prev_on_screen,on_screen)

        prev_image:str = None
        if num_loops > 1:
            prev_image = DataBase.get_last_screenshot(output_folder,num_loops)
        screenshot_changed = screenshot_diff(prev_image,screenshot_png)

        return dataframe_changed, screenshot_changed
            

    @abstractmethod
    def take_action(
        self,
        tool_executor: ToolInterface,
        tool_input: str,
        num_loops: int,
        output_folder: str,
    ):
        pass

    @abstractmethod
    def is_closed(self):
        pass

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def from_pickle(self, output_folder, loop_num):
        pass
