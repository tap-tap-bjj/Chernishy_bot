from access_file import login_Gena, password_Gena
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
    truck_number = 'Y677BX60' # nomer 2 po spisku # 'T997BH39' nomer 1
    truck_num = 1 # Номер тягача по списку
    pricep_num = 1 # Номер прицепа по списку
    start_date = date(2024, 0o2, 16) # Диапозон дат в формате ГГГГ, ММ, ДД от -
    end_date = date(2024, 0o2, 16) # - до
    login = login_Gena # Логин
    password = password_Gena # Пароль

    # Набор фунций для запуска
    new()


