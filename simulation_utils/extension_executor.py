def simulate_user_call(wd, url, objective_text, num_of_iteration=1):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time

    wait = WebDriverWait(wd, 10)

    # open site
    wd.get(url)

    # 1. Open the menu
    # wd.get(f"chrome-extension://{extension_id}/main.html")
    time.sleep(2)
    wd.find_element(By.ID, "ai-assistance-circle").click()
    time.sleep(1)

    # 2. Add objective
    wd.find_element(By.ID, "objective").click()
    wd.find_element(By.ID, "objective").send_keys(objective_text)

    # 3. Toggle on the 'switch'
    switch_element = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".switch"))
    )
    if not switch_element.is_selected():
        switch_element.click()

    current_index = 0

    while current_index < num_of_iteration:
        # 4. we assume the objective and switch status are preserved
        time.sleep(2)
        # switch to extension
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, "submit")))
        submit_button.click()

        # sleep until the button is re-enabled
        while not wd.find_element(By.ID, "submit").is_enabled():
            time.sleep(2)
        current_index += 1

        time.sleep(5)
