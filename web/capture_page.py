from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

def screenshot_url(url: str, output_path: str, minimum_delay: float | None = None):
    """
    Opens a headless browser, navigates to a given URL, waits for the page to fully load,
    optionally delays further if specified, and captures a screenshot to the given file path.

    :param url: The webpage URL to capture.
    :param output_path: The file path (absolute or relative) to save the screenshot as a .png file.
    :param minimum_delay: Optional delay (in seconds) to wait after initial page load. Default is None.
    :raises ValueError: If output_path does not end in '.png'
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
