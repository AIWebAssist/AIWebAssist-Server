import base64
import io
import json
import pandas as pd
import requests
from PIL import Image, ImageDraw
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait


def start_browesr(
    dockerized=True, headless=False, selenium_host="host.docker.internal"
):
    """start browser"""
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_extension("extension.crx")

    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--lang=en")
    chrome_options.add_argument("ignore-certificate-errors")

    if headless:
        chrome_options.headless = True
        chrome_options.add_argument("--headless")
    if dockerized:
        return webdriver.Remote(
            f"http://{selenium_host}:4444/wd/hub", options=chrome_options
        )

    service = Service(executable_path=r"/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=chrome_options)


def clear_sessions(selenium_host="host.docker.internal", session_id=None):
    """
    Here we query and delete orphan sessions
    docs: https://www.selenium.dev/documentation/grid/advanced_features/endpoints/
    :return: None
    """

    url = f"http://{selenium_host}:4444"
    if not session_id:
        # delete all sessions
        r = requests.get(f"{url}/status")
        data = json.loads(r.text)
        for node in data["value"]["nodes"]:
            for slot in node["slots"]:
                if slot["session"]:
                    id = slot["session"]["sessionId"]
                    r = requests.delete(f"{url}/session/{id}")
    else:
        # delete session from params
        r = requests.delete(f"{url}/session/{session_id}")


def load_script(filepath):
    """load script from file"""
    with open(filepath, "r", encoding="utf-8") as f:
        return "".join(f.readlines())


def extract_with_js_code(wd, filepath):
    """execute script on web driver"""
    script = f"""
  var consoleLogs = [];
  var originalLog = console.log;
  console.log = function(message) {{
      consoleLogs.push(message);
      originalLog.apply(console, arguments);
  }};

  {load_script(filepath)}

  return consoleLogs;
  """
    return wd.execute_script(script)


def action_with_js_code(wd, filepath, **kwarg):
    """execute script on web driver"""
    script = load_script(filepath)
    for key in kwarg:
        script = script.replace(f"{{{key}}}", str(kwarg[key]))

    wd.execute_script(
        f"""
  {script}
  """
    )


def encode_image(file_path):
    """convert file to byte array stream"""
    with open(file_path, "rb") as image_file:
        # Read the binary image data
        binary_data = image_file.read()

        # Encode the binary data in base64
        base64_encoded = base64.b64encode(binary_data).decode("utf-8")

        # Construct the data URL
        data_url = f"data:image/png;base64,{base64_encoded}"

    return data_url


def file_to_bytes(image_path):
    """convert file to byte array"""

    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def bytes_to_file(screenshot_data, file_path):
    """convert byte array to file"""
    if not file_path.endswith(".png"):
        raise ValueError("must be a png.")

    screenshot_binary = base64.b64decode(screenshot_data.split(",")[1])

    # Save the binary image to a file or process it as needed
    with open(file_path, "wb") as f:
        f.write(screenshot_binary)

    return file_path


def web_driver_to_image(wd, file_name):
    """save screenshot of a web driver"""
    full_path = f"{file_name}.png"
    wd.save_screenshot(full_path)
    return full_path


def web_driver_to_html(wd, file_name):
    """extract html from web driver"""
    # Get the page source HTML
    html_content = wd.page_source
    full_path = f"{file_name}.html"
    # Save the HTML content to a file
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return full_path


def elements_to_table(logs):
    """convert string to dataframe"""
    df = pd.read_csv(io.StringIO(logs), sep=",", lineterminator="\n")
    for column in df.columns:
        if hasattr(df[column], "str"):
            df[column] = (
                df[column].str.replace("<comma>", ",").str.replace("<new_line>", "\n")
            )
    return df


def draw_on_screen(wd, filename, x, y, **kwarg):
    """draw x and y box in the screen"""

    # Perform mouse click at X and Y coordinates
    # Open the screenshot image using Pillow
    final_fname = f"{filename}_click_location"
    final_fname = web_driver_to_image(wd, final_fname)
    image = Image.open(final_fname)

    # Create a drawing context on the image
    draw = ImageDraw.Draw(image)

    # Define the size of the marker
    marker_size = 10

    # Draw a marker at the specified coordinates
    draw.rectangle(
        [(x - marker_size, y - marker_size), (x + marker_size, y + marker_size)],
        outline="red",
    )

    if "text" in kwarg:
        text_x = x  # X coordinate for the text (centered with the rectangle)
        text_y = y - marker_size - 20  # Y coordinate above the rectangle
        draw.text((text_x, text_y), kwarg["text"], fill="black")

    # Save the marked screenshot

    image.save(final_fname)
    return filename


def wait_for_page_load(wdriver):
    """wait until the page is loaded"""
    wait = WebDriverWait(wdriver, 60)

    def page_loaded(driver):
        return driver.execute_script("return document.readyState") == "complete"

    wait.until(page_loaded)
