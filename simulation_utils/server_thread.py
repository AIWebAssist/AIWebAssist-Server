from multiprocessing import Process
from scrape_anything import Server


class ServerInAThread:
    process = None

    def __init__(self, experiment_uuid) -> None:
        self.experiment_uuid = experiment_uuid

    def _start_server(self):
        Server(self.experiment_uuid).start()

    def start(self):
        self.process = Process(target=self._start_server)
        self.process.start()

    def stop(self):
        self.process.terminate()
        self.process.join()
