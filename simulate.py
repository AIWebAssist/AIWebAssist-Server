from scrape_anything.util.browser import clear_sessions,start_browesr
from main import start_server,stop_server
import shutil

def simulate_user_call(wd,url,objective_text,num_of_iteration=1):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time
    wait = WebDriverWait(wd, 10)

    # open site
    wd.get(url)

    # 1. Open the menu
    #wd.get(f"chrome-extension://{extension_id}/main.html")
    time.sleep(2)
    wd.find_element(By.ID,"ai-assistance-circle").click()
    time.sleep(1)

    # 2. Add objective
    wd.find_element(By.ID,"objective").click()
    wd.find_element(By.ID,"objective").send_keys(objective_text) 

    # 3. Toggle on the 'switch'
    switch_element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.switch')))
    if not switch_element.is_selected():
        switch_element.click()

    current_index = 0

    while current_index < num_of_iteration:
                
        # 4. we assume the objective and switch status are preserved 
        time.sleep(2)
        # switch to extension
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit')))
        submit_button.click()

        # sleep until the button is re-enabled
        while not wd.find_element(By.ID,'submit').is_enabled():
          time.sleep(2)
        current_index+=1

        time.sleep(5)

def simulate_client_click(url,user_task,num_of_iteration=1):
    clear_sessions(selenium_host="selenium-chrome")
    web_driver = start_browesr(selenium_host="selenium-chrome")
    simulate_user_call(web_driver,url,user_task,num_of_iteration=num_of_iteration)



def simulate(url,task_description):
    # start the server
    start_server()
    # start calling the extension
    simulate_client_click(url,task_description,num_of_iteration=10)
    # stop the server
    stop_server()


scenarios = [
    {"url":"https://www.google.com/?hl=en","task_description":"I need to search my name in google, my name is 'sefi'"},
    {"url":"https://www.google.com/?hl=en","task_description":"help my signin my facebook account."},
    {"url":"https://www.google.com/?hl=en","task_description":"i need to read my emails i've an account on gmail."},
    {"url":"https://www.google.com/?hl=en","task_description":"help me find the latest twitte of elon musk?"},
]
for scenario in scenarios:
    simulate(**scenario)