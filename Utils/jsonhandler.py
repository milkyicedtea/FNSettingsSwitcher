import os
import json


def readjson() -> str:
    try:
        with open(f'{os.getcwd()}/latest.json', 'r') as file:
            latest_mode = json.load(file)['mode']
            file.close()
        return latest_mode
    except FileNotFoundError:
        with open(f'{os.getcwd()}/latest.json', 'w') as file:
            json.dump({
               "mode": "None"
            }, file)
        return 'none'


def dumpjson(to_dump) -> None:
    with open(f'{os.getcwd()}/latest.json', 'w') as file:
        json.dump(to_dump, file)
