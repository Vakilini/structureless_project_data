import PySimpleGUI as sg
# import socket
# import random
# from threading import Thread
# from datetime import datetime
# from colorama import Fore, init, Back
import re
import socket
import json
import time
from PIL import Image
from io import BytesIO
def popup(key,food):
    print(food[key])
    layout = [
        [sg.Output(size=(100, 15), font=('Helvetica 10'))],
       # [sg.Multiline(size=(55, 5), enter_submits=False, key='-QUERY-', do_not_clear=False), sg.Button("Отправить", key="_send_", write_only=True)],
        [sg.Button("Закрыть")],
    ]
    window = sg.Window(key, layout, modal=True, size=(640, 480))
    while True:

        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Закрыть'):
            result = None
            break
        elif event == 'SEND':
            query = values['-QUERY-'].rstrip()
            # EXECUTE YOUR COMMAND HERE
            print('The command you entered was {}'.format(query), flush=True)


    window.close()
    #return result
def l(food):

    font = ("Courier New", 11)
    sg.theme('DarkBlue3')
    sg.set_options(font=font)
    layout = [[sg.Text("Чат", font=('Helvitica bold', 14), justification='center', size=(100, 1))],
        [sg.Button("Профиль", size=(12, 3), key='_Profile_'),
        [sg.Text('                                                              Your output will go here',size=(60, 1))]],
        [sg.Listbox(list(food.keys()), size=(15, 15), enable_events=True, key='-CATEGORY-')],


    ]

    window = sg.Window('Food', layout, size=(640, 480))

    while True:

        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == '-CATEGORY-':
            key = values[event][0]
            print(values)
            popup(key,food)


    window.close()



def SinIn(values):
    #print(values)
    HOST = '127.0.0.1'
    PORT = 8088

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        data = json.dumps({'a': '<-Запрос на вход->', 'b': values['_login_'], 'c': values['_passin_']})
        #print(data)
        s.sendall(data.encode())
        answer = s.recv(1024)
        print(answer)
        answer = json.loads(answer.decode())
        print(answer)
        if answer.get('b') == 'В базе нет такого пользователя':
            return None
        else:
            print(answer.get('e'))
            return answer.get('c'), answer.get('d'),answer.get('e')

def RegOnSerwer(FormReg):
    del FormReg['_passin2_']
    HOST = '127.0.0.1'
    PORT = 8088

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        data = json.dumps({'a': '<-Запрос на регистрацию->', 'b':FormReg['_namein_'],'c':FormReg['_fnamein_'],'d':FormReg['_login_'],'e':FormReg['_passin1_']})
        print(data)
        s.sendall(data.encode())
        answer = s.recv(1024)
        answer = json.loads(answer.decode())
        #print(answer)
        return answer.get('b')



def Registration(visibleerr = False, ErrType = 'Ошибка ввода!', RegIn = False):

    RegLayout = [[sg.Text("Вас приветствует наш корпоративный чат!", font=('Helvitica bold', 20), justification='center', size=(100, 1))],
                 [sg.Text("Регистрация", font=('Helvitica bold', 15), justification='center', size=(100, 1))],

                 [sg.Text("Ваше имя", font=('Helvitica bold', 12), justification='center', size=(15, 1)),
                  sg.InputText(key='_namein_', default_text='Иван')],

                 [sg.Text("Ваша фамилия", font=('Helvitica bold', 12), justification='center', size=(15, 1)),
                  sg.InputText(key='_fnamein_',default_text = "Иван")],

                 [sg.Text("Логин", font=('Helvitica bold', 12), justification='center', size=(15, 1)),
                  sg.InputText(key='_login_', default_text = "name.fname@ya.ru")],

                 [sg.Text("Придумайте пароль", font=('Helvitica bold', 12), justification='center', size=(15, 1)),
                  sg.InputText(key='_passin1_', password_char='*', default_text = 'DDf_123')],

                 [sg.Text("Повторите пароль", font=('Helvitica bold', 12), justification='center', size=(15, 1)),
                  sg.InputText(key='_passin2_', password_char='*', default_text = 'DDf_123')],

                 [sg.Button("Зарегестрироваться", size=(15, 1), font=("Times New Roman", 12), key='_but1_')],
                 [sg.Text(ErrType, font=('Helvitica bold', 12), justification='center', size=(100, 1), text_color='red', visible=visibleerr)]
                 ]

    window = sg.Window('Window Reg', RegLayout, size=(640, 480))
    if  RegIn:
        time.sleep(300)
        window.close()
        return ''
    else:
        event, values = window.read()
        window.close()
    return values
#Registration()



def Error(values):
    InName = "^([а-яА-ЯёЁ]+(\-[а-яА-ЯёЁ]+)*)$"
    InPassw = "^(?=\S{6,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])"
    InLog = "([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
    errorList = ""

    if re.compile(InName).search(values['_namein_']) is None:
        errorList += "\nНеправильно введено имя."
    if re.compile(InName).search(values['_fnamein_']) is None:
        errorList += "\nНеправильно введена фамилия."
    if re.compile(InLog).search(values['_login_']) is None:
        errorList += "\nНеправильный логин."
    if re.compile(InPassw).search(values['_passin1_']) is None:
        errorList += "\nНеправильный пароль."
    if values['_passin1_'] != values['_passin2_']:
        errorList += "\nПароли не совпадают."
    print(errorList)
    if errorList:
        Error(Registration(True, errorList))
    else:
        #Приколы с записью в пользователя в бд)))
        answer = RegOnSerwer(values)
        if answer == 'Пользователь с таким логином уже зарегестрирован':
            Error(Registration(True, answer))
        else:
            Login()



def UserList():
    HOST = '127.0.0.1'
    PORT = 8088

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        data = json.dumps({'a': '<-Запрос на список пользователей->'})
        print(data)
        s.sendall(data.encode())
        answer = s.recv(1024)
        answer = json.loads(answer.decode())


def IM(name, fname):
    path = r"C:\Users\vaniv\Downloads\Telegram Desktop\Дизайн без названия.png"
    layout = [[sg.Text('Browse to a png or gif file')],
              [sg.Input(key='-FILE-', enable_events=True, default_text=path), sg.FileBrowse()],
              [sg.Button('Show')],
              [sg.Image(filename=None, key='Image')]]

    window = sg.Window('File Compare', layout)

    while True:
        event, values = window.read()

        if event in (None,):
            break
        if event in ('Show'):

            if values['-FILE-'] and values['-FILE-'][-3:] in ['png', 'gif']:
                # изменение размеров картинки
                image = Image.open(values['-FILE-'])
                # максимальный размер
                size = (500, 500)
                image.thumbnail(size, Image.ANTIALIAS)
                # запись в память в виде байтов
                buffered = BytesIO()
                image.save(buffered, format=values['-FILE-'][-3:])
                # присвоение виджету измененой картинки
                window.FindElement('Image').Update(data=buffered.getvalue())


    window.close()
#IM()





def Profile(name, fname):
    User = name+' '+ fname
    # path = r"C:\Users\vaniv\Downloads\Telegram Desktop\Дизайн без названия.png"
    # image = Image.open(path)
    # # максимальный размер
    # size = (100, 100)
    # image.thumbnail(size, Image.ANTIALIAS)
    # # запись в память в виде байтов
    # buffered = BytesIO()
    # image.save(buffered, format=path)

    layout = [[sg.Text(User, font=('Helvitica bold', 14), justification='center', size=(100, 1))],
             #  [sg.Image(data=buffered.getvalue(),filename=None, key='Image')],
             # [sg.Button('Изменить фото',key='ImageN')]
              [sg.Button('Чат',key='_Action_')]
              ]
    window = sg.Window('File Compare', layout, size=(640, 480))





    event, values = window.read()
    if event == "_Action_":
        window.close()
        action(name, fname)


def Recipient(recipient):
    Loyout2 = [
        [sg.Output(size=(100, 15), font=('Helvetica 10'),default_text=recipient)],
        [sg.Multiline(size=(20, 5), enter_submits=False, key='-QUERY-', do_not_clear=False)]]
    window = sg.Window('Window Log', Loyout2, size=(640, 480), modal=True)

    event, values = window.read()

def action(name, fname, UserLog):
    Loyout1 = [[sg.Text("Чат", font=('Helvitica bold', 14), justification='center', size=(100, 1))],
                  [sg.Button("Профиль", size=(12,3),key='_Profile_'),
                  [sg.Text('                                                              Your output will go here', size=(60, 1))]],
                  [sg.Listbox(values= UserLog, size=(15, 15),key='_CorrespondenceList_')],
               [sg.Button("Написать", size=(12, 3), key='_CorrespondenceEnter_')]
    ]

    Loyout2 = [
               [sg.Output(size=(100, 15), font=('Helvetica 10'))],
               [sg.Multiline(size=(20, 5), enter_submits=False, key='-QUERY-', do_not_clear=False)]]


    window = sg.Window('Window Log', Loyout1, size=(640, 480), modal=True)
    while True:
        event, values = window.read()
        if event == '_Profile_':
            window.close()
            #Profile(name, fname)
            Profile(name, fname)
        elif event == "_CorrespondenceEnter_":
            recipient = values[event]
            print(values)
            Recipient(recipient)


#action()
def Login(visibleerr = False):
    LogLayout = [[sg.Text("Вас приветствует наш корпоративный чат!", font=('Helvitica bold', 20), justification='center', size=(100, 1))],
               [sg.Text("Вход в систему", font=('Helvitica bold', 15), justification='center', size=(100, 1))],
               [sg.Text("Логин", font=('Helvitica bold', 12), justification='center', size=(15, 1)), sg.InputText(key='_login_', default_text = "name.fname@ya.ru")],
               [sg.Text("Пароль", font=('Helvitica bold', 12), justification='center', size=(15, 1)), sg.InputText(key='_passin_', password_char='*',default_text = 'DDf_123')],
                 [sg.Button("Войти", size=(20, 1), font=("Times New Roman", 12), key='_SinIn_')],
                [sg.Button("Создать новый аккаунт", size=(20, 1), font=("Times New Roman", 12), key='_cre-new-akk_')],
               [sg.Text("В базе нет такого пользователя", font=('Helvitica bold', 12), justification='center', size=(100, 1), text_color='red', visible=visibleerr)]
                ]

    window = sg.Window('Window Log', LogLayout, size=(640, 480))

    event, values = window.read()
    if event == "_cre-new-akk_":
        window.close()
        Error(Registration())
    elif event == '_SinIn_':
        name, fname, UserLog = SinIn(values)
        if name:
            print(name,fname)
            window.close()
            UserLog_ok = {}
            for i in UserLog.keys():
                UserLog_ok.update({(i+UserLog[i][0]+ ' ' +UserLog[i][0]):i}) #(UserLog[i][0]+ ' ' +UserLog[i][0]) = i
            print(UserLog_ok)
            l(UserLog_ok)
            #action(name, fname,UserLog)
        else:
            window.close()
            Login(True)



Login()






