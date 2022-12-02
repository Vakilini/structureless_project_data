import PySimpleGUI as sg

def popup(key):
    sg.theme('DarkGreen3')
    layout = [
        [sg.Listbox(food[key], size=(30, 3), enable_events=True, key='-GOODS-')],
        [sg.Button("Cancel")],
    ]
    window = sg.Window(key, layout, modal=True)
    while True:

        event, values = window.read()

        if event in (sg.WINDOW_CLOSED, 'Cancel'):
            result = None
            break
        elif event == '-GOODS-':
            result = values[event][0]
            print(result)
            break

    window.close()
    return result

food = {
    'Fruit'     : ['Apple','Bananas','Oranges','Mangoes'],
    'Vegetable' : ['Kale', 'Cabbage', 'Celery', 'Asparagus', 'Lettuce'],
    'Meat'      : ['Pork', 'Beef', 'Mutton', 'Veal', 'Vension'],
}

font = ("Courier New", 11)
sg.theme('DarkBlue3')
sg.set_options(font=font)

layout = [
    [sg.Listbox(list(food.keys()), size=(30, 3), enable_events=True, key='-CATEGORY-')],
    [sg.VPush()],
    [sg.StatusBar('', size=(0, 1), key='-STATUS-')],
]

window = sg.Window('Food', layout, size=(640, 480))

while True:

    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == '-CATEGORY-':
        key = values[event][0]
        print(values)
        goods = popup(key)
        if goods:
            window['-STATUS-'].update(f'{key} - {goods}')
        else:
            window['-STATUS-'].update('')

window.close()