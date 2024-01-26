from scrape_anything.view.dom.filters import is_screenshot_changed
from scrape_anything.util import file_to_bytes
import os

def test_screenshot_changed():
    resources = os.path.dirname(os.path.abspath(__file__))
    screen_strem_before = file_to_bytes(os.path.join(resources,"step_1_screenshot.png"))
    screen_strem_current = file_to_bytes(os.path.join(resources,"step_2_screenshot.png"))
    assert is_screenshot_changed(screen_strem_before, screen_strem_current)

def test_screenshot1_not_changed():
    resources = os.path.dirname(os.path.abspath(__file__))
    screen_strem_before = file_to_bytes(os.path.join(resources,"step_1_screenshot.png"))
    screen_strem_current = file_to_bytes(os.path.join(resources,"step_1_screenshot.png"))
    assert not is_screenshot_changed(screen_strem_before, screen_strem_current)

def test_screenshot2_not_changed():
    resources = os.path.dirname(os.path.abspath(__file__))
    screen_strem_before = file_to_bytes(os.path.join(resources,"step_2_screenshot.png"))
    screen_strem_current = file_to_bytes(os.path.join(resources,"step_2_screenshot.png"))
    assert not is_screenshot_changed(screen_strem_before, screen_strem_current)