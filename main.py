import snake
import PySimpleGUI as sg

layout = [  [sg.Text("Start Snake game?")],
            [sg.Button('Ok')] ]

window = sg.Window('Snake', layout)
                                          
event, values = window.read()


window.close()

while True:
    snake.main()
