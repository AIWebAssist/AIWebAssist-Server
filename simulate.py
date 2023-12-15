from scrape_anything.util.browser import clear_sessions,start_browesr
from main import start_server,stop_server
from simulation_utils.screen_recoding import ScreenRecorder
from simulation_utils.extension_executor import simulate_user_call
import uuid,os
import pandas as pd
import datetime

def simulate_client_click(url,user_task,recording_file,num_of_iteration=1):
    clear_sessions(selenium_host="selenium-chrome")
    web_driver = start_browesr(selenium_host="selenium-chrome")

    screen_recorder = ScreenRecorder(os.path.join("Recordings",recording_file),web_driver)
    simulate_completed = False
    try:
        screen_recorder.start_recording()
        simulate_completed = simulate_user_call(web_driver,url,user_task,num_of_iteration=num_of_iteration)
    finally:
        recording_completed = screen_recorder.stop_recording()

        return simulate_completed,recording_completed



def simulate(experiment_uuid,url,task_description,max_num_of_iteration):
    os.environ['EXPRIMENT_UUID'] = experiment_uuid
    # start the server
    start_server()
    # start calling the extension
    simulate_completed,recording_completed = simulate_client_click(url,task_description,experiment_uuid,num_of_iteration=max_num_of_iteration)
    # stop the server
    stop_server()

    return simulate_completed and recording_completed


scenarios = [
    {"url":"https://www.google.com/?hl=en","task_description":"I need to search my name in google, my name is 'sefi'","max_num_of_iteration":2},
    # {"url":"https://www.google.com/?hl=en","task_description":"help my signin my facebook account.","max_num_of_iteration":10},
    # {"url":"https://www.google.com/?hl=en","task_description":"i need to read my emails i've an account on gmail.","max_num_of_iteration":10},
    # {"url":"https://www.google.com/?hl=en","task_description":"help me find the latest twitte of elon musk?","max_num_of_iteration":10},
]

df = pd.DataFrame(scenarios)
df['uuid'] = df.apply(lambda _: str(uuid.uuid4()).replace("-", "_"), axis=1)
df['run_status'] = False

for index, row in df.iterrows():
    row['run_status'] = simulate(row['uuid'], row['url'], row['task_description'], row['max_num_of_iteration'])

df.to_csv(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_scenarios.csv")