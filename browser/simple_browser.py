import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller_fix
import random
import os


def create_browser(gui, user_id):
    options = Options()
    if not gui:
        options.add_argument('--headless') # Запуск с интерфейсом или без
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_directory = os.path.join(script_dir, 'users')
    user_directory = os.path.join(base_directory, f'user_{user_id}')
    options.add_argument(f'user-data-dir={user_directory}')

    # Браузер и функции
    chromedriver_autoinstaller_fix.install()
    browser = webdriver.Chrome(options=options)
    return browser

if __name__ == '__main__':
    driver = create_browser(True)
    driver.get('https://srv-go.ru/')
    time.sleep(30)
