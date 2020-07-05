import math
import pygame


def ms_to_min_sec_ms(total_milliseconds):
    minutes = math.floor(total_milliseconds / 60000)
    seconds = math.floor(total_milliseconds / 1000) % 60
    milliseconds = total_milliseconds % 1000
    return minutes, seconds, milliseconds


def min_sec_ms_to_ms(time):
    return time[0] * 60000 + time[1] * 1000 + time[2]


def ms_time_to(end_time):
    return end_time - pygame.time.get_ticks()


def min_sec_ms_time_to(end_time):
    milliseconds = ms_time_to(end_time)
    return ms_to_min_sec_ms(milliseconds)


def crosses_interval(x, y, i):
    """ Returns whether there is a multiple of i between x and y.

    x and y must be integers.
    If x and y are both equal to the same multiple of i, this returns False.
    If one of x or y is equal to a multiple of i, and no other multiples are
    crossed between the two, this returns True only if the one on the interval
    is the greater of the two.
    """
    if x == y:
        return False
    if x // i == y // i:
        return False
    return True
