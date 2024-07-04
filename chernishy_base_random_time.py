from access_file import bot_token_SRV, chat_id_my, TWO_CAPCHA_TOKEN

import chromedriver_autoinstaller_fix
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime, timedelta
import telebot
from twocaptcha import TwoCaptcha
from selenium.webdriver.chrome.options import Options
import requests


class Chernishy:
    def __init__(self, truck_num, pricep_num, start_date, end_date, time_set, login, password):
        # Словарь для капчи
        self.dict_resut = {}
        # Создание объекта опций
        options = Options()
        #options.add_argument("--headless")  # Запуск Chrome в режиме без графического интерфейса
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        # Браузер и функции
        chromedriver_autoinstaller_fix.install()
        self.browser = webdriver.Chrome(options=options)
        self.actions = ActionChains(self.browser)
        self.wait = WebDriverWait(self.browser, 5)
        # Флаг для окончания программы
        self.flag = True
        self.bot = telebot.TeleBot(token=bot_token_SRV)
        # Переменные пользователя
        self.truck_coord = truck_num * 22
        self.pricep_coord = pricep_num * 22
        self.start_date = start_date
        self.end_date = end_date
        self.day_count = (end_date - start_date).days + 1
        self.time_set = time_set
        self.login = login
        self.password = password
        self.screenshot_fail = f'screenshot_fail{self.login}_{time_set}.png'
        self.screenshot_sucsses = f'screenshot_sucsses_{self.login}_{time_set}.png'

    def is_element_present(self, how, what):
        try:
            self.browser.find_element(how, what)
        except (NoSuchElementException, TimeoutException):
            return False
        return True


    def bot_send_message_start(self):
        self.bot.send_message(chat_id=chat_id_my, text=f'Запуск бота для {self.login}')

    def bot_send_message_stop(self):
        self.bot.send_message(chat_id=chat_id_my, text=f'Остановка бота для {self.login}')

    def sender_solve(self, path):
        solver = TwoCaptcha(TWO_CAPCHA_TOKEN)
        # bot.send_message(chat_id=chat_id_my, text='2) Изображение отправленно для разгадывания:')
        print('2) Изображение отправленно для разгадывания:')
        result = solver.normal(path, param='ru')
        # bot.send_message(chat_id=chat_id_my, text=f'3) От API пришёл ответ: {result}')
        print(f'3) От API пришёл ответ: {result}')
        # API вернёт словарь {'captchaId': '72447681441', 'code': 'gbkd'}
        # Обновляем словарь для дальнейшего извлечения ID капчи и отправки репорта
        self.dict_resut.update(result)
        return result['code']

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
            self.img_names = 'img_yandex.png'
            with open(self.img_names, 'wb') as file:
                # Извлекаем атрибут src из тега в котором хранится ссылка на изображение
                img = self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'img[alt="Задание с картинкой"]'))).get_attribute(
                    'src')
                # Делаем простой requests запрос для скачивания картинки и её записи в файл
                file.write(requests.get(img).content)
                # bot.send_message(chat_id=chat_id_my, text=f'1) url image: {img}')
                print('Poluchena kartinka capcha')

            Chernishy.sender_solve(self, path=self.img_names)
            # bot.send_message(chat_id=chat_id_my, text=f'4) {dict_resut["code"]}')
            print(f'4) {self.dict_resut["code"]}')

            # Вставлям необходимую часть словаря dict_resut в котором лежит разгаданное слова с капчи
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.Textinput-Control'))).send_keys(
                self.dict_resut['code'])
            time.sleep(1)

            # Кликаем на кнопку отправить
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.CaptchaButton_view_action'))).click()

            # Возвращаемся к основному коду на странице
            self.browser.switch_to.default_content()
        except Exception as E:
            # Ошибка возникла, записываем сообщение в журнал
            print("Произошла ошибка в капче: %s", str(E))
            # self.browser.py.save_screenshot(self.screenshot_fail)
            # Отправляем сообщение в чат бота
            # bot.send_message(chat_id=chat_id_my, text=f"Ошибка в капче: {str(E)}")

    def get_main_srv(self):  # Функция для записи куков и входа в систему
        try:
            self.browser.delete_all_cookies()
            url_main = "https://srv-go.ru/"
            self.browser.get(url_main)
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#lyt_chk_clone_1'))).click()
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#txt_login input'))).send_keys(self.login)
            self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#txt_password input'))).send_keys(self.password)
            self.wait.until(EC.element_to_be_clickable((By.ID, 'btn_login'))).click()
            time.sleep(3)
            return self.browser
        except Exception as e:
            print(f'Oshibka vhoda {str(e)}')
            #self.browser.py.save_screenshot(self.screenshot_fail)

    def new_zayavka(self):
        while self.flag == True:
            try:
                if Chernishy.is_element_present(self, how=By.CSS_SELECTOR, what='#lyt_chk_clone_1'): # Если выскочило на страницу ввода пароля,
                    # вводим пароль
                    Chernishy.get_main_srv(self)
                self.browser.refresh()
                time.sleep(3)
                btn_create_request = WebDriverWait(self.browser, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#btn_create_request button')))
                btn_create_request.click()
                select_truck = WebDriverWait(self.browser, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, '#cmb_step_car use')))
                self.actions.move_to_element(select_truck).click(select_truck).move_by_offset(0,
                                                                                         self.truck_coord).click().perform()
                self.truck = self.browser.find_element(By.CSS_SELECTOR,
                                             '#cmb_step_car > div > div > div').text  # Выбор номера тягача
                select_pricep = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cmb_trailer_step_1 use')))
                self.actions.move_to_element(select_pricep).click(select_pricep).move_by_offset(0,
                                                                                           self.pricep_coord).click().perform()
                self.pricep = self.browser.find_element(By.CSS_SELECTOR,
                                              '#cmb_trailer_step_1 > div > div > div').text  # Выбор номера прицепа
                self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btn_step_next button'))).click()
                trans_type = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cmb_transportation_type use')))
                self.actions.move_to_element(trans_type).click(trans_type).move_by_offset(0, 45).click().perform()
                trans_kind = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cmb_transportation_kind use')))
                self.actions.move_to_element(trans_kind).click(trans_kind).move_by_offset(0, 25).click().perform()
                self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#chk_copy ._7m08SzSw'))).click()
                self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btn_step_next button'))).click()

                Chernishy.captcha(self)

                Chernishy.input_day_new(self)

            except Exception as e:
                print(f'Ошибка в new_zayavka', str(e))
                #self.browser.py.save_screenshot(self.screenshot_fail)

    def input_day_new(self):
        try:
            while self.flag == True:
                for single_date in [d for d in (self.start_date + timedelta(n) for n in range(self.day_count))]:
                    day = single_date.strftime("%d.%m.%Y")
                    calen = self.wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, '#lyt_create #dtx_date > div > div.CPJFu7k2 > svg')))
                    calen.click()
                    date = WebDriverWait(self.browser, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '[placeholder="Input date"]')))
                    date.send_keys(Keys.CONTROL + 'a')
                    # date.send_keys(Keys.DELETE)
                    date.send_keys(day)
                    self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '._3J1cw2n9'))).click()

                    try:
                        slot = WebDriverWait(self.browser, 1).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, f'#lyt_slot_clone_{self.time_set}.slotInactive')))
                        # выбор времени брони по цифре слота (By.CSS_SELECTOR, '#lyt_slot_clone_11.slotInactive')
                        slot.click()
                        self.browser.find_element(By.CSS_SELECTOR, '#btn_step_next button').click()

                        slotText = slot.text
                        self.bot.send_message(chat_id=chat_id_my,
                                              text=f'Появилось место!!!!!! на {day}: \n{slotText} тек. время: {datetime.now()}')
                        print(f'Появилось место!!!!!! на {day}: \n{slotText} тек. время: {datetime.now()}')
                        print(f'Машина {self.truck} и прицеп {self.pricep} записан на {day}: \n{slotText}')
                        self.bot.send_message(chat_id=chat_id_my,
                                              text=f'Машина {self.truck} и прицеп {self.pricep} записан на {day}: \n{slotText}')
                        # self.flag = False
                        #self.browser.py.save_screenshot(self.screenshot_sucsses)
                        # self.browser.py.quit()
                        continue

                    except TimeoutException:
                        print(f'Нет места для заявки для тягача {self.truck} на: {day} тек. время: {datetime.now()}')
                        continue
        except Exception as e:
            print(f'Ошибка в input_day_new {str(e)}')
            #self.browser.py.save_screenshot(self.screenshot_fail)

    def change_time(self, truck_number):
        while self.flag == True:
            try:
                if Chernishy.is_element_present(self, how=By.CSS_SELECTOR, what='#lyt_chk_clone_1'):
                    Chernishy.get_main_srv(self)
                self.browser.refresh()
                time.sleep(3)
                car_row = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{truck_number}')]")))
                car_row.click()
                #time.sleep(1)
                button_edit = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#lyt_btn_edit')))
                button_edit.click()
                #time.sleep(1)
                button_reschedule = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btn_request_reschedule')))
                button_reschedule.click()

                #Chernishy.captcha(self)

                Chernishy.input_day_reschedule(self, truck_number)

            except Exception as e:
                print(f'Ошибка в change_time', str(e))
                #self.browser.py.save_screenshot(self.screenshot_fail)

    def input_day_reschedule(self, truck_number):
        try:
            while self.flag == True:
                for single_date in [d for d in (self.start_date + timedelta(n) for n in range(self.day_count))]:
                    day = single_date.strftime("%d.%m.%Y")
                    calen = self.wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, '#lyt_reschedule #dtx_date > div > div.CPJFu7k2 > svg')))
                    calen.click()
                    date = WebDriverWait(self.browser, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '[placeholder="Input date"]')))
                    date.send_keys(Keys.CONTROL + 'a')
                    # date.send_keys(Keys.DELETE)
                    date.send_keys(day)
                    self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '._3J1cw2n9'))).click()

                    try:
                        slot = WebDriverWait(self.browser, 1).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div .slotInactive')))
                        slot.click()
                        self.browser.find_element(By.CSS_SELECTOR, '#btn_step_next button').click()

                        self.bot.send_message(chat_id=chat_id_my,
                                         text=f'Появилось место!!!!!! на {day}: \n{slot.text}')
                        print(f'Появилось место!!!!!! на {day}: \n{slot.text}')
                        print(f'Машина {truck_number} перенсена на дату {day}: \n{slot.text}')
                        self.bot.send_message(chat_id=chat_id_my,
                                         text=f'Машина {truck_number} перенсена на дату {day}: \n{slot.text}')
                        self.flag = False
                        #self.browser.py.save_screenshot(self.screenshot_sucsses)
                        self.browser.quit()
                        break

                    except TimeoutException:
                        with open("log_chernishy.txt", 'a') as f:
                            print(f'Нет места для переноса заявки тягача {truck_number} на: {day} тек. время: {datetime.now()}')
                        continue
        except Exception as e:
            print(f'Ошибка в input_day_reschedule {str(e)}')
            #self.browser.py.save_screenshot(self.screenshot_fail)