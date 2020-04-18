import pygame
import const


class SpriteColumn:
    def __init__(self, path, sprite_count):
        image = pygame.image.load(path)
        image.convert()
        image.set_colorkey(const.TRANSPARENT)

        self.surface = image
        self.path = path
        self.sprite_count = sprite_count

        self.single_width = image.get_width()
        self.single_height = int(image.get_height() / sprite_count)


class SpriteSheet:
    def __init__(self, column_list):
        self.column_x = []  # x position of each column on the surface
        self.columns = column_list

        width = 0
        height = 0
        for column in column_list:
            column_x = width
            width += column.surface.get_width()
            height = max(height, column.surface.get_height())

    def draw_sprite(self, surface, position, column_num, frame_num):
        column = self.columns[column_num]

        width = column.single_width
        height = column.single_height
        sprite_y = height * frame_num

        surface.blit(column.surface, position, (0, sprite_y, width, height))


class Animation:
    def __init__(self, sprite_sheet):
        self._frame_lengths = []
        for column in sprite_sheet.columns:
            frames = column.sprite_count
            self._frame_lengths.append([1] * frames)

        self._delay = 0
        self._frame = 0
        self._col_num = 0
        self.sheet = sprite_sheet

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        # Automatically loops around when frame reaches end
        value %= self.sheet.columns[self._col_num].sprite_count
        self._frame = value

    @property
    def col_num(self):
        return self._col_num

    @col_num.setter
    def col_num(self, value):
        if value >= len(self.sheet.columns):
            print("Tried to set to an invalid animation " +
                  "(%d when %d is the max)" % (value, len(self.sheet.columns)))
        elif value < 0:
            print("Tried to set to an invalid animation " +
                  "(%d when 0 is the min)" % value)

    def set_frame_delay(self, col_num, delay):
        frames = self.sheet.columns[col_num].sprite_count
        self._frame_lengths[col_num] = [delay] * frames

    def set_frame_delays(self, col_num, delays):
        self._frame_lengths[col_num] = delays

    def update(self):
        self._delay += 1
        if self._delay >= self._frame_lengths[self.col_num][self._frame]:
            self.frame += 1
            self._delay = 0

    def draw(self, surface, position):
        self.sheet.draw_sprite(surface, position, self._col_num, self._frame)

# import window
# test_window = window.PixelWindow(10, (320, 180))
#
# test_column_tumble = SpriteColumn("images/tumble.png", 6)
# test_column_run = SpriteColumn("images/run.png", 6)
# test_sprite_sheet = SpriteSheet([test_column_tumble, test_column_run])
# test_animation = Animation(test_sprite_sheet)
# test_animation.set_frame_delay(0, 10)
#
# print(test_column_tumble.single_height)
# for frame in range(150):
#     test_animation.draw(test_window.unscaled, (0, 0))
#     test_animation.update()
#
#     test_window.scale_blit()
#     test_window.update(60)
#     test_window.clear()
#
# pygame.quit()
