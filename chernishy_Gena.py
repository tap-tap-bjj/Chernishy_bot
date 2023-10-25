
from access_file import login_Gena, password_Gena, bot_token_SRV, chat_id_my, TWO_CAPCHA_TOKEN
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
import telebot
from twocaptcha import TwoCaptcha
from selenium.webdriver.chrome.options import Options
import requests
import logging

def sender_solve(path):
    solver = TwoCaptcha(TWO_CAPCHA_TOKEN)
    #bot.send_message(chat_id=chat_id_my, text='2) Изображение отправленно для разгадывания:')
    print('2) Изображение отправленно для разгадывания:')
    result = solver.normal(path, param='ru')
    #bot.send_message(chat_id=chat_id_my, text=f'3) От API пришёл ответ: {result}')
    print(f'3) От API пришёл ответ: {result}')
    #API вернёт словарь {'captchaId': '72447681441', 'code': 'gbkd'}
    #Обновляем словарь для дальнейшего извлечения ID капчи и отправки репорта
    dict_resut.update(result)
    return result['code']


def captcha(browser):
    try:
        #Переключаемся на новый iframe с картинкой
        WebDriverWait(browser, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe[title='SmartCaptcha advanced widget']")))

        #Хардкодим имя картинки
        img_names = 'img_yandex.png'
        with open(img_names, 'wb') as file:
            #Извлекаем атрибут src из тега в котором хранится ссылка на изображение
            img = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img[alt="Задание с картинкой"]'))).get_attribute('src')
            #Делаем простой requests запрос для скачивания картинки и её записи в файл
            file.write(requests.get(img).content)
            #bot.send_message(chat_id=chat_id_my, text=f'1) url image: {img}')
            print('Poluchena kartinka capcha')

        sender_solve(img_names)
        #bot.send_message(chat_id=chat_id_my, text=f'4) {dict_resut["code"]}')
        print(f'4) {dict_resut["code"]}')

        #Вставлям необходимую часть словаря dict_resut в котором лежит разгаданное слова с капчи
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input.Textinput-Control'))).send_keys(dict_resut['code'])
        time.sleep(1)

        #Кликаем на кнопку отправить
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.CaptchaButton_view_action'))).click()

        #Возвращаемся к основному коду на странице
        browser.switch_to.default_content()
    except Exception as E:
        # Ошибка возникла, записываем сообщение в журнал
        print("Произошла ошибка в капче: %s", str(E))

        # Отправляем сообщение в чат бота
        #bot.send_message(chat_id=chat_id_my, text=f"Ошибка в капче: {str(E)}")


def get_main_srv(browser, login, password): # Функция для записи куков и входа в систему
    try:
        browser.delete_all_cookies()
        url_main = "https://srv-go.ru/"
        browser.get(url_main)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#lyt_chk_clone_1'))).click()
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#txt_login input'))).send_keys(login)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#txt_password input'))).send_keys(password)
        wait.until(EC.element_to_be_clickable((By.ID, 'btn_login'))).click()
        time.sleep(3)
        return browser
    except Exception as e:
        print(f'Oshibka vhoda {str(e)}')


def new_zayavka(browser, truck_coord, pricep_coord):
    global flag
    while flag == True:
        try:
            #get_main_srv(browser)
            browser.refresh()
            time.sleep(3)
            btn_create_request = WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btn_create_request button')))
            btn_create_request.click()
            select_truck = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cmb_step_car use')))
            actions.move_to_element(select_truck).click(select_truck).move_by_offset(0, truck_coord).click().perform()
            truck = browser.find_element(By.CSS_SELECTOR, '#cmb_step_car > div > div > div').text # Выбор номера тягача
            select_pricep = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cmb_trailer_step_1 use')))
            actions.move_to_element(select_pricep).click(select_pricep).move_by_offset(0, pricep_coord).click().perform()
            pricep = browser.find_element(By.CSS_SELECTOR, '#cmb_trailer_step_1 > div > div > div').text # Выбор номера прицепа
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btn_step_next button'))).click()
            trans_type = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cmb_transportation_type use')))
            actions.move_to_element(trans_type).click(trans_type).move_by_offset(0, 45).click().perform()
            trans_kind = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#cmb_transportation_kind use')))
            actions.move_to_element(trans_kind).click(trans_kind).move_by_offset(0, 25).click().perform()
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#chk_copy ._7m08SzSw'))).click()
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btn_step_next button'))).click()

            #captcha(browser)

            input_day_new(browser, truck, pricep, day1, day2)

        except Exception as e:
            print(f'Ошибка в new_zayavka', str(e))


def input_day_new(browser, truck, pricep, day1, day2):
    global flag
    try:
        while flag == True:
            for j in range(day1, day2 + 1):
                    day = f'{j}.10.2023'
                    calen = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#lyt_create #dtx_date > div > div.CPJFu7k2 > svg')))
                    calen.click()
                    date = WebDriverWait(browser, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '[placeholder="Input date"]')))
                    date.send_keys(Keys.CONTROL + 'a')
                    #date.send_keys(Keys.DELETE)
                    date.send_keys(day)
                    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '._3J1cw2n9'))).click()

                    try:
                        slot = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div .slotInactive')))
                        slot.click()
                        button = WebDriverWait(browser, 3).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, '#btn_step_next button')))
                        button.click()

                        bot.send_message(chat_id=chat_id_my,
                                         text=f'Появилось место!!!!!! на {day}: \n{slot.text}')
                        print(f'Появилось место!!!!!! на {day}: \n{slot.text}')
                        print(f'Машина {truck} и прицеп {pricep} записан на {day}: \n{slot.text}')
                        bot.send_message(chat_id=chat_id_my,
                                         text=f'Машина {truck} и прицеп {pricep} записан на {day}: \n{slot.text}')
                        flag = False
                        break

                    except TimeoutException:
                        with open("log_chernishy.txt", 'a') as f:
                            print(f'Нет места для заявки для тягача {truck} на: {day} тек. время: {datetime.now()}')
                        continue
    except Exception as e:
                print(f'Ошибка в input_day_new {str(e)}')

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    # Standart var
    bot = telebot.TeleBot(token=bot_token_SRV)
    dict_resut = {}
    flag = True

    # User var
    truck_coord = 45
    pricep_coord = 25
    day1 = 22
    day2 = 23
    login = login_Gena
    password = password_Gena

    # Создание объекта опций
    options = Options()
    options.add_argument("--headless")  # Запуск Chrome в режиме без графического интерфейса
    options.add_argument("--no-sandbox")
    #options.add_extension('coordinates.crx')
    options.add_argument("--window-size=1920,1080")

    # Браузер и функции
    browser = webdriver.Chrome(options=options)
    actions = ActionChains(browser)
    wait = WebDriverWait(browser, 5)
    #browser.implicitly_wait(5)

    # Набор фунций для запуска
    bot.send_message(chat_id=chat_id_my, text=f'Запуск бота для {login}')
    get_main_srv(browser, login, password)
    #change_time(browser)
    new_zayavka(browser, truck_coord, pricep_coord)
    browser.quit()
    bot.send_message(chat_id=chat_id_my, text=f'Остановка бота для {login}')

