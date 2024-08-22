import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller_fix
import random


def create_browser(gui):
    with open("browser/proxylist.txt", 'r') as file:
        proxies = file.readlines()
    PROXY = random.choice(proxies)  # Получаем случайный прокси из списка

    options = Options()
    if not gui:
        options.add_argument('--headless') # Запуск с интерфейсом или без
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('--proxy-server=%s' % PROXY)
    # Браузер и функции
    chromedriver_autoinstaller_fix.install()
    browser = webdriver.Chrome(options=options)
    print(PROXY)
    return browser

if __name__ == '__main__':
    driver = create_browser(True)
    driver.get('https://srv-go.ru/')
    time.sleep(30)
