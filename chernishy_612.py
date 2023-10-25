from access_file import login_SRV, password_SRV
from datetime import date
from chernishy_base import Chernishy

def new():
    chernishy = Chernishy(truck_num, pricep_num, start_date, end_date, login, password)
    chernishy.bot_send_message_start()
    chernishy.get_main_srv()
    chernishy.new_zayavka()
    chernishy.bot_send_message_stop()
    chernishy.browser.quit()

if __name__ == '__main__':

    # User var
    truck_num = 1 # Номер тягача по списку
    pricep_num = 1 # Номер прицепа по списку
    start_date = date(2023, 10, 29) # Диапозон дат в формате ГГГГ, ММ, ДД от -
    end_date = date(2023, 11, 2) # - до
    login = login_SRV # Логин
    password = password_SRV # Пароль

    # Набор фунций для запуска
    new()


