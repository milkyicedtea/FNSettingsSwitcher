import PySimpleGUI as sg

from Utils.buttonHandlers import ButtonHandlers
from Utils.jsonhandler import readjson

exit_button = [sg.Button('Exit', size = (15, 1), key = 'Exit_Program')]

sg.theme('DarkAmber')
# print(sg.theme_button_color())
# print(sg.theme_global())
exit_column = []

layout = [
    [sg.Text('FNSS', font = "_ 15", justification = 'c', expand_x = True)],
    [sg.Text(f"Click on the settings you want to apply.\nYou'll be able to adjust them in-game if needed.", justification = 'c', expand_x = True, pad = ((0, 0), (0, 0)))],
    [sg.Text(f"You last set your settings to: {readjson()}", key = "ModeTxt", justification = 'c', expand_x = True, pad = ((0, 0), (0, 5)))],
    [sg.Button('Performance', size = (15, 1), key = "Performance", pad = ((30, 0), (4, 4))), sg.Text('Competitive settings', expand_x = True)],
    [sg.Button('Dx 12 Epic/High', size = (15, 1), key = "Dx12", pad = ((30, 0), (4, 4))), sg.Text("Epic/High \"optimized\" settings")],
    [sg.Button('Exit', size = (7, 1), key = 'Exit_Program', pad = ((0, 0), (10, 0)))],
]

# initialize winodw
window = sg.Window('FN Settings Switcher', layout, size = (375, 215), resizable = False, finalize = True, element_justification = 'c')


def main_app():
    while True:
        pass

        event, value = window.read()

        if event in [sg.WIN_CLOSED, 'Exit_Program']:
            break

        elif event in ['Performance']:
            ButtonHandlers().setPerformance(window)

        elif event in ['Dx12']:
            ButtonHandlers().setDx12(window)


if __name__ == "__main__":
    main_app()
