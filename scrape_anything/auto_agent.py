import datetime
import threading
import traceback

from pydantic import BaseModel
from typing import List

from scrape_anything.util import *
from scrape_anything.view import *
from scrape_anything.think import *
from scrape_anything.act import *
from scrape_anything.controllers import Controller
from scrape_anything.tools import ToolBox
from scrape_anything.controllers.data_types import (
    ClientResponseStatus,
    LLMResponseParsingStatus,
)


class Agent(BaseModel):
    llm: LLMInterface
    max_loops: int = 1
    tool_box: ToolBox = ToolBox()
    context: str

    def run_parallel(self, controller: Controller):
        thread = threading.Thread(target=self.run, args=(controller,))
        thread.start()

        return thread

    def run(self, controller: Controller):
        Logger.info(
            f"starting new agent of {type(controller)}, context ={self.context}"
        )

        on_screen = None
        num_loops = 0
        try:
            previous_responses = ExecutionStatusPromptValues()

            while num_loops <= self.max_loops or self.max_loops == -1:
                num_loops += 1
                Logger.info(f"starting iteration number {num_loops}")

                (
                    on_screen,
                    _,
                    _,
                    width,
                    height,
                    screenshot_png,
                    screenshot_stream,
                    _,
                    scroll_ratio,
                    url,
                    task_to_accomplish,
                ) = controller.fetch_information_on_screen(
                    self.context, loop_num=num_loops
                )

                _, screenshot_changed = controller.extract_from_agent_memory(
                    on_screen, screenshot_stream, self.context, num_loops
                )

                if not previous_responses.is_empty():
                    previous_responses.on_new_screenshot(screenshot_changed)

                parsing_status = LLMResponseParsingStatus.Failed
                execution_status = ClientResponseStatus.Failed
                error_message = ""
                try:
                    Logger.info(f"calling llm of type {type(self.llm)}")
                    raw = self.llm.make_a_decide_on_next_action(
                        num_loops,
                        self.context,
                        today=datetime.date.today(),
                        site_url=url,
                        tool_description=self.tool_box.tool_description,
                        tool_names=self.tool_box.tool_names,
                        task_to_accomplish=task_to_accomplish,
                        previous_responses=previous_responses,
                        on_screen_data=DataFramePromptValues(on_screen),
                        width=width,
                        height=height,
                        scroll_ratio=scroll_ratio,
                        screenshot_png=screenshot_png,
                    )

                    # store response
                    DataBase.store_response(
                        raw, call_in_seassion=num_loops, context=self.context
                    )

                    Logger.info(f"extracting tool from = {raw}")
                    tool, tool_input, current_task, next_task = extract_tool_and_args(
                        raw.replace("N/A", "")
                    )
                    Logger.info(
                        f"extracted tools are tool={tool} and tool_input={tool_input}"
                    )

                    # try to grab tool
                    Logger.info(
                        f"trying to extract tool '{tool}' and tool inputs '{tool_input}' "
                    )
                    tool_executor, tool_input = self.tool_box.extract(tool, tool_input)
                    # mark tool is well formatted
                    parsing_status = LLMResponseParsingStatus.Successful
                    Logger.info(
                        f"Extract tool '{type(tool_executor)}' and tool inputs '{tool_input}'."
                    )

                    controller.mark_on_screenshot(
                        tool_executor,
                        screen_width=width,
                        screen_height=height,
                        context=self.context,
                        call_in_seassion=num_loops,
                        **tool_input,
                    )
                    # use the tool
                    Logger.info("calling controller action.")
                    execution_status = controller.take_action(
                        tool_executor, tool_input, num_loops, self.context
                    )
                    Logger.info(f"execution completed successfully.")

                # handle exceptions
                except (ValueError, KeyError, ExecutionError, LlmProviderError) as e:
                    error_message = f"failed, error: {str(e)}"

                    if not isinstance(e, ExecutionError):
                        Logger.error("reporting failure to controller.")
                        controller.on_action_extraction_failed(loop_num=num_loops)
                        Logger.error("failure reported to controller.")

                    Logger.error(
                        f"cycle failed parsing_status={parsing_status},\n"
                        f"context={self.context},\n"
                        f"error = {error_message}\n"
                    )

                except Exception as e:
                    Logger.error(
                        f"unknown exception {str(e)}: {traceback.format_exc()}"
                    )
                    raise e

                # format a message
                current_status = None
                if (
                    parsing_status == LLMResponseParsingStatus.Failed
                ):  # if parsing failed
                    current_status = FailedLLMUnderstandingStepExecution(
                        num_loops,
                        raw,
                        error_message,
                        action_description=current_task,
                        on_succeed_next_action_description=next_task,
                    )
                elif (
                    execution_status == ClientResponseStatus.Failed
                ):  # execution failed
                    current_status = FailedStepExecution(
                        num_loops,
                        error_message,
                        tool,
                        tool_input,
                        action_description=current_task,
                        on_succeed_next_action_description=next_task,
                    )
                else:
                    current_status = SuccessfulStepExecution(
                        num_loops,
                        tool,
                        tool_input,
                        action_description=current_task,
                        on_succeed_next_action_description=next_task,
                    )

                Logger.info(
                    f"execution number {num_loops} completed, response {current_status}"
                )
                DataBase.store_exection_status(
                    str(current_status),
                    context=self.context,
                    call_in_seassion=num_loops,
                )
                previous_responses.append(current_status)

                # if the client closed, exit.
                if execution_status == ClientResponseStatus.Close:
                    Logger.info("Status close was detected, exiting.")
                    break

        except Exception as e:
            Logger.error(
                f"reporting fatal to controller, reason={str(e)},{traceback.format_exc()}"
            )
            controller.on_action_extraction_fatal(num_loops)
            raise e

        finally:
            controller.close()
