import os
import PySimpleGUI as sg
from PySimpleGUI import Window
from Utils.jsonhandler import dumpjson, readjson
import Utils.modes as modes


def updatePerformance(window: Window):
    window['Dx12'].update(button_color = ('#000000', '#fdcb52'))
    window['Performance'].update(button_color = ('white', 'green'))
    window['Dx11'].update(button_color = ('#000000', '#fdcb52'))
    dumpjson(
        {
            "mode": "Performance"
        }
    )
    window['ModeTxt'].update(f"You last set your settings to: {readjson()}")


def updateDx12(window: Window):
    window['Performance'].update(button_color = ('#000000', '#fdcb52'))
    window['Dx12'].update(button_color = ('white', 'green'))
    window['Dx11'].update(button_color = ('#000000', '#fdcb52'))
    dumpjson(
        {
            "mode": "Dx12"
        }
    )
    window['ModeTxt'].update(f"You last set your settings to: {readjson()}")


def updateDx11(window: Window):
    window['Performance'].update(button_color = ('#000000', '#fdcb52'))
    window['Dx12'].update(button_color = ('#000000', '#fdcb52'))
    window['Dx11'].update(button_color = ('white', 'green'))
    dumpjson(
        {
            "mode": "Dx11"
        }
    )
    window['ModeTxt'].update(f"You last set your settings to: {readjson()}")


class ButtonHandlers:
    def __init__(self):
        self.config_folder = f"{os.getenv('LOCALAPPDATA')}/FortniteGame/Saved/Config/WindowsClient"

    def setPerformance(self, window: Window):
        updatePerformance(window)
        stretched = sg.popup_yes_no("Do you want streched res? Default stretched res is 1680x1050")
        with open(self.config_folder + "/GameUserSettings.ini", "w") as file:
            if stretched == "Yes":
                file.write(modes.Performance_stretched())
            else:
                file.write(modes.Performance_1080p())

    def setDx12(self, window: Window):
        updateDx12(window)
        stretched = sg.popup_yes_no("Do you want streched res? Default stretched res is 1680x1050")
        with open(self.config_folder + "/GameUserSettings.ini", "w") as file:
            if stretched == "Yes":
                file.write(modes.Dx12_stretched())
            else:
                file.write(modes.Dx12_1080p())

    def setDx11(self, window: Window):
        updateDx11(window)
        stretched = sg.popup_yes_no("Do you want streched res? Default stretched res is 1680x1050")
        with open(self.config_folder + "/GameUserSettings.ini", "w") as file:
            if stretched == "Yes":
                file.write(modes.Dx11_stretched())
            else:
                file.write(modes.Dx11_1080p())
