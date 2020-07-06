import json


def json_read(path):
    with open(path, "r") as file:
        data = json.load(file)
    return data


def json_write(path, obj, formatted=True):
    with open(path, "w+") as file:
        if formatted:
            json.dump(obj, file, indent=4)
        else:
            json.dump(obj, file)
