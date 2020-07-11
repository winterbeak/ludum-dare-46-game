import json
import os

import graphics


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


def json_path(string):
    return os.path.join("data", string + ".json")


def png_path(string):
    return os.path.join("images", string + ".png")


def load_png_sprite(string):
    return graphics.Sprite(png_path(string))


def load_png_column(string, sprite_count):
    return graphics.SpriteColumn(png_path(string), sprite_count)
