import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from browser.stable_browser import create_browser
from config import load_config
from selenium_checks.check import is_element_clickable



class EPD_BOT:
    def __init__(self):
        # Create a browser instance
        self.browser = create_browser(True)
        self.wait = WebDriverWait(self.browser, 5).until

    def authorization(self, login, password):
        # Open the login page
        self.browser.get(
            'https://esia.epd-portal.ru/auth/signin?OauthKey=dfeb0c2d-6a60-466f-b207-33e95c30d446&client=EOPP')

        if is_element_clickable(self, By.CSS_SELECTOR, '.gosuslugi-btn'):
            self.browser.find_element(By.CSS_SELECTOR, '.gosuslugi-btn').click()

            # Find the login and password input fields
            if is_element_clickable(self, By.ID, 'login'):
                login_input = self.wait(EC.presence_of_element_located((By.ID, 'login')))
                login_input.send_keys(login)
            password_input = self.wait(EC.presence_of_element_located((By.ID, 'password')))
            # Enter the login and password
            password_input.send_keys(password)
            # Submit the login form
            password_input.send_keys(Keys.ENTER)
            text_frame = self.wait(EC.presence_of_element_located((By.CLASS_NAME, 'text-plain')))
            print(text_frame.text)

            # В этом месте отправка запроса в бот и ожидание ответа пользователя

            time.sleep(30)

        # Wait for the page to load
        self.wait(EC.element_to_be_clickable((By.ID, 'mat-expansion-panel-header-1'))).click()
        self.wait(EC.element_to_be_clickable((By.CLASS_NAME, 'role'))).click()
        self.wait(EC.element_to_be_clickable((By.CLASS_NAME, 'system-redirect-links-item-title'))).click()
        self.wait(EC.element_to_be_clickable((By.ID, 'mat-expansion-panel-header-1'))).click()
        self.wait(EC.element_to_be_clickable((By.CLASS_NAME, 'role'))).click()
        time.sleep(300)

        return self.browser


if __name__ == '__main__':
    config = load_config()
    epd = EPD_BOT()
    epd.authorization(config.gos_usl.login, config.gos_usl.password)

