import os
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth
import chromedriver_autoinstaller_fix
import time


def get_random_chrome_user_agent():
    user_agent = UserAgent()
    return user_agent.random


def create_browser(user_id=1):
    chromedriver_autoinstaller_fix.install()
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_directory = os.path.join(script_dir, 'users')
    user_directory = os.path.join(base_directory, f'user_{user_id}')

    options.add_argument(f'user-data-dir={user_directory}')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_argument('--no-sandbox')
    # options.add_argument('--headless')

    browser = webdriver.Chrome(options=options)
    ua = get_random_chrome_user_agent()
    stealth(driver=browser,
            user_agent=ua,
            languages=["ru-RU", "ru"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            run_on_insecure_origins=True
            )

    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
      '''
    })
    return browser


def main_login(user_id=1):
    browser = create_browser(user_id)
    url_main = "https://srv-go.ru/"
    browser.get(url_main)
    time.sleep(350)

main_login()
