import StatHandler
import PySimpleGUI as sg

sg.theme('DarkAmber') 

body = []
window = sg.Window('Window Title', [])

def add_character(name:int):
    window.extend_layout([[sg.Text(name),sg.Input(size=(3,1), pad=(0,0))]])


add_character("epic")
add_character("steve")

layout = [  [sg.Text('Initiative')],
            [body],
            [sg.Button('Add'), sg.Button('Cancel')] ]

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
        break
    add_character("test")

window.close()