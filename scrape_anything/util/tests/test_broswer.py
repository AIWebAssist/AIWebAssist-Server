from scrape_anything.util.browser import draw_on_image
from scrape_anything.view import is_screenshot_changed
from scrape_anything.util import file_to_bytes
import os
from PIL import Image


def test_draw_on_image_i_feel_lucky():
    resources = os.path.dirname(os.path.abspath(__file__))
    screen_strem_before = Image.open(os.path.join(resources, "screenshot.png"))

    output = draw_on_image(
        screen_strem_before,
        screen_width=1512,
        screen_height=815,
        **{"y": 436.5, "x": 825.5}
    )
    output.save("temp.png")

    expected = file_to_bytes(os.path.join(resources, "I_feel_lucky.png"))
    output = file_to_bytes("temp.png")

    assert not is_screenshot_changed(output, expected)
    os.remove("temp.png")


def test_draw_on_image_enter_text():
    resources = os.path.dirname(os.path.abspath(__file__))
    screen_strem_before = Image.open(os.path.join(resources, "screenshot.png"))

    output = draw_on_image(
        screen_strem_before,
        screen_width=1512,
        screen_height=815,
        **{"x": 733.5, "y": 366.5}
    )
    output.save("temp.png")

    expected = file_to_bytes(os.path.join(resources, "enter_text.png"))
    output = file_to_bytes("temp.png")

    assert not is_screenshot_changed(output, expected)
    os.remove("temp.png")
