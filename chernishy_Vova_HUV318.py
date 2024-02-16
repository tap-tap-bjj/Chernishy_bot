from access_file import login_Vova, password_Vova
from datetime import date
from chernishy_base import Chernishy

def new():
    chernishy = Chernishy(truck_num, pricep_num, start_date, end_date, login, password)
    chernishy.bot_send_message_start()
    chernishy.get_main_srv()
    chernishy.new_zayavka()
    #chernishy.change_time(truck_number)
    chernishy.bot_send_message_stop()
    chernishy.browser.quit()

if __name__ == '__main__':

    # User var
    truck_number = 'C531KH39'
    truck_num = 2 # Номер тягача по списку
    pricep_num = 1 # Номер прицепа по списку
    start_date = date(2023, 12, 18) # Диапозон дат в формате ГГГГ, ММ, ДД от -
    end_date = date(2023, 12, 19) # - до
    login = login_Vova # Логин
    password = password_Vova # Пароль

    # Набор фунций для запуска
    new()


