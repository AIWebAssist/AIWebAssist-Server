from scrape_anything.browser import simulate_user_call,clear_sessions,start_browesr
from examples.api import start_server

def simulate_client_click(url,user_task):
    clear_sessions(selenium_host="selenium-chrome")
    web_driver = start_browesr(selenium_host="selenium-chrome")
    simulate_user_call(web_driver,url,user_task)


start_server()
simulate_client_click("https://www.google.com/?hl=en","I Need to search my name in google, my name is 'sefi'")