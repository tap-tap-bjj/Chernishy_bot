import subprocess
import time
import os
import psutil


script_name = 'chernishy_delta_14days_random_time.py'
processes = []
lunches = 1

# Проверка наличия скрипта
if not os.path.isfile(script_name):
    print(f"Script {script_name} not found.")
else:
    # Запуск процессов
    for i in range(1, lunches+1):
        try:
            # Используем shell=True для Windows, иначе убираем его
            process = subprocess.Popen(args=["start", "python", script_name, str(i)], shell=True, stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
            processes.append(process)
            print(f'Starting process #{i}')
        except Exception as e:
            print(f'Error starting process #{i}: {e}')
        time.sleep(20)

    # Ожидание 50 минут
    time.sleep(50*60)

    # Завершение процессов
    for i in range(lunches):
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                # Проверяем имя и аргументы командной строки процесса
                if proc.name() == 'python.exe' and script_name in proc.cmdline():
                    proc.terminate()
                    try:
                        proc.wait(timeout=10)  # Ждем, пока процесс завершится
                    except psutil.TimeoutExpired:
                        proc.kill()  # Принудительно завершаем процесс
                    print(f'Process {proc.pid} terminated.')
        except Exception as e:
            print(f'Error terminating process: {e}')

# Завершение окон терминала
subprocess.run(["taskkill", "/f", "/im", "cmd.exe"], shell=True)
print('All terminal windows closed.')
