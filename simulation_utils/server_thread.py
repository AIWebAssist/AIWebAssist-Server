from scrape_anything import Server
from multiprocessing import Process


class ServerInAThread:
    process = None

    def __init__(self,experiment_uuid) -> None:
        self.experiment_uuid = experiment_uuid
   
    def start(self):
        self.process = Process(target=lambda: Server(self.experiment_uuid).start())
        self.process.start()

    def stop(self):
        self.process.terminate()
        self.process.join()
