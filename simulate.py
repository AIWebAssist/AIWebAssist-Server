from scrape_anything.util.browser import clear_sessions, start_browesr
from simulation_utils.server_thread import ServerInAThread
from simulation_utils.screen_recoding import ScreenRecorder
from simulation_utils.extension_executor import simulate_user_call
import uuid
import os
import shutil
import pandas as pd
import datetime
from scrape_anything.util.logger import Logger
from webdriver_manager.chrome import ChromeDriverManager
import requests


def simulate_client_click(
    url, user_task, recording_file, num_of_iteration=1, dockerized=True
):
    if dockerized:
        clear_sessions(selenium_host="selenium-chrome")
    else:
        executable_path = ChromeDriverManager().install()

    web_driver = start_browesr(
        selenium_host="selenium-chrome",
        dockerized=dockerized,
        executable_path=executable_path,
    )
    web_driver.maximize_window()

    screen_recorder = ScreenRecorder(
        os.path.join("outputs", "recordings", recording_file), web_driver
    )
    simulate_completed = False
    screen_recorder.start_recording()
    try:
        simulate_completed = simulate_user_call(
            web_driver, url, user_task, num_of_iteration=num_of_iteration
        )
    except Exception:
        Logger.error_execption("Simulation call failed")
    finally:
        recording_completed = screen_recorder.stop_recording()

    return simulate_completed, recording_completed


def simulate(
    experiment_uuid, url, task_description, max_num_of_iteration, dockerized=True
):
    # start the server
    server = ServerInAThread(experiment_uuid)
    server.start()
    # start calling the extension
    simulate_completed, recording_completed = simulate_client_click(
        url,
        task_description,
        experiment_uuid,
        num_of_iteration=max_num_of_iteration,
        dockerized=dockerized,
    )
    # stop the server
    server.stop()

    if not (simulate_completed and recording_completed):
        Logger.error(
            f"Simulation failed. simulate_completed={simulate_completed},recording_completed={recording_completed}"
        )

    Logger.copy_log_file(experiment_uuid)

    return simulate_completed and recording_completed


if __name__ == "__main__":
    scenarios = [
        # {
        #     "url": "https://www.google.com/?hl=en",
        #     "task_description": "I need to search my name in google, my name is 'sefi'",
        #     "max_num_of_iteration": 5,
        # },
        {
            "url": "https://www.google.com/?hl=en",
            "task_description": "help my signin my facebook account.",
            "max_num_of_iteration": 5,
        },
        {
            "url": "https://www.google.com/?hl=en",
            "task_description": "i need to read my emails i've an account on gmail.",
            "max_num_of_iteration": 5,
        },
        {
            "url": "https://www.google.com/?hl=en",
            "task_description": "help me find the latest twitte of elon musk?",
            "max_num_of_iteration": 5,
        },
    ]
    dockerized_selenuim = False

    df = pd.DataFrame(scenarios)
    df["uuid"] = df.apply(lambda _: str(uuid.uuid4()).replace("-", "_"), axis=1)
    df["run_status"] = False

    for index, row in df.iterrows():
        row["run_status"] = simulate(
            row["uuid"],
            row["url"],
            row["task_description"],
            row["max_num_of_iteration"],
            dockerized=dockerized_selenuim,
        )

    experiment_date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    df.to_csv(os.path.join("outputs", experiment_date + "_scenarios.csv"))
    shutil.make_archive(experiment_date, "zip", "outputs")
