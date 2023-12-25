from scrape_anything import Agent
from scrape_anything import TextOnlyLLM
from scrape_anything import RemoteFeedController
from queue import Queue

user_task = (
    "log in to my account,user name is 'erlichsefi@gmail.com', password is '1234567'"
)
experiment = "outputs/08_23_18_2023_09_30x1d50316f_f6dc_4737_a434_98c6c26afc14"


feed_from_chrome = Queue(maxsize=1)
feed_from_agent = Queue(maxsize=1)

controller = RemoteFeedController(
    incoming_data_queue=feed_from_chrome,
    outgoing_data_queue=feed_from_agent,
    user_task=user_task,
)
controller.unpickle(experiment, 0)

agnet = Agent(llm=TextOnlyLLM(), max_loops=1)
thread = agnet.run_parallel(controller)

call_to_action = feed_from_agent.get()
print(call_to_action)

thread.stop()
