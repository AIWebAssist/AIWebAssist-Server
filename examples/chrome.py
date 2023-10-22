from scrape_anything.browser import simulate_user_call,clear_sessions,start_browesr


def simulate_client_click(user_task):
    clear_sessions(selenium_host="selenium-chrome")
    web_driver = start_browesr(selenium_host="selenium-chrome")
    simulate_user_call(web_driver,user_task)


simulate_client_click("I need help!")