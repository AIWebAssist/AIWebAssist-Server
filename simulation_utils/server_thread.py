from scrape_anything import Server
from multiprocessing import Process


class ServerInAThread:
    process = None

    @classmethod
    def start(cls):
        cls.process = Process(target=lambda: Server().start())
        cls.process.start()

    @classmethod
    def stop(cls):
        cls.process.terminate()
        cls.process.join()
