import datetime
import os
import threading

from pydantic import BaseModel


from scrape_anything.browser import *
from scrape_anything.view import *
from scrape_anything.think import *
from scrape_anything.act import *
from scrape_anything.controllers import Controller
from scrape_anything.tools import ToolBox


class Agent(BaseModel):
    llm: LLMInterface
    max_loops: int = 1
    tool_box : ToolBox = ToolBox()
    

    @staticmethod
    def clean_empty_lines(generated:str):
        return "\n".join(list(filter(lambda x: len(x.strip())>0,generated.split("\n"))))

    def get_output_folder(self):
        import uuid
        import datetime

        # Generate a UUID and replace dashes with underscores
        uuid_str = str(uuid.uuid4()).replace("-", "_")

        # Get the current date and time
        current_datetime = datetime.datetime.now()

        # Format the date and time as a string
        datetime_str = current_datetime.strftime("%H_%M_%S_%Y_%m_%d")

        # Combine the UUID and datetime
        return f"{datetime_str}x{uuid_str}"

    def run_parallel(self,controller: Controller):
        thread = threading.Thread(target=self.run,args=(controller,))
        thread.start()

        return thread
        
    def run(self, controller: Controller):
        output_folder = os.path.join("outputs",self.get_output_folder())
        os.makedirs(output_folder)
        
        on_screen = None
        try:
            previous_responses = []
            previous_responses_status = ""
            num_loops = 0
     
            on_screen,_,_,\
            screen_size,screenshot_png, _,\
                scroll_ratio,url,task_to_accomplish = controller.fetch_infomration_on_screen(output_folder,loop_num=num_loops)
            
            while True:
                num_loops += 1
                print(f"--- Iteration {num_loops} ---")
            
                generated = "parsing generation failed"
                try:
                    generated, tool, tool_input, final_answer_token = self.llm.make_a_decide_on_next_action(
                        num_loops,
                        output_folder,
                        today = datetime.date.today(),
                        site_url=url,
                        tool_description=self.tool_box.tool_description,
                        tool_names=self.tool_box.tool_names,
                        task_to_accomplish=task_to_accomplish,
                        previous_responses="\n".join(previous_responses),
                        on_screen_data=on_screen.rename_axis("index").to_csv(),
                        screen_size=screen_size,
                        scroll_ratio=scroll_ratio,
                        screenshot_png=screenshot_png
                    )
                    tool_executor = self.tool_box.get_tool(tool, tool_input,final_answer_token)
                    controller.take_action(tool_executor, tool_input,num_loops,output_folder)
                    previous_responses_status = "successful."

                # if there is an issue with the response of the LLM, update the controller and continue
                except (ValueError,KeyError) as e:
                    previous_responses_status = f"failed, {str(e)}"
                    controller.on_action_extraction_failed()
                    print(f"WARNINGS: {str(e)}")

                finally:
                    # if there is not other itreation
                    if num_loops >= self.max_loops and self.max_loops != -1: #
                        break

                    on_screen,_,_,\
                    screen_size,_, _,\
                    scroll_ratio,url,task_to_accomplish = controller.fetch_infomration_on_screen(output_folder,loop_num=num_loops)

                previous_responses.append(f"\n\nPrevious {num_loops} response:\n{self.clean_empty_lines(generated)}\nexecution status:{previous_responses_status}")
        except Exception as e:
            controller.on_action_extraction_fatal()
            raise e
        finally:
            controller.close()
