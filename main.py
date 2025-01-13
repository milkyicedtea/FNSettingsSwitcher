from pathlib import Path
from typing import Any

import PySimpleGUI as sg
import sys

from Utils.buttonHandlers import ButtonHandlers
from Utils.jsonhandler import JsonHandler

sg.theme('DarkAmber')

def get_resource_path(relative_path: str) -> Path:
    if hasattr(sys, '_MEIPASS'):
        return Path(sys._MEIPASS) / relative_path
    return Path(relative_path)

license_file_path = get_resource_path('LICENSE.md')
try:
    license_text = license_file_path.read_text(encoding="utf-8")
except FileNotFoundError:
    license_text = "License file not found. Please contact support."

menu_def = [
    ['About', ['License']]
]
layout = [
    [sg.Menu(menu_def)],
    [sg.Text('FNSS', font = "_ 15", justification = 'c', expand_x = True)],
    [
        sg.Push(),
        sg.Text(f"Click on the settings you want to apply.\n"
             f"You'll be able to adjust them in-game if needed.",
             expand_x = True,
             pad = ((35, 0), (4, 10))
        ),
        sg.Push()
    ],

    [
        sg.Push(),
        sg.Button(
            'Save settings',
            size = (15, 1),
            key = "Save"
        ),
        sg.Button(
            'Load settings',
            size = (15, 1),
            key = "Load"
        ),
        sg.Push()
    ],
    [sg.Push()],
    [sg.Text('Or try one of the included settings!', font = '_ 12', pad = ((75, 0), (4, 4))), sg.Push()],

    [
        sg.Push(),
        sg.Combo(['', 'Performance', 'Dx 12 Epic/High', 'Dx 11 Epic/High'], readonly = True),
        sg.Button('Apply', size = (15, 1), key = "Apply_Included"),
        sg.Push()
    ],

    [sg.Button('Exit', size = (7, 1), key = 'Exit_Program', pad = ((0, 0), (10, 0)))],
]

if Path.home().joinpath('fnss_latest.json').exists():
    layout.insert(3,[
        sg.Text(
            f"You last set your settings to: {JsonHandler.readjson()}",
            key = "ModeTxt",
            expand_x = True,
            pad = ((75, 0), (0, 4)),
            visible = JsonHandler.readjson() != "None"
        ),
        sg.Push()
    ],)
else:
    layout.insert(3, [
        sg.Text(
            key = "ModeTxt",
            expand_x = True,
            pad = ((75, 0), (0, 4)),
            visible = False
        )
    ])

sg.set_global_icon(str(get_resource_path('icons/fnss_white.ico')))

# initialize winodw
window = sg.Window(
    'FN Settings Switcher',
    layout = layout,
    resizable = False,
    finalize = True,
    element_justification = 'c',
    size = (450, 270)
)


def main_app():
    while True:
        pass

        event: str
        value: dict[str, Any]

        event, value = window.read()

        with ButtonHandlers(window) as button:
            if event in [sg.WIN_CLOSED, 'Exit_Program']:
                break

            elif event == 'License':
                sg.popup_scrolled("License", license_text, size = (60, 20))

            elif event == 'Save':
                button.save_settings()

            elif event == 'Load':
                button.load_settings()

            elif event == 'Apply_Included':
                selected_mode = list(value.values())[0]
                button.apply_included(selected_mode)
                window['ModeTxt'].update(f"You last set your settings to: {JsonHandler.readjson()}", visible = True)


if __name__ == "__main__":
    main_app()
