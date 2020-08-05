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
left_text = files.load_png_column("left_text", 13)
LEFT_TEXT_STRING = "BOTTLES LEFT"


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


def render_left_count(count, exclamation, color, shake=0):
    number_string = str(count)

    # Calculates the size of the surface
    left_text_length = len(LEFT_TEXT_STRING)
    if exclamation:
        left_text_length += 1  # Exclamation mark adds one to the length
    if count == 1:
        left_text_length -= 1  # Non plural removes an "S"

    number_width = numbers.single_width * len(number_string)
    text_width = left_text.single_width * (left_text_length + 1)
    width = number_width + text_width
    surface = graphics.new_surface((width, numbers.single_height))

    # Draws the number
    x = 0
    for char in number_string:
        if char != " ":
            sprite_num = int(char)

            x_offset = round((random.random() - 0.5) * (shake * 2))
            y_offset = round((random.random() - 0.5) * (shake * 2))

            numbers.draw(surface, (x + x_offset, y_offset), sprite_num)

        x += numbers.single_width

    # Draws the "Bottles Left" text
    y = numbers.single_height - left_text.single_height - 5
    x += left_text.single_width

    if exclamation:
        end = left_text.sprite_count + 1
    else:
        end = left_text.sprite_count

    for index in range(end):
        # Skips the "S" if there is only one bottle left
        if count == 1 and index == LEFT_TEXT_STRING.index("S"):
            continue

        x_offset = round((random.random() - 0.5) * (shake * 2))
        y_offset = round((random.random() - 0.5) * (shake * 2))

        left_text.draw(surface, (x + x_offset, y + y_offset), index)

        x += left_text.single_width

    pixel_array = pygame.PixelArray(surface)
    pixel_array.replace(colors.TEXT_PLACEHOLDER, color)

    return surface


def draw_timer(surface, color, time, position, shake=0):
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
