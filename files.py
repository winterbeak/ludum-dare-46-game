import json


def json_read(path):
    with open(path, "r") as file:
        data = json.load(file)
    return data


def json_write(path, obj):
    with open(path, "w+") as file:
        json.dump(obj, file)
