import ctypes, sys
import time
from datetime import datetime
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
if is_admin():
    start_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day,int(input("С какого часа закрыть доступ: \n")))
    finish_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day,int(input("С какого часа открыть доступ: \n")))

    print(start_time,'\n',finish_time)

    try:
        hosts = r'C:\Windows\System32\drivers\etc\hosts'
    except FileNotFoundError:
        hosts = r'/etc/hosts'

    redirect_url = '127.0.0.1'
    blocked_sites = ['www.vk.com','vk.com','rt.pornhub.com','pornhub.com']
    while True:
        if start_time < datetime.now() < finish_time:
            print("Доступ ограничен!")

            with open(hosts, 'r+') as file:
                src = file.read()

                for site in blocked_sites:
                    if site in src:
                        pass
                    else:
                        file.write(f'{redirect_url} {site}\n')
        else:
        

            with open(hosts,'r+') as file:
                src = file.readlines()
                file.seek(0)
                for line in src:
                    if not any(site in line for site in blocked_sites):
                        file.write(line)
                file.truncate()
            print('Доступ открыт!')
        time.sleep(5)
else:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    print("Права нет!")