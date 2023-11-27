from queue import Queue
from .remote_feed import RemoteFeedController
from .data_types import IncommingData
from ..util import encode_image,Logger
import os

# TODO: remove patch
class DevRemoteFeedController(RemoteFeedController):

    def __init__(self, incoming_data_queue: Queue, outgoing_data_queue: Queue, status_queue: Queue, user_task: str, max_loops: int) -> None:
        Logger.warning("You are using controller which is used DEV ONLY.")
        super().__init__(incoming_data_queue, outgoing_data_queue, status_queue, user_task, max_loops)

    def fetch_infomration_on_screen(self,output_folder:str,loop_num:int):

        Logger.info("dev controller, waiting on incoming queue.")
        incoming_data:IncommingData = self.incoming_data_queue.get()
        
        # patch screenshot using selenuim
        Logger.info("encoding image")
        incoming_data.screenshot = encode_image("temp_patch.png")
        os.remove("temp_patch.png")

        Logger.info("dev controller, puting PATCHED data.")
        self.incoming_data_queue.put(incoming_data)

        return super(DevRemoteFeedController,self).fetch_infomration_on_screen(output_folder,loop_num)