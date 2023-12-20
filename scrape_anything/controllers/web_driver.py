from ..util import *
from ..view import *
from ..think import *
from ..act import *
from .controller import Controller
from .data_types import IncommingData
from selenium.common.exceptions import WebDriverException
import time
import sys


class WebDriverController(Controller):
    def __init__(self, url, user_task: str, cache_to_pickle=False) -> None:
        super(WebDriverController, self).__init__(user_task)
        try:
            clear_sessions(selenium_host="selenium-chrome")
            self.web_driver = start_browesr(selenium_host="selenium-chrome")
            self.web_driver.set_window_size(1024, 768)
            self.web_driver.get(url)
            self.url = url
            self.cache_to_pickle = cache_to_pickle
        except Exception as e:
            self.close()
            raise e

    def fetch_infomration_on_screen(self, output_folder: str, loop_num: int):
        # compute the elements on screen, current + change
        (
            raw_on_screen,
            viewpointscroll,
            viewportHeight,
            scroll_width,
            scroll_height,
        ) = get_screen_information(self.web_driver)
        # get screen size
        width, height = get_screen_size(self.web_driver)
        url = get_url(self.web_driver)

        file_name_png = web_driver_to_image(
            self.web_driver, f"{output_folder}/step_{loop_num+1}"
        )
        screenshot = encode_image(file_name_png)

        screen_data = IncommingData(
            url=url,
            task="{task}",
            viewpointscroll=viewpointscroll,
            viewportHeight=viewportHeight,
            scroll_width=scroll_width,
            scroll_height=scroll_height,
            width=width,
            height=height,
            raw_on_screen=raw_on_screen,
            screenshot=screenshot,
        )
        if self.cache_to_pickle:
            self.pickle(
                output_folder=output_folder, loop_num=loop_num, data=screen_data
            )

        file_name_html = web_driver_to_html(
            self.web_driver, f"{output_folder}/step_{loop_num+1}"
        )

        return self.process_screen_data(
            screen_data, output_folder, loop_num, file_name_html=file_name_html
        )

    def take_action(
        self,
        tool_executor: ToolInterface,
        tool_input: str,
        num_loops: int,
        output_folder: str,
    ):
        initial_page_url = self.web_driver.current_url

        if tool_executor.is_click_on_screen():
            draw_on_screen(
                self.web_driver, f"{output_folder}/step_{str(num_loops)}", **tool_input
            )
        try:
            tool_executor.example(self.web_driver, **tool_input)
            time.sleep(4)
            tool_executor.use(self.web_driver, **tool_input)
        except WebDriverException as e:
            message_without_session_id = str(e).split("\n")[0]
            raise ValueError(f"tool execution failed,{message_without_session_id}")

        after_tool_url = self.web_driver.current_url

        need_to_wait = initial_page_url != after_tool_url
        # if the tool worked, wait and sample the site again.
        if need_to_wait:
            wait_for_page_load(self.web_driver)

    def on_action_extraction_failed(self, loop_num: int):
        pass

    def on_action_extraction_fatal(self, loop_num: int):
        sys.exit(1)

    def is_closed(self):
        return (self.web_driver != None) or (self.web_driver.is_closed())

    def close(self):
        try:
            if self.web_driver != None:
                self.web_driver.close()
                self.web_driver.quit()
        except UnboundLocalError:
            raise ValueError("please start server")
