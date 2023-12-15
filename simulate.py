from scrape_anything.util.browser import clear_sessions,start_browesr
from main import start_server,stop_server
from simulation_utils.screen_recoding import ScreenRecorder
from simulation_utils.extension_executor import simulate_user_call


def simulate_client_click(url,user_task,num_of_iteration=1):
    clear_sessions(selenium_host="selenium-chrome")
    web_driver = start_browesr(selenium_host="selenium-chrome")

    screen_recorder = ScreenRecorder("test",web_driver)
    screen_recorder.start_recording()
    simulate_user_call(web_driver,url,user_task,num_of_iteration=num_of_iteration)
    screen_recorder.stop_recording()



def simulate(url,task_description):
    # start the server
    start_server()
    # start calling the extension
    simulate_client_click(url,task_description,num_of_iteration=2)
    # stop the server
    stop_server()


scenarios = [
    {"url":"https://www.google.com/?hl=en","task_description":"I need to search my name in google, my name is 'sefi'"},
    # {"url":"https://www.google.com/?hl=en","task_description":"help my signin my facebook account."},
    # {"url":"https://www.google.com/?hl=en","task_description":"i need to read my emails i've an account on gmail."},
    # {"url":"https://www.google.com/?hl=en","task_description":"help me find the latest twitte of elon musk?"},
]
for scenario in scenarios:
    simulate(**scenario)