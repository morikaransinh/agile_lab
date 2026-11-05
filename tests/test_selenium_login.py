import os
import shutil
import threading
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from werkzeug.serving import make_server

from app import app


@pytest.fixture(scope="module")
def live_server():
    server = make_server("127.0.0.1", 0, app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
    thread.join(timeout=5)


@pytest.fixture
def browser():
    chrome_candidates = [
        os.environ.get("CHROME_BIN"),
        shutil.which("chrome"),
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
    ]
    if os.name == "nt":
        chrome_candidates.extend(
            [
                str(
                    Path(os.environ.get("ProgramFiles", ""))
                    / "Google"
                    / "Chrome"
                    / "Application"
                    / "chrome.exe"
                ),
                str(
                    Path(os.environ.get("ProgramFiles(x86)", ""))
                    / "Google"
                    / "Chrome"
                    / "Application"
                    / "chrome.exe"
                ),
                str(
                    Path(os.environ.get("LOCALAPPDATA", ""))
                    / "Google"
                    / "Chrome"
                    / "Application"
                    / "chrome.exe"
                ),
            ]
        )
    if not any(path and Path(path).is_file() for path in chrome_candidates):
        pytest.skip("Chrome is not installed; install Chrome to run the Selenium tests.")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    try:
        driver = webdriver.Chrome(options=options)
    except WebDriverException as error:
        pytest.skip(f"Chrome and a compatible driver are required: {error.msg}")
    yield driver
    driver.quit()


@pytest.mark.selenium
def test_successful_login_shows_dashboard(browser, live_server):
    browser.get(f"{live_server}/login")
    browser.find_element(By.ID, "username").send_keys("demo")
    browser.find_element(By.ID, "password").send_keys("demo123")
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    heading = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "dashboard-title"))
    )
    assert heading.text == "Welcome, demo!"


@pytest.mark.selenium
def test_invalid_login_shows_error(browser, live_server):
    browser.get(f"{live_server}/login")
    browser.find_element(By.ID, "username").send_keys("demo")
    browser.find_element(By.ID, "password").send_keys("wrong")
    browser.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

    message = WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-testid='flash-message']"))
    )
    assert message.text == "Invalid username or password."
