from config import load_config

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from twocaptcha import TwoCaptcha
import requests
import time


class Captcha:
    def __init__(self, browser):
        #self.dict_resut = {}
        self.browser = browser
        self.two_cup_token = load_config().token.captcha_token
        self.wait = WebDriverWait(self.browser, 5)

    def sender_solve(self, path):
        try:
            solver = TwoCaptcha(self.two_cup_token)
            # bot.send_message(chat_id=chat_id_my, text='2) Изображение отправленно для разгадывания:')
            print('2) Изображение отправленно для разгадывания:')
            result = solver.normal(path, param='ru')
            # bot.send_message(chat_id=chat_id_my, text=f'3) От API пришёл ответ: {result}')
            print(f'3) От API пришёл ответ: {result}')
            # API вернёт словарь {'captchaId': '72447681441', 'code': 'gbkd'}
            # Обновляем словарь для дальнейшего извлечения ID капчи и отправки репорта
            #self.dict_resut.update(result)
            return result['code']
        except Exception as e:
            print(f'Ошибка в sender_solve: {e}')


    def captcha(self):
        try:
            # Переключаемся на iframe капчи
            WebDriverWait(self.browser, 5).until(EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[title='SmartCaptcha checkbox widget']")))

            # Ожидаем кнопку и кликаем по ней
            WebDriverWait(self.browser, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[class="CheckboxCaptcha-Button"]'))).click()

            # Возвращаемся к основному коду на странице
            self.browser.switch_to.default_content()

            # Переключаемся на новый iframe с картинкой
            WebDriverWait(self.browser, 5).until(EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[title='SmartCaptcha advanced widget']")))

            # Хардкодим имя картинки
            img_names = 'screenshot\img_yandex.png'
            with open(img_names, 'wb') as file:
                # Извлекаем атрибут src из тега в котором хранится ссылка на изображение
                img = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'img[alt="Задание с картинкой"]'))).get_attribute(
                    'src')
                # Делаем простой requests запрос для скачивания картинки и её записи в файл
                file.write(requests.get(img).content)
                # bot.send_message(chat_id=chat_id_my, text=f'1) url image: {img}')
                print('Poluchena kartinka capcha')

            cod = Captcha.sender_solve(self, path=img_names)
            # bot.send_message(chat_id=chat_id_my, text=f'4) {dict_resut["code"]}')
            print(f'4) {cod}')

            # Вставлям необходимую часть словаря dict_resut в котором лежит разгаданное слова с капчи
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.Textinput-Control'))).send_keys(
                cod)
            time.sleep(1)

            # Кликаем на кнопку отправить
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.CaptchaButton_view_action'))).click()

            # Возвращаемся к основному коду на странице
            self.browser.switch_to.default_content()

            return self.browser

        except Exception as E:
            # Ошибка возникла, записываем сообщение в журнал
            print("Произошла ошибка в капче: %s", str(E))
            # browser.py.save_screenshot(screenshot_fail)
            # Отправляем сообщение в чат бота
            # bot.send_message(chat_id=chat_id_my, text=f"Ошибка в капче: {str(E)}")

    def captcha_test(self):
        try:
            # Переключаемся на iframe капчи
            WebDriverWait(self.browser, 5).until(EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[title='SmartCaptcha checkbox widget']")))

            # Ожидаем кнопку и кликаем по ней
            WebDriverWait(self.browser, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[class="CheckboxCaptcha-Button"]'))).click()

            # Возвращаемся к основному коду на странице
            self.browser.switch_to.default_content()

            # Переключаемся на новый iframe с картинкой
            WebDriverWait(self.browser, 5).until(EC.frame_to_be_available_and_switch_to_it(
                (By.CSS_SELECTOR, "iframe[title='SmartCaptcha advanced widget']")))
            # Хардкодим имя картинки
            img_names = 'screenshot\img_yandex.png'

            while True:
                with (open(img_names, 'wb') as file):
                    # Извлекаем атрибут src из тега в котором хранится ссылка на изображение
                    img = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'img[alt="Задание с картинкой"]'))
                    ).get_attribute('src')
                    # Делаем простой requests запрос для скачивания картинки и её записи в файл
                    file.write(requests.get(img).content)
                    print('Poluchena kartinka capcha')

                cod = Captcha.sender_solve(self, path=img_names)

                print(f'4) {cod}')

                # Вставлям необходимую часть словаря dict_result в котором лежит разгаданное слова с капчи
                self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.Textinput-Control'))).send_keys(
                    cod)
                time.sleep(1)

                # Кликаем на кнопку отправить
                self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.CaptchaButton_view_action'))).click()

                # Возвращаемся к основному коду на странице
                self.browser.switch_to.default_content()

                if self.wait.until(EC.element_to_be_clickable
                                       ((By.CSS_SELECTOR, '#lyt_create #dtx_date > div > div.CPJFu7k2 > svg'))):
                    print('Капча пройдена')
                    break
                else:
                    # Переключаемся на новый iframe с картинкой
                    WebDriverWait(self.browser, 5).until(EC.frame_to_be_available_and_switch_to_it(
                        (By.CSS_SELECTOR, "iframe[title='SmartCaptcha advanced widget']")))
                    continue



            return self.browser

        except Exception as E:
            # Ошибка возникла, записываем сообщение в журнал
            print("Произошла ошибка в капче: %s", str(E))


    def simple_captcha(self):
        # Находим элемент, где располагается изображение капчи и делаем его скриншот,
        # screenshot('img.png') сохрнаняет скриншот в папке с проектом
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, 'captcha_image'))).screenshot('img.png')
            print('1) Скриншот области simple_captcha успешно сделан')
            # Находим текстовое поле и вставляем код который возвращает функция solver(),
            self.browser.find_element(By.ID, 'captcha_input').send_keys(self.sender_solve('img.png'))
            # Находим кнопку "Подтвердить" и кликаем по ней.
            self.browser.find_element(By.ID, 'submit_button').click()
        except Exception as E:
            # Ошибка возникла, записываем сообщение в журнал
            print("Произошла ошибка в капче: %s", str(E))
