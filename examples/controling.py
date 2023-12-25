from scrape_anything import Agent
from scrape_anything import TextOnlyLLM
from scrape_anything import WebDriverController


controller = WebDriverController(
    "https://www.wishingwell.co.il/",
    user_task="log in to my account,user name is 'erlichsefi@gmail.com', password is '1234567'",
    cache_to_pickle=True,
)
agnet = Agent(llm=TextOnlyLLM(), max_loops=10)
agnet.run(controller)
