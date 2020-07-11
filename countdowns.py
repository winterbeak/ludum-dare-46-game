import pygame
import random

import files
import graphics
import colors


# Countdown stuff
def draw_debug(end_time, surface, position):
    """ Draws a primitive, unstylized countdown. """
    time = (end_time - pygame.time.get_ticks()) / 1000
    text = graphics.tahoma.render(str(time), False, colors.WHITE)
    surface.blit(text, position)


numbers = files.load_png_column("numbers", 11)
numbers_small = files.load_png_column("numbers_small", 11)


def render_number(text, color, shake=0):
    """ Renders a number using numbers.png.

    Supports the : character.  Ignores the negative sign.
    """
    width = numbers.single_width * len(text)
    surface = graphics.new_surface((width, numbers.single_height))

    x = 0
    for char in text:
        if char == "-":
            continue

        if char == ":":
            sprite_num = 10
        else:
            sprite_num = int(char)

        x_offset = round((random.random() - 0.5) * (shake * 2))
        y_offset = round((random.random() - 0.5) * (shake * 2))

        numbers.draw(surface, (x + x_offset, y_offset), sprite_num)
        x += numbers.single_width

    pixel_array = pygame.PixelArray(surface)
    pixel_array.replace(colors.TEXT_PLACEHOLDER, color)

    return surface


def render_small_number(text, color, shake=0):
    """ Renders a number using numbers_small.png.

    Supports the . character.
    """
    width = numbers_small.single_width * len(text)
    surface = graphics.new_surface((width, numbers_small.single_height))

    x = 0
    for char in text:
        if char == ".":
            sprite_num = 10
        else:
            sprite_num = int(char)

        x_offset = round((random.random() - 0.5) * (shake * 2))
        y_offset = round((random.random() - 0.5) * (shake * 2))

        numbers_small.draw(surface, (x + x_offset, y_offset), sprite_num)
        x += numbers_small.single_width

    pixel_array = pygame.PixelArray(surface)
    pixel_array.replace(colors.TEXT_PLACEHOLDER, color)

    return surface


def draw(surface, color, time, position, shake=0):
    """ Draws the countdown to a given time.

    The time variable is a 3-tuple in minutes/seconds/milliseconds form.
    """
    minutes, seconds, milliseconds = time

    number = render_number("%d:%02d" % (minutes, seconds), color, shake)
    small_number = render_small_number(".%03d" % milliseconds, color, shake)

    surface.blit(number, position)

    x = position[0] + number.get_width()
    y = position[1] + number.get_height() - small_number.get_height()
    surface.blit(small_number, (x, y))
