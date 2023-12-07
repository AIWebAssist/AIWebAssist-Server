from scrape_anything.util.browser import web_driver_to_image,clear_sessions,start_browesr
from examples.api import start_server,stop_server

def simulate_user_call(wd,url,objective_text,num_of_iteration=1):
    from selenium.webdriver.common.by import By
    import time

    # open site
    wd.get(url)

    # open extension
    #wd.execute_script("window.open('');") 
    #wd.switch_to.window(wd.window_handles[1])

    # get the extension id
    #wd.get('Chrome://extensions')
    #extension_id = wd.execute_script("return chrome.management.getAll();")[0]['id']

    # 1. Add objective
    #wd.get(f"chrome-extension://{extension_id}/main.html")
    time.sleep(2)
    wd.find_element(By.ID,"ai-assistance-circle").click()
    time.sleep(1)
    wd.find_element(By.ID,"objective").click()
    wd.find_element(By.ID,"objective").send_keys(objective_text) 

    # 2. Toggle on the 'switch'
    switch_element = wd.find_element(By.CSS_SELECTOR,'.switch')
    if not switch_element.is_selected():
        switch_element.click()

    current_index = 0
    while current_index < num_of_iteration:
        
        web_driver_to_image(wd,"temp_patch") # TODO: remove patch
        
        time.sleep(2)
        # switch to extension
        submit_button = wd.find_element(By.ID,'submit')
        submit_button.click()

        # sleep until the button is re-enabled
        while not wd.find_element(By.ID,'submit').is_enabled():
          time.sleep(2)
        current_index+=1

def simulate_client_click(url,user_task,num_of_iteration=1):
    clear_sessions(selenium_host="selenium-chrome")
    web_driver = start_browesr(selenium_host="selenium-chrome")
    simulate_user_call(web_driver,url,user_task,num_of_iteration=num_of_iteration)


# start the server
start_server()
# start calling the extension
simulate_client_click("https://www.google.com/?hl=en","I Need to search my name in google, my name is 'sefi'",num_of_iteration=10)
# stop the server
stop_server()