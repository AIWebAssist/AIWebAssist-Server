from .browser import run_js_code


def screen_to_window_dim(wd):
    logs = run_js_code(wd,"window.js")
    assert len(logs) == 2
    viewpointscroll = int(logs[0])
    viewportHeight = int(logs[1])

    return viewpointscroll,viewportHeight

def screen_to_table(wd):
  import pandas as pd
  import io

  logs = run_js_code(wd,"elements.js")
  try:
     return pd.read_csv(io.StringIO("\n".join(logs)), sep=",")
  except Exception as e:
    print(f"WARNING:\n On Table Data: {logs}\n Error {e}")
    return pd.read_csv(io.StringIO("\n".join(logs)), sep=",",on_bad_lines="skip")
  

def get_scroll_height(web_driver):
  import time
  initial_scroll_position = web_driver.execute_script("return window.pageYOffset")

  # Scroll down a bit
  web_driver.execute_script("window.scrollBy(0, 100);")

  # Wait for a brief moment
  time.sleep(1)

  # Get the scroll position after scrolling down
  scroll_down_position = web_driver.execute_script("return window.pageYOffset")

  # Scroll up to the initial position
  web_driver.execute_script(f"window.scrollTo(0, {initial_scroll_position});")

  # Wait for a brief moment
  time.sleep(1)

  # Scroll up a bit
  web_driver.execute_script("window.scrollBy(0, -100);")

  # Wait for a brief moment
  time.sleep(1)

  # Get the scroll position after scrolling up
  scroll_up_position = web_driver.execute_script("return window.pageYOffset")

  # Scroll back to the initial position
  web_driver.execute_script(f"window.scrollTo(0, {initial_scroll_position});")

  # Compare the scroll positions
  if scroll_down_position > initial_scroll_position or scroll_up_position < initial_scroll_position:
      return "Client can scroll both up and down!"
  elif scroll_down_position > initial_scroll_position:
      return "Client can scroll down!"
  elif scroll_up_position < initial_scroll_position:
      return "Client can scroll up!"
  else:
      return "Client cannot scroll either up or down!"

def get_scroll_width(web_driver):
    import time
    initial_scroll_position = web_driver.execute_script("return window.pageXOffset")

    # Scroll right a bit
    web_driver.execute_script("window.scrollBy(100, 0);")

    # Wait for a brief moment
    time.sleep(1)

    # Get the scroll position after scrolling right
    scroll_right_position = web_driver.execute_script("return window.pageXOffset")

    # Scroll left to the initial position
    web_driver.execute_script(f"window.scrollTo({initial_scroll_position}, 0);")

    # Wait for a brief moment
    time.sleep(1)

    # Scroll left a bit
    web_driver.execute_script("window.scrollBy(-100, 0);")

    # Wait for a brief moment
    time.sleep(1)

    # Get the scroll position after scrolling left
    scroll_left_position = web_driver.execute_script("return window.pageXOffset")

    # Scroll back to the initial position
    web_driver.execute_script(f"window.scrollTo({initial_scroll_position}, 0);")

    # Compare the scroll positions
    if scroll_right_position > initial_scroll_position or scroll_left_position < initial_scroll_position:
        return "Client can scroll both left and right!"
    elif scroll_right_position > initial_scroll_position:
        return "Client can scroll right!"
    elif scroll_left_position < initial_scroll_position:
        return "Client can scroll left!"
    else:
        return "Client cannot scroll either left or right!"


def get_scroll_options(web_driver):
    width = get_scroll_width(web_driver)
    height = get_scroll_height(web_driver)
    return f"On the Width Axis, {width}. On the Height Axis, {height}"