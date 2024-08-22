import time

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import random


def create_browser(gui):
    with open("browser/private_proxylist.txt", 'r') as file:
        proxies = file.readlines()
    proxy = random.choice(proxies)  # Получаем случайный прокси из списка
    proxy_parametr = proxy.strip().split(':') # ip:port:login:password
    proxy_url = f"http://{proxy_parametr[2]}:{proxy_parametr[3]}@{proxy_parametr[0]}:{proxy_parametr[1]}"
    seleniumwire_options = {
        "proxy": {
            "http": proxy_url,
            "https": proxy_url,
            'no_proxy': 'localhost,127.0.0.1'
        },
    }
    options = Options()
    if not gui:
        options.add_argument('--headless') # Запуск с интерфейсом или без
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument('ignore-certificate-errors')
    options.add_argument('--allow-insecure-localhost')
    # Браузер и функции
    browser = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    seleniumwire_options=seleniumwire_options,
    options=options)

    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        'source': '''
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
      '''
    })
    print(proxy_url)
    return browser

if __name__ == '__main__':
    driver = create_browser(True)
    driver.get('https://srv-go.ru/')
    time.sleep(30)
