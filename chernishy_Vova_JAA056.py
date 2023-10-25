from chernishy_base import Chernishy
from access_file import login_Vova, password_Vova

def new():
    chernishy = Chernishy(truck_num, pricep_num, day1, day2, login, password)
    chernishy.bot_send_message_start()
    chernishy.get_main_srv()
    chernishy.new_zayavka()
    chernishy.bot_send_message_stop()
    chernishy.browser.quit()


if __name__ == '__main__':

    # User var
    truck_num = 1
    pricep_num = 2
    day1 = 25
    day2 = 27
    login = login_Vova
    password = password_Vova


    # Набор фунций для запуска

    new()