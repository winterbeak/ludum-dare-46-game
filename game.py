import pygame
import math
import random

import window
import geometry
import curves
import graphics
import const
import events
import bottles
import incidents

# TODO: change to full screen
# screen = window.PixelWindow(int(window.monitor_size[0] / 320), (0, 0))
screen = window.PixelWindow(2, (1280, 720))
# screen is 640 by 360, scaled to 2x for 720p and 3x for 1080p

# pygame.display.set_caption("Read The Label")

background = graphics.SpriteColumn("images/background.png", 1)
ui = graphics.SpriteColumn("images/test.png", 1)

feed_text = graphics.SpriteColumn("images/feed_text.png", 1)
skip_text = graphics.SpriteColumn("images/skip_text.png", 1)

prev_text = graphics.SpriteColumn("images/prev_text.png", 1)
next_text = graphics.SpriteColumn("images/next_text.png", 1)

homunculus_idle = graphics.SpriteColumn("images/homunculus.png", 4)
homunculus_eat = graphics.SpriteColumn("images/homunculus_eat.png", 8)
homunculus_sprite_sheet = graphics.SpriteSheet([homunculus_idle,
                                                homunculus_eat
                                                ])
HOMUNCULUS_IDLE = 0
HOMUNCULUS_EAT = 1

homunculus = graphics.Animation(homunculus_sprite_sheet)
homunculus.set_frame_delay(HOMUNCULUS_IDLE, 3)
homunculus.set_frame_delay(HOMUNCULUS_EAT, 3)

TIME_ADDED_GREEN = (27, 255, 27)
HOMUNCULUS_ORANGE = const.HOMUNCULUS_ORANGE
AMBULANCE_RED = const.AMBULANCE_RED
MENU_WHITE = (225, 225, 225)

homunculus_text = graphics.SpriteColumn("images/homunculus_text.png", 1)
ambulance_text = graphics.SpriteColumn("images/ambulance_text.png", 1)

one_more_text = graphics.SpriteColumn("images/one_more_text.png", 1)


def draw_debug_countdown(end_time, surface, position):
    time = (end_time - pygame.time.get_ticks()) / 1000
    text = graphics.tahoma.render(str(time), False, const.WHITE)
    surface.blit(text, position)


TEXT_PLACEHOLDER_COLOR = (160, 160, 160)
numbers = graphics.SpriteColumn("images/numbers.png", 11)
numbers_small = graphics.SpriteColumn("images/numbers_small.png", 11)


def render_number(text, color, shake=0):
    width = numbers.single_width * len(text)
    surface = graphics.new_surface((width, numbers.single_height))

    x = 0
    for char in text:
        if char == ":":
            sprite_num = 10
        else:
            sprite_num = int(char)

        x_offset = round((random.random() - 0.5) * (shake * 2))
        y_offset = round((random.random() - 0.5) * (shake * 2))

        numbers.draw(surface, (x + x_offset, y_offset), sprite_num)
        x += numbers.single_width

    pixel_array = pygame.PixelArray(surface)
    pixel_array.replace(TEXT_PLACEHOLDER_COLOR, color)

    return surface


def render_small_number(text, color, shake=0):
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
    pixel_array.replace(TEXT_PLACEHOLDER_COLOR, color)

    return surface


def milliseconds_to_time(total_milliseconds):
    minutes = math.floor(total_milliseconds / 60000)
    seconds = math.floor(total_milliseconds / 1000) % 60
    milliseconds = total_milliseconds % 1000
    return minutes, seconds, milliseconds


def calculate_time_milliseconds(end_time):
    return end_time - pygame.time.get_ticks()


def calculate_time(end_time):
    milliseconds = calculate_time_milliseconds(end_time)
    return milliseconds_to_time(milliseconds)


def draw_countdown(surface, color, time, position, shake=0):
    minutes, seconds, milliseconds = time

    number = render_number("%d:%02d" % (minutes, seconds), color, shake)
    small_number = render_small_number(".%03d" % milliseconds, color, shake)

    surface.blit(number, position)

    x = position[0] + number.get_width()
    y = position[1] + number.get_height() - small_number.get_height()
    surface.blit(small_number, (x, y))


class PlayScreen:

    BOTTLE_SECTION_LEFT = 300
    BOTTLE_SECTION = (BOTTLE_SECTION_LEFT, 0,
                      screen.unscaled.get_width() - BOTTLE_SECTION_LEFT,
                      screen.unscaled.get_height())

    SHIFT_AMOUNT = 500
    SHIFT_LENGTH = 15

    HOMUNCULUS_EAT_DELAY_LENGTH = 5

    AMBULANCE_TIMER_POSITION = (40, 6)
    HOMUNCULUS_TIMER_POSITION = (40, 80)

    def __init__(self):
        self.death_time = 0
        self.ambulance_time = 0
        self.bottle_time = 0

        self.incident_num = 0

        self.generator = bottles.BottleGenerator()
        self.current_bottle = bottles.ghost_bottle
        self.previous_bottle = bottles.ghost_bottle

        self.shift = curves.SineOut(-self.SHIFT_AMOUNT, 0, self.SHIFT_LENGTH)
        self.toss_x = curves.Linear(0, -320, self.SHIFT_LENGTH)
        self.toss_y = curves.QuadraticArc(0, -100, self.SHIFT_LENGTH - 4)
        self.toss_scale = curves.Linear(1, 0.05, self.SHIFT_LENGTH)
        self.toss_rotate = curves.Linear(0, 290, self.SHIFT_LENGTH)
        self.toss_x.frame = self.toss_x.length
        self.toss_y.frame = self.toss_y.length
        self.toss_scale.frame = self.toss_scale.length
        self.toss_rotate.frame = self.toss_rotate.length

        self.homunculus_eat_delay = 0

        self.green_timer_frame = 0
        self.one_more_frame = 0

        self.game_over = False
        self.win = False

    def update(self):

        # If you press the key to feed
        if events.keys.released_key == pygame.K_LEFT:
            self._start_tossing()
            self.previous_bottle = self.current_bottle
            self.current_bottle = self.generator.next_item()

        # If you press the key to trash
        elif events.keys.released_key == pygame.K_RIGHT:
            self._start_shifting()
            self.previous_bottle = self.current_bottle
            self.current_bottle = self.generator.next_item()

        # If currently in tossing animation
        if self.is_tossing():
            self.toss_x.frame += 1
            self.toss_y.frame += 1
            self.toss_scale.frame += 1
            self.toss_rotate.frame += 1
            self.homunculus_eat_delay += 1
            if self.homunculus_eat_delay == self.HOMUNCULUS_EAT_DELAY_LENGTH:
                homunculus.col_num = HOMUNCULUS_EAT

        # Verdict of whether the bottle eaten was lethal or not
        if homunculus.col_num == HOMUNCULUS_EAT:
            if homunculus.frame == 5 and homunculus.delay == 0:
                if self.previous_bottle.lethal:
                    self.game_over = True
                else:
                    self.death_time += self.bottle_time
                    self.green_timer_frame = 30

        # Handles winning and losing due to timers
        if self.death_time > self.ambulance_time:
            self.win = True
        elif calculate_time_milliseconds(self.death_time) < 0:
            self.game_over = True

        # Handles turning the timer green when time is gained
        if self.green_timer_frame > 0:
            self.green_timer_frame -= 1

        # If currently in shifting animation
        if self.is_shifting():
            self.shift.frame += 1

        homunculus.update()
        if homunculus.col_num == HOMUNCULUS_EAT and homunculus.done:
            homunculus.col_num = HOMUNCULUS_IDLE
            self.homunculus_eat_delay = 0

    def is_tossing(self):
        if self.toss_x.frame <= self.toss_x.last_frame:
            return True
        return False

    def _start_tossing(self):
        self.toss_x.frame = 0
        self.toss_y.frame = 0
        self.toss_scale.frame = 0
        self.toss_rotate.frame = 0
        self._start_shifting()

    def is_shifting(self):
        if self.shift.frame <= self.shift.last_frame:
            return True
        return False

    def _start_shifting(self):
        self.shift.frame = 0

    def _draw_bottles_shifting(self, surface):
        bottle1 = self.current_bottle
        x1, y1 = geometry.centered(self.BOTTLE_SECTION, bottle1.total_size)

        if not self.is_tossing():
            bottle2 = self.previous_bottle
            x2, y2 = geometry.centered(self.BOTTLE_SECTION, bottle2.total_size)
            x2 += self.shift.current_value + self.SHIFT_AMOUNT
            surface.blit(bottle2.render(), (x2, y2))

        x1 += self.shift.current_value
        surface.blit(bottle1.render(), (x1, y1))

    def draw_bottles(self, surface):
        # Draws all bottles (except a bottle that's being tossed

        if self.is_shifting():
            self._draw_bottles_shifting(surface)
        else:
            bottle = self.current_bottle
            x, y = geometry.centered(self.BOTTLE_SECTION, bottle.total_size)
            surface.blit(bottle.render(), (x, y))

    def draw_tossed_bottle(self, surface):

        bottle = self.previous_bottle
        x2, y2 = geometry.centered(self.BOTTLE_SECTION, bottle.total_size)
        x2 += self.toss_x.current_value
        y2 += self.toss_y.current_value

        bottle_sprite = bottle.render()
        width = int(bottle_sprite.get_width() * self.toss_scale.current_value)
        height = int(bottle_sprite.get_height() * self.toss_scale.current_value)
        scaled = pygame.transform.scale(bottle_sprite, (width, height))

        angle = self.toss_rotate.current_value
        rotated = pygame.transform.rotate(scaled, angle)

        surface.blit(rotated, (x2, y2))

    def draw_countdowns(self, surface):
        # Ambulance timer
        time = calculate_time(self.ambulance_time)
        position = self.AMBULANCE_TIMER_POSITION
        draw_countdown(surface, AMBULANCE_RED, time, position)

        # Homunculus timer
        milliseconds = calculate_time_milliseconds(self.death_time)
        shake = max(0, (15000 - milliseconds) / 5000)
        if self.green_timer_frame > 0:
            color = TIME_ADDED_GREEN
        else:
            color = HOMUNCULUS_ORANGE

        time = calculate_time(self.death_time)
        position = self.HOMUNCULUS_TIMER_POSITION
        draw_countdown(surface, color, time, position, shake)

    def draw_controls(self, surface):
        # Feed text
        x = 338
        if events.keys.held_key == pygame.K_LEFT:
            x -= 10
        feed_text.draw(surface, (x, 322), 0)

        # Skip text
        x = 481
        if events.keys.held_key == pygame.K_RIGHT:
            x += 10
        skip_text.draw(surface, (x, 324), 0)

    def draw_ui_text(self, surface):
        self.draw_countdowns(surface)

        # Homunculus and ambulance timer labels
        ambulance_text.draw(surface, (5, 7), 0)
        homunculus_text.draw(surface, (5, 88), 0)

        self.draw_controls(surface)

    def draw_homunculus(self, surface):
        y = screen.unscaled.get_height() - homunculus_idle.single_height
        homunculus.draw(surface, (0, y))

    def draw(self, surface):
        background.draw(surface, (0, 0), 0)

        # Bottles that are not tossed appear below UI
        self.draw_bottles(surface)

        ui.draw(surface, (0, 0), 0)
        self.draw_ui_text(surface)

        # Bottles that are tossed appear above UI
        if self.is_tossing():
            self.draw_tossed_bottle(surface)

        self.draw_homunculus(surface)

        # fps_text = graphics.tahoma.render(str(screen.clock.get_fps()), False, const.WHITE, const.BLACK)
        # surface.blit(fps_text, (10, 10))


class MenuScreen(PlayScreen):
    def __init__(self):
        super().__init__()
        self._current_level = incident_list[0]
        self._current_level_number = 0
        self._shift_direction = const.LEFT
        self.current_bottle = incident_list[0].bottle
        self.selected = False

    def update(self):
        homunculus.update()

        if homunculus.col_num == HOMUNCULUS_EAT and homunculus.done:
            homunculus.col_num = HOMUNCULUS_IDLE
            self.homunculus_eat_delay = 0

        if self.is_shifting():
            self.shift.frame += 1

        if events.keys.released_key == pygame.K_SPACE:
            self.selected = True

        elif events.keys.released_key == pygame.K_LEFT:
            if self.current_level_number > 0:
                self.current_level_number -= 1

        elif events.keys.released_key == pygame.K_RIGHT:
            if self.current_level_number < len(incident_list) - 1:
                self.current_level_number += 1

    @property
    def current_level_number(self):
        return self._current_level_number

    @current_level_number.setter
    def current_level_number(self, value):
        if value < self.current_level_number:
            self._shift_direction = const.RIGHT
        elif value > self.current_level_number:
            self._shift_direction = const.LEFT
        else:
            return
        self._current_level_number = value
        self._current_level = incident_list[value]
        self.previous_bottle = self.current_bottle
        self.current_bottle = self._current_level.bottle
        self._start_shifting()

    @property
    def current_level(self):
        return self._current_level

    def draw_ui_text(self, surface):
        self.draw_controls(surface)

    def draw_homunculus(self, surface):
        pass

    def _draw_bottles_shifting(self, surface):
        bottle1 = self.current_bottle
        x1, y1 = geometry.centered(self.BOTTLE_SECTION, bottle1.total_size)

        bottle2 = self.previous_bottle
        x2, y2 = geometry.centered(self.BOTTLE_SECTION, bottle2.total_size)

        if self._shift_direction == const.LEFT:
            x1 -= self.shift.current_value
            x2 -= self.shift.current_value + self.SHIFT_AMOUNT
        else:
            x1 += self.shift.current_value
            x2 += self.shift.current_value + self.SHIFT_AMOUNT

        surface.blit(bottle1.render(), (x1, y1))
        surface.blit(bottle2.render(), (x2, y2))

    def draw(self, surface):
        super().draw(surface)

        text = self.current_level.text
        font = graphics.tahoma
        max_width = self.BOTTLE_SECTION_LEFT - 60
        text_surface = graphics.text_block_color_codes(text, font, max_width)

        width = text_surface.get_width() + 20
        height = surface.get_height() - 40
        text_rect = (20, 20, width, height)
        color = self.current_level.bottle.palette.label_color

        pygame.draw.rect(surface, color, text_rect)
        surface.blit(text_surface, (30, 30))

    def draw_controls(self, surface):
        # Feed text
        x = 338
        if events.keys.held_key == pygame.K_LEFT:
            x -= 10
        prev_text.draw(surface, (x, 10), 0)

        # Skip text
        x = 481
        if events.keys.held_key == pygame.K_RIGHT:
            x += 10
        next_text.draw(surface, (x, 10), 0)


def menu_play_transition(menu, play):
    time = pygame.time.get_ticks()
    play.ambulance_time = time + menu.current_level.ambulance_time
    play.death_time = time + menu.current_level.homunculus_time
    play.bottle_time = menu.current_level.bottle_time

    play.previous_bottle = menu.current_level.bottle

    play.incident_num = menu.current_level.number
    play.generator.level = menu.current_level.number

    play.current_bottle = play.generator.next_item()


incident_list = [
    incidents.generate_basic_incident(),
    incidents.generate_fast_incident(),
]

MENU_SCREEN = 0
menu_screen = MenuScreen()

PLAY_SCREEN = 1
play_screen = PlayScreen()

GAME_OVER_SCREEN = 2
WIN_SCREEN = 3

current_screen = MENU_SCREEN
running = True

while True:

    events.update()

    if events.quit_program:
        break

    if current_screen == MENU_SCREEN:
        menu_screen.update()
        menu_screen.draw(screen.unscaled)

        if menu_screen.selected:
            menu_screen.selected = False
            current_screen = PLAY_SCREEN
            menu_play_transition(menu_screen, play_screen)

    elif current_screen == PLAY_SCREEN:
        play_screen.update()

        if play_screen.game_over:
            play_screen.game_over = False
            current_screen = GAME_OVER_SCREEN

        elif play_screen.win:
            play_screen.win = False
            current_screen = WIN_SCREEN

        else:
            play_screen.draw(screen.unscaled)

    if current_screen == GAME_OVER_SCREEN:
        screen.unscaled.blit(graphics.tahoma.render("GAME OVER", False, const.BLACK), (50, 100))

    if current_screen == WIN_SCREEN:
        screen.unscaled.blit(graphics.tahoma.render("WIN", False, const.BLACK), (50, 100))

    screen.scale_blit()
    screen.update(60)
    screen.clear(const.WHITE)

pygame.quit()
