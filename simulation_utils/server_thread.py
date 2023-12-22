
from scrape_anything import Server

class ServerInAThread:
    process = None

    @class_method
    def start(cls):
        cls.process = Process(target=lambda : Server().start())
        cls.process.start()

    def stop(cls):
        cls.process.terminate()
        cls.process.join()