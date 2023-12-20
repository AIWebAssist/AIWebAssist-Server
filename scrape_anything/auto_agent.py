import datetime
import os
import threading

from pydantic import BaseModel


from scrape_anything.util import *
from scrape_anything.view import *
from scrape_anything.think import *
from scrape_anything.act import *
from scrape_anything.controllers import Controller
from scrape_anything.tools import ToolBox


class Agent(BaseModel):
    llm: LLMInterface
    max_loops: int = 1
    tool_box : ToolBox = ToolBox()
    session_id: str 
    

    def run_parallel(self,controller: Controller):
        thread = threading.Thread(target=self.run,args=(controller,))
        thread.start()

        return thread
        
    def run(self, controller: Controller):
        Logger.info(f"starting new agent of {type(controller)}, session_id ={self.session_id}")
        on_screen = None
        try:
            previous_responses = []
            num_loops = 0
     
            on_screen,_,_,\
            screen_size,screenshot_png, _,\
                scroll_ratio,url,task_to_accomplish = controller.fetch_infomration_on_screen(self.session_id,loop_num=num_loops)
            
            while True:
                num_loops += 1
                Logger.info(f"starting iteration number {num_loops}")
            
                parsing_status = False
                execution_status = False
                error_message = ""
                try:
                    
                    Logger.info(f"calling llm of type {type(self.llm)}")                    
                    raw = self.llm.make_a_decide_on_next_action(
                        num_loops,
                        self.session_id,
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

                    # store reponse
                    DataBase.store_response(raw,call_in_seassion=num_loops, session_id=self.session_id)

                    Logger.info(f"extracting tool from = {raw}")
                    tool, tool_input = extract_tool_and_args(raw.replace("N/A",""))
                    Logger.info(f"extracted tools are tool={tool} and tool_input={tool_input}")

                    # try to grab tool
                    Logger.info(f"trying to extract tool '{tool}' and tool inputs '{tool_input}' ")
                    tool_executor,tool_input = self.tool_box.extract(tool,tool_input)
                    # mark tool is well foramted
                    parsing_status = True
                    Logger.info(f"Extract tool '{type(tool_executor)}' and tool inputs '{tool_input}'.")

                    # use the tool
                    Logger.info("calling controller action.")
                    controller.take_action(tool_executor, tool_input, num_loops, self.session_id)
                    execution_status = True
                    Logger.info(f"execution completed successfully.")
                    
                # if there is an issue with the response of the LLM, update the controller and continue
                except (ValueError,KeyError,ExecutionError,LlmProviderError) as e:
                    error_message = f"failed, error: {str(e)}"

                    # if the error doesn't sources from the end client, report failure.
                    if not isinstance(e,ExecutionError):
                        Logger.error("reporting failure to controller.") 
                        controller.on_action_extraction_failed(loop_num=num_loops) 
                        Logger.error("failure reported to controller.")

                    Logger.error(f"cycle failed parsing_status={parsing_status},session_id={self.session_id} error = {error_message}")
                except Exception as e:
                    Logger.error(f"unknown execption {str(e)}") 
                    raise e
                finally:
                    # if there is not other itreation
                    if num_loops >= self.max_loops and self.max_loops != -1: #
                        Logger.info("closeing agent.")
                        break

                    on_screen,_,_,\
                    screen_size,screenshot_png, _,\
                    scroll_ratio,url,task_to_accomplish = controller.fetch_infomration_on_screen(self.session_id,loop_num=num_loops)

                    # foramt a message
                    message = f"Itreation number {num_loops} \n"
                    if not parsing_status: # if parsing failed
                        message+= f"parsing failed. The raw response = {raw}. Error message = {error_message}"
                    elif not execution_status: # exection failed
                        message+= f"execution failed. Error message = {error_message}"
                    else:
                        message+= f"execution successful. Tool used: {tool}, Tool input: {tool_input}"

                    Logger.info(f"exection number {num_loops} completed, message = {message}")
                    DataBase.store_exection_status(message,session_id=self.session_id,call_in_seassion=num_loops)
                    previous_responses.append(message)
                    
        except Exception as e:
            Logger.error(f"reporting fatel to controler, reason={str(e)}")
            controller.on_action_extraction_fatal(num_loops)            
            raise e
        finally:
            controller.close()
