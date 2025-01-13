import configparser
import os
import re
from pathlib import Path

import FreeSimpleGUI as sg
from FreeSimpleGUI import Window
from Utils.jsonhandler import JsonHandler
import Utils.modes as modes


class ButtonHandlers:
    def __init__(self, window: Window):
        self.config_folder = Path(f"{os.getenv('LOCALAPPDATA')}/FortniteGame/Saved/Config/WindowsClient")
        self.__window = window

    def save_settings(self):
        save_path = Path(sg.popup_get_file(
            "Select a location to save your .fnss file",
            save_as=True,
            file_types=(('fnss Files', '*.fnss'),)
        ))

        if save_path:
            if not save_path.suffix == '.fnss':
                save_path.rename(save_path.name+'.fnss')
            for file in self.config_folder.iterdir():
                settings_content = None
                if file.name == 'GameUserSettings.ini':
                    settings_content = file.read_text()
                if settings_content:
                    save_path.write_text(settings_content)
                    sg.popup_ok(f"Settings successfully saved to {save_path}!")
                    break

    def load_settings(self):
        load_path = Path(sg.popup_get_file(
            "Select a .fnss file to load",
            file_types=(('fnss Files', '*.fnss'),)
        ))
        if load_path:
            if not load_path.suffix == '.fnss':
                sg.popup("No .fnss file was selected!\nYour settings haven't been edited.")
            settings_file = self.config_folder.joinpath('GameUserSettings.ini')

            if not settings_file.exists():
                settings_file.touch()
            settings_content = load_path.read_text()
            settings_file.write_text(settings_content)

            sg.popup_ok("Settings successfully loaded!")

    def apply_settings(self, ini_strings):
        settings_file = self.config_folder.joinpath('GameUserSettings.ini')
        if not settings_file.exists():
            settings_file.touch()  # Create the file if it doesn't exist

        choice = sg.popup_yes_no('Would you like to have stretched resolution?')
        if not choice:
            sg.popup("Don't just close the popup please!!")
            return
        if choice == "Yes":
            stretched_res = sg.popup_get_text(
                'Enter your preferred stretched resolution. Ex: 1650x1080',
            )
            if not stretched_res:
                sg.popup("Your settings haven't been edited because exited the menu "
                         "without providing a stretched resolution"
                         )
                return
            match = re.match(r'^(\d+)x(\d+)$', stretched_res)
            if not match:
                sg.popup("The stretched resulution you provided is invalid ")
                return

            width = int(match.group(1))
            height = int(match.group(2))

            config = configparser.ConfigParser(allow_no_value = True, strict = False)
            config.optionxform('str')
            config.read_string(ini_strings)

            section = '/Script/FortniteGame.FortGameUserSettings'
            if section not in config.sections():
                config.add_section(section)

            resolution_keys = [
                'ResolutionSizeX',
                'ResolutionSizeY',
                'LastUserConfirmedResolutionSizeX',
                'LastUserConfirmedResolutionSizeY',
                'DesiredScreenWidth',
                'DesiredScreenHeight',
                'LastUserConfirmedDesiredScreenWidth',
                'LastUserConfirmedDesiredScreenHeight',
            ]

            for key in resolution_keys:
                if key.endswith('X') or key.endswith('Width'):
                    config[section][key] = str(width)
                else:
                    config[section][key] = str(height)

            # noinspection PyTypeChecker
            # pycharm inspection bad
            config.write(settings_file.open('w'), space_around_delimiters = False)
        else:
            settings_file.write_text(ini_strings)

        sg.popup_ok("Settings successfully loaded!")

    def apply_included(self, to_apply: str):
        ini_strings: str

        match to_apply:
            case 'Performance':
                ini_strings = modes.performance()

            case 'Dx 12 Epic/High':
                ini_strings = modes.dx12()

            case 'Dx 11 Epic/High':
                ini_strings = modes.dx11()

            case _:
                return

        self.apply_settings(ini_strings)
        JsonHandler.dumpjson(
            {
                "mode": to_apply
            }
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self