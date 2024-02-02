from ..util import *
from ..view import *
from ..think import *
from ..act import *
from .controller import Controller
from .data_types import (
    IncommingData,
    OutGoingData,
    IncomeingExecutionReport,
    IncomeingExecutionFailure,
    Error,
    ClientResponseStatus,
    AgnetStatus,
)
from queue import Queue


class RemoteFeedController(Controller):
    def __init__(
        self,
        incoming_data_queue: Queue,
        outgoing_data_queue: Queue,
        status_queue: Queue,
        user_task: str,
        max_loops: int,
        agent_status: AgnetStatus,
    ) -> None:
        super(RemoteFeedController, self).__init__(user_task)
        self.incoming_data_queue = incoming_data_queue
        self.outgoing_data_queue = outgoing_data_queue
        self.status_queue = status_queue
        self.max_loops = max_loops
        self.message_count = 0
        self.agent_status = agent_status

    def fetch_information_on_screen(self, output_folder: str, loop_num: int):
        incoming_data: IncommingData = self.incoming_data_queue.get()
        # compute the elements on screen, current + change
        file_name_html = None

        return self.process_screen_data(
            incoming_data, output_folder, loop_num, file_name_html=file_name_html
        )

    def should_close(self, tool_executor=None):
        self.message_count = +1
        if self.message_count == self.max_loops:
            Logger.info(
                f"Session closed because execution count eached limit {self.max_loops}"
            )
            return True
        elif tool_executor is not None and isinstance(tool_executor, FinalMessage):
            Logger.info(
                f"Session closed because final answer was provided {tool_executor}"
            )
            return True
        return False

    def take_action(
        self,
        tool_executor: ToolInterface,
        tool_input,
        contains_user_input: bool,
        loop_num: int,
        output_folder: str,
    ):
        Logger.info(f"itration number {loop_num}: putting response.")

        close_request = self.should_close(tool_executor)
        response = OutGoingData(
            session_closed=close_request,
            script=tool_executor.example_script,
            tool_input=tool_input,
            force_guide=contains_user_input,
        )
        DataBase.store_server_response(
            response, context=output_folder, call_in_seassion=loop_num
        )
        self.outgoing_data_queue.put(response)

        # waiting to client response
        Logger.info(f"itration number {loop_num}: waiting for feedback from client.")
        execution_status = self.status_queue.get()

        Logger.info(
            f"itration number {loop_num}: response from client is {execution_status}"
        )
        if isinstance(execution_status,IncomeingExecutionFailure):
            raise ExecutionError(f"execution failed: {execution_status.message}")

        if close_request:
            # don't allow new connections
            self.close()
            # report the agent the exit
            execution_status.set_close()

        return execution_status

    def on_action_extraction_failed(self, loop_num: int):
        Logger.info(
            f"itration number {loop_num}: putting failed response on recoverable error."
        )
        self.outgoing_data_queue.put(
            Error(
                error_message="server_fault_retry",
                user_should_retry=True,
                session_closed=self.should_close(),
            )
        )
        Logger.info(
            f"itration number {loop_num}: after putting failed response on recoverable error."
        )

    def on_action_extraction_fatal(self, loop_num: int):
        Logger.info(
            f"itration number {loop_num}: putting failed response on non-recoverable error."
        )
        self.outgoing_data_queue.put(
            Error(
                error_message="server_fault_contact_admin",
                is_fatel=True,
                session_closed=self.should_close(),
            )
        )
        Logger.info(
            f"itration number {loop_num}: after putting failed response on non-recoverable error."
        )

    def is_closed(self):
        return self.agent_status.is_closed()

    def from_pickle(self, output_folder, loop_num):
        data = unpickle(f"{output_folder}/data_{loop_num}.pkl")
        self.incoming_data_queue.put(data)

    def close(self):
        self.agent_status.close()
