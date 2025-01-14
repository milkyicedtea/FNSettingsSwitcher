import json
from pathlib import Path
from time import sleep
import FreeSimpleGUI as sg


class JsonHandler:
    __json_file = Path.home().joinpath('fnss_latest.json')
    __config_exists = __json_file.exists()

    @classmethod
    def readjson(cls) -> str:
        try:
            if not cls.__config_exists:
                cls.__json_file.touch()
                cls.dumpjson({"mode": "None"})
                cls.__config_exists = True
            latest_mode = json.loads(cls.__json_file.read_bytes())['mode']
            return latest_mode
        except Exception as e:
            sg.popup_error(f"Error reading configuration: {str(e)}")
            return "None"

    @classmethod
    def dumpjson(cls, to_dump) -> None:
        try:
            if not cls.__config_exists:
                cls.__json_file.touch()
            cls.__json_file.write_text(json.dumps(to_dump))
            sleep(0.1)
        except Exception as e:
            sg.popup_error(f"Error saving configuration: {str(e)}")
