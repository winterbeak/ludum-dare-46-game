import pygame
import colors

pygame.display.set_mode((100, 100))

tahoma = pygame.font.Font("Tahoma.ttf", 10)


def new_surface(size):
    surface = pygame.Surface(size)
    surface.set_colorkey(colors.TRANSPARENT)
    surface.fill(colors.TRANSPARENT)
    return surface


def remove_color_codes(text):
    text_line = text
    for code in color_codes:
        text_line = text_line.replace("<%s>" % code, "")

    return text_line


def split_into_lines(text, font, max_width):
    line = ""
    lines = []

    first_word = True
    current_width = 0

    # Determines where to split the lines up
    for word in text.split():
        width = font.size(remove_color_codes(word + " "))[0]

        # Special line break denoter
        if word == "<br>":
            lines.append(line)
            line = ""
            first_word = True

            current_width = 0

        # If word makes the line too long, cut this line here
        elif current_width + width > max_width and not first_word:
            lines.append(line)
            line = word + " "

            current_width = width

        # Add word to the line
        else:
            line += word + " "

            current_width += width

        first_word = False

    lines.append(line)

    return lines


def text_block(text, font, color, max_width):
    """ Renders a block of text, and automatically wraps it to a width. """
    lines = split_into_lines(text, font, max_width)

    # Makes the final rendered surface that all the text is rendered on
    line_height = font.get_linesize()
    height = len(lines) * line_height

    surface = new_surface((max_width, height))
    surface.fill(colors.TRANSPARENT)

    # Renders all the lines
    y = 0
    for text_line in lines:

        # Gets rid of all color codes
        text_line = remove_color_codes(text_line)

        rendered_text = font.render(text_line, False, color)
        surface.blit(rendered_text, (0, y))
        y += line_height

    return surface


color_codes = {
    "k" : colors.BLACK,
    "r" : colors.AMBULANCE_RED,
    "o" : colors.ORANGE_TEXT,
}


def colorize(text, code):
    return "<%s>%s<k>" % (code, text)


def text_block_color_codes(text, font, max_width):
    """ Renders a block of wrapped text, and applies color codes to them. """

    lines = split_into_lines(text, font, max_width)
    # Makes the final rendered surface that all the text is rendered on
    line_height = font.get_linesize()
    height = len(lines) * line_height

    surface = new_surface((max_width, height))
    surface.fill(colors.TRANSPARENT)

    # Renders all the lines
    previous_color = colors.BLACK
    y = 0
    for text_line in lines:

        x = 0
        while text_line.count("<") >= 1:
            index = text_line.index("<")
            previous_text = text_line[:index]
            code = text_line[index + 1]
            text_line = text_line[index + 3:]

            rendered_text = font.render(previous_text, False, previous_color)
            surface.blit(rendered_text, (x, y))

            x += rendered_text.get_width()
            previous_color = color_codes[code]

        rendered_text = font.render(text_line, False, previous_color)
        surface.blit(rendered_text, (x, y))
        y += line_height

    return surface


class SpriteColumn:
    def __init__(self, path, sprite_count):
        image = pygame.image.load(path)
        image.convert()
        image.set_colorkey(colors.TRANSPARENT)

        self.surface = image
        self.path = path
        self.sprite_count = sprite_count

        self.single_width = image.get_width()
        self.single_height = int(image.get_height() / sprite_count)
        self.single_size = (self.single_width, self.single_height)

    def draw(self, surface, position, sprite_num):
        width = self.single_width
        height = self.single_height

        y = height * sprite_num

        surface.blit(self.surface, position, (0, y, width, height))


def load_multiple_columns(template_string, column_count, sprite_count):
    columns = []
    for x in range(column_count):
        column = SpriteColumn(template_string % x, sprite_count)
        columns.append(column)

    return columns


class SpriteSheet:
    def __init__(self, column_list):
        self.column_x = []  # x position of each column on the surface
        self.columns = column_list

        width = 0
        height = 0
        for column in column_list:
            self.column_x.append(width)
            width += column.surface.get_width()
            height = max(height, column.surface.get_height())

    def draw(self, surface, position, column_num, sprite_num):
        column = self.columns[column_num]
        column.draw(surface, position, sprite_num)


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

        self.done = False

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        # Automatically loops around when frame reaches end
        if value >= self.sheet.columns[self._col_num].sprite_count:
            value %= self.sheet.columns[self._col_num].sprite_count
            self.done = True
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
        else:
            self._col_num = value
            self._frame = 0
            self.done = False

    @property
    def delay(self):
        return self._delay

    def set_frame_delay(self, col_num, delay):
        frames = self.sheet.columns[col_num].sprite_count
        self._frame_lengths[col_num] = [delay] * frames

    def set_frame_delays(self, col_num, delays):
        self._frame_lengths[col_num] = delays

    @property
    def frame_lengths(self):
        return self._frame_lengths

    @property
    def current_frame_lengths(self):
        """ Returns the frame delays for the current animation. """
        return self._frame_lengths[self._col_num]

    def update(self):
        self._delay += 1
        if self._delay >= self._frame_lengths[self.col_num][self._frame]:
            self.frame += 1
            self._delay = 0

    def draw(self, surface, position):
        self.sheet.draw(surface, position, self._col_num, self._frame)

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
