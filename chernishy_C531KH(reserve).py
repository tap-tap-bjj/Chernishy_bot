from access_file import login_SRV, password_SRV
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
    truck_num = 1 # Номер тягача по списку
    pricep_num = 1 # Номер прицепа по списку
    start_date = date(2024, 0o3, 0o1) # Диапозон дат в формате ГГГГ, ММ, ДД от -
    end_date = date(2024, 0o3, 0o1) # - до
    login = login_SRV # Логин
    password = password_SRV # Пароль

    # Набор фунций для запуска
    new()


