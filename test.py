import os
from dotenv import load_dotenv
load_dotenv()

from browserpilot.agents.gpt_selenium_agent import GPTSeleniumAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import tempfile

instructions = """Go to Google.com
Find all textareas.
Find the first visible textarea.
Click on the first visible textarea.
Type in "buffalo buffalo buffalo buffalo buffalo" and press enter.
Wait 2 seconds.
Find all anchor elements that link to Wikipedia.
Click on the first one.
Wait for 10 seconds."""

# Create a temporary directory for Chrome data
temp_dir = tempfile.mkdtemp()

# Create Chrome options dictionary with user data directory
chrome_options = {
    'no-sandbox': None,
    'disable-dev-shm-usage': None,
    'disable-gpu': None,
    # 'headless': None, # The headless mode is typically used for:
                        # Running tests in CI/CD pipelines
                        # Server environments without displays
                        # Scenarios where visual feedback isn't needed
    'remote-debugging-port': '9222',
    'disable-extensions': None,
    'disable-software-rasterizer': None,
    'disable-web-security': None,
    'user-data-dir': temp_dir  # Set custom user data directory
}

# Kill existing Chrome processes
import subprocess
try:
    subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'], capture_output=True)
    subprocess.run(['taskkill', '/F', '/IM', 'chromedriver.exe'], capture_output=True)
except:
    pass

# Create agent with the updated options
agent = GPTSeleniumAgent(
    instructions,
    ChromeDriverManager().install(),
    chrome_options
)

try:
    agent.run()
finally:
    # Clean up the temporary directory
    import shutil
    try:
        shutil.rmtree(temp_dir)
    except:
        pass