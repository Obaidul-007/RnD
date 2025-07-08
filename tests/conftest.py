import pytest
import subprocess
import time
import requests
from playwright.sync_api import Playwright, Browser, BrowserContext, Page

@pytest.fixture(scope="session")
def app_server():
    """Start Flask app for testing"""
    # Important: Remove stdout/stderr redirection for debugging Flask output
    process = subprocess.Popen(["python", "src/app.py"])

    # Give the server some time to start up
    time.sleep(5)

    # Verify server is running
    try:
        response = requests.get("http://localhost:5000")
        assert response.status_code == 200
    except requests.exceptions.ConnectionError as e:
        print(f"\nFailed to connect to Flask app: {e}")
        # Capture and print Flask app's stdout/stderr if connection fails
        stdout, stderr = process.communicate(timeout=1) # Use communicate to get output
        print(f"Flask App stdout:\n{stdout.decode()}")
        print(f"Flask App stderr:\n{stderr.decode()}")
        pytest.fail(f"Flask app did not start correctly or respond: {e}")
    finally:
        # Yield the process for the tests to use
        yield process
        # Terminate the server after tests
        process.terminate()
        process.wait() # Ensure it's fully terminated

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720}
    }

@pytest.fixture
def page(page: Page, app_server):
    page.goto(app_server)
    return page