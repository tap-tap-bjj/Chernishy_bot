import time
import undetected_chromedriver as uc


def create_browser():
    browser = uc.Chrome(headless=False, use_subprocess=True)
    return browser

if __name__ == '__main__':
    driver = create_browser()
    driver.get('https://srv-go.ru/')
    time.sleep(30)