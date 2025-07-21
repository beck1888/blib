"""
capture_page.py

Provides a utility function to capture a screenshot of a webpage using a headless browser.

This module contains:
- screenshot_url: Captures a screenshot of a given URL and saves it as a PNG file.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

def screenshot_url(url: str, output_path: str, minimum_delay: float | None = None):
    """
    Captures a screenshot of a webpage using a headless Chrome browser.

    Args:
        url (str): The URL of the webpage to capture.
        output_path (str): The file path (absolute or relative) to save the screenshot as a PNG file.
                           Must end with '.png'.
        minimum_delay (float | None, optional): Additional delay (in seconds) to wait after the page 
                                                loads. Defaults to None.

    Raises:
        ValueError: If the output_path does not end with '.png'.
        selenium.common.exceptions.WebDriverException: If there is an issue with the browser setup or execution.
    """
    if not output_path.lower().endswith(".png"):
        raise ValueError("Output file must end in '.png'")

    # Setup headless Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # 'new' headless mode (better rendering)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")

    # Launch headless browser
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(url)
        # Optional delay to allow additional loading time
        if minimum_delay and minimum_delay > 0:
            import time
            time.sleep(minimum_delay)
        # Wait until the page reports it's fully loaded
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )
        # Wait for content to load (optional - could add explicit waits)
        driver.implicitly_wait(5)
        driver.save_screenshot(output_path)
