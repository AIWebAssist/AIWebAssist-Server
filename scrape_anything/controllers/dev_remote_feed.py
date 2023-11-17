from .remote_feed import RemoteFeedController
from .data_types import IncommingData
from ..browser import *
import os

# TODO: remove patch
class DevRemoteFeedController(RemoteFeedController):



    def fetch_infomration_on_screen(self,output_folder:str,loop_num:int):

        incoming_data:IncommingData = self.incoming_data_queue.get()
        
        # patch screenshot using selenuim
        incoming_data.screenshot = encode_image("temp_patch.png")
        os.remove("temp_patch.png")

        self.incoming_data_queue.put(incoming_data)

        return super(DevRemoteFeedController,self).fetch_infomration_on_screen(output_folder,loop_num)