"""Basic handling of the game's window.

Handles the game's main window, allowing it to be resized and full
screened.
"""

# Note: this file was written by me a while ago!  That's why it's all
# documented, and in a different style than all of my other files.  It
# also happens to be the only thing I wrote a while ago, because I've
# been slacking.  Oh well.

import pygame
import os
import ctypes
import math


os.environ["SDL_VIDEO_CENTERED"] = "1"  # Centers screen

pygame.init()

# Makes sure DPI doesn't mess with the window size.
# My computer (and many others) is 1920x1080, but acts like 1280x720.
# That means that windows are drawn larger than they actually are, and
# makes it so that full screen windows are larger than the monitor.
# This line of code fixes that.
ctypes.windll.user32.SetProcessDPIAware()


# TODO: Expand this list to support more windowed resolutions
RESOLUTIONS = [(800, 600), (1280, 720), (1920, 1080)]
RESOLUTIONS.sort()  # Resolutions should be in order of size.

# Gets the monitor size.
startup_info = pygame.display.Info()
monitor_size = (startup_info.current_w, startup_info.current_h)


def get_display_size():
    """ Find the current size of the game window.

    :return: A (width, height) tuple, the current size of the display.
    """
    info = pygame.display.Info()
    return info.current_w, info.current_h


def find_default_windowed_resolution():
    """ Find the largest resolution that fits comfortably on the monitor.

    Specifically, this is the largest resolution in the list RESOLUTIONS
    that is less than 90% of the user's monitor size.  90% so that the
    screen doesn't reach the very edge of the monitor.

    If no such resolution is found, this returns the smallest resolution
    in the list RESOLUTIONS.

    :return: A (width, height) tuple which is the default windowed
    screen resolution.
    """

    for resolution in reversed(RESOLUTIONS):
        if resolution[0] < monitor_size[0] * 0.9:
            if resolution[1] < monitor_size[1] * 0.9:
                return resolution

    return RESOLUTIONS[0]


default_windowed_resolution = find_default_windowed_resolution()


class Window:
    """ The game's window.

    There should only be one Window or PixelWindow in the entire game.

    :param screen_size: (width, height) pair representing the screen's
    dimensions, in pixels.  Defaults to (0, 0), which is a special case
    that represents full screen.
    """
    def __init__(self, screen_size=(0, 0)):

        self.clock = pygame.time.Clock()

        self._full_screen = False

        # This will be set when full_screen is set
        self.display = None

        # Full screen
        if screen_size == (0, 0):
            self._windowed_resolution = default_windowed_resolution
            self.full_screen = True

        # Not full screen
        else:
            self._windowed_resolution = screen_size
            self.full_screen = False

    def update(self, fps):
        """ Used to update the screen every frame, displaying all changes.

        :param fps: What frames per second to run at.
        """
        pygame.display.flip()
        self.clock.tick(fps)

    @property
    def windowed_resolution(self):
        """ The resolution of the screen when windowed.

        If full screen is currently active, this stores the resolution
        of the window before full screen was entered.  If the window
        started in full screen, this is set to the default windowed
        resolution.
        """
        return self._windowed_resolution

    @windowed_resolution.setter
    def windowed_resolution(self, screen_size):
        """ Change the size of the window.

        If you are in full screen, this brings you out of it.

        PyGame side effect: changing screen size will clear the display.

        :param screen_size: The size, in pixels, to change the window to.
        """
        self._windowed_resolution = screen_size

        if self.full_screen:
            self.full_screen = False
        else:
            self.display = pygame.display.set_mode(screen_size)

    @property
    def full_screen(self):
        """ Boolean that stores if the window is full screen or not. """
        return self._full_screen

    @full_screen.setter
    def full_screen(self, value):
        """ Changes the window from full screen to not full screen. """
        self._full_screen = value
        if value:
            self._enter_full_screen()
        else:
            self._exit_full_screen()

    def _enter_full_screen(self):
        """ Make the window full screen.

        If you are already in full screen, this method will cause the
        screen to briefly stop existing and then exist again.

        PyGame side effect: entering full screen clears the display.
        """

        # Restarting the display fixes a bug where the full screen
        # window displays a scaled version of the windowed resolution.
        pygame.display.quit()
        pygame.display.init()

        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def _exit_full_screen(self):
        """ Make the window not full screen.

        When exiting full screen, the screen size will set to the size
        when full screen was entered.  If the program started out in full
        screen, then it is set to the default resolution.

        You can freely run this method while not in full screen.  Nothing
        will happen.

        PyGame side effect: exiting full screen clears the display.
        """
        self.display = pygame.display.set_mode(self.windowed_resolution)


class PixelWindow(Window):
    """ The game's window, but for games that use pixel art.

    There should only be one Window or PixelWindow in the entire game.

    The process for drawing things goes something like this:
    * Draw on .unscaled anything you want scaled up (ex. pixel art)
    * .scale_blit() to blit .unscaled onto .display, scaled up
    * Draw on .display anything that you don't want scaled (ex. ui)
    * .update() to show the final result on the window

    :param scale: An integer that is the scale multiplier, or by
    how much the screen is scaled by.  For example, if scale is 2,
    then the screen doubles its size.
    :param final_screen_size: (width, height) pair representing the
    screen's dimensions post-scale.  That is, after everything is
    sized up, this is the game's final display size.  Defaults to
    (0, 0), which is a special case that represents full screen.
    """
    def __init__(self, scale, final_screen_size=(0, 0)):

        self._scale = scale

        super().__init__(final_screen_size)

        self.unscaled = None  # Defined in _update_unscaled_size()
        self._update_unscaled_size()

    def _get_pixel_offset(self):
        """ Calculates how much to offset the scaled screen by.

        If the chosen screen size is not a perfect multiple of the scale,
        then the pixel grid will not perfectly fit onto the window.  This
        is compensated for by making the unscaled screen slightly larger.
        For example, if the screen is 100 pixels wide with a 3x scale, the
        unscaled screen will be 34 pixels wide, and when scaled up it will
        be 102 pixels wide.  In this case, one pixel should be cut off on
        both the left and right side of the final screen.  This function
        calculates how many pixels to shift the screen by.

        :return: An (x, y) tuple of integers.  How much to shift the
        screen by.
        """
        full_width = self.unscaled.get_width() * self.scale
        extra_x_pixels = full_width - self.display.get_width()
        x_offset = -math.floor(extra_x_pixels / 2)

        full_height = self.unscaled.get_height() * self.scale
        extra_y_pixels = full_height - self.display.get_height()
        y_offset = -math.floor(extra_y_pixels / 2)

        return x_offset, y_offset

    def scale_blit(self):
        """ Scales .unscaled, then blits it onto .display. """
        width = self.unscaled.get_width() * self.scale
        height = self.unscaled.get_height() * self.scale
        scaled = pygame.transform.scale(self.unscaled, (width, height))

        offset = self._get_pixel_offset()
        self.display.blit(scaled, offset)

    def _update_unscaled_size(self):
        """ Sets the unscaled surface to the correct size.

        After the scale or screen size is changed, this replaces .unscaled
        with a new surface that is the correct size.
        """
        width = math.ceil(self.display.get_width() / self.scale)
        height = math.ceil(self.display.get_height() / self.scale)

        self.unscaled = pygame.Surface((width, height))

    @Window.full_screen.setter
    def full_screen(self, value):
        """ Documented in parent.

        Only difference is that the unscaled window changes size
        accordingly.
        """

        # Calls the parent class's setter
        Window.full_screen.__set__(self, value)
        self._update_unscaled_size()

    @Window.windowed_resolution.setter
    def windowed_resolution(self, screen_size):
        """ Documented in parent.

        Only difference is that the unscaled window changes size
        accordingly.
        """

        # Calls the parent class's setter
        Window.windowed_resolution.__set__(self, screen_size)
        self._update_unscaled_size()

    @property
    def scale(self):
        """ The scale modifier of this window. """
        return self._scale

    @scale.setter
    def scale(self, value):
        """ Changes the scale modifier of this window.

        :param value: The scale modifier.  Must be an integer.
        """
        self._scale = value
        self._update_unscaled_size()
