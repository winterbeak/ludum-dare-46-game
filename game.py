import sound

import pygame
import math
import time_math
import random

import window
import geometry
import curves
import graphics
import const
import events
import bottles
import incidents


if window.monitor_size == (1920, 1080):
    screen = window.PixelWindow(3, (0, 0))
elif window.monitor_size == (1280, 720):
    screen = window.PixelWindow(2, (0, 0))
else:
    resolution = window.find_default_windowed_resolution()
    if resolution == (1920, 1080):
        screen = window.PixelWindow(3, (1920, 1080))
    elif resolution == (1280, 720):
        screen = window.PixelWindow(2, (1280, 720))
    else:
        screen = window.PixelWindow(1, (640, 360))

pygame.display.set_caption("READ THE LABEL")
pygame.display.set_icon(pygame.image.load("images/icon_large.png"))

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
win_text = graphics.SpriteColumn("images/win.png", 1)
lose_text = graphics.SpriteColumn("images/lose.png", 1)

ambulance = graphics.SpriteColumn("images/ambulance.png", 1)


# shobango
menu_press = sound.load_numbers("menu_press%d", 1)
menu_release = sound.load_numbers("menu_release%d", 1)
menu_press.set_volumes(0.5)
menu_release.set_volumes(0.5)

feed_press = sound.load_numbers("feed_press%d", 3)
toss = sound.load_numbers("toss%d", 3)
feed_press.set_volumes(0.3)

skip_press = sound.load_numbers("skip_press%d", 3)
slide = sound.load_numbers("slide%d", 3)
skip_press.set_volumes(0.3)

tick = sound.load_numbers("tick%d", 1)
tick.set_volumes(0.3)
subtick = sound.load_numbers("subtick%d", 1)
subtick.set_volumes(0.3)

death = sound.load_numbers("death%d", 1)
death.set_volumes(0.5)

start_release = sound.load_numbers("start_release%d", 1)
start_press = sound.load_numbers("start_press%d", 1)
start_release.set_volumes(0.8)
start_press.set_volumes(0.8)

extra_time = sound.load_numbers("extra_time%d", 1)
extra_time.set_volumes(0.6)

ambulance_arrive = sound.load_numbers("ambulance%d", 1)
ambulance_arrive.set_volumes(0.5)

fast_tick = sound.load_numbers("fast_tick%d", 1)
fast_tick.set_volumes(0.3)
ambulance_pickup = sound.load_numbers("ambulance_pickup_%d", 1)
ambulance_pickup.set_volumes(0.5)

eat = sound.load_numbers("eat%d", 1)
eat.set_volumes(0.8)

win_sound = sound.load_numbers("win%d", 1)
win_sound.set_volumes(0.5)
lose_sound = sound.load_numbers("lose%d", 1)
lose_sound.set_volumes(0.4)


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

    SHIFT_AMOUNT = 600
    SHIFT_LENGTH = 15

    HOMUNCULUS_EAT_DELAY_LENGTH = 5

    AMBULANCE_TIMER_POSITION = (40, 6)
    HOMUNCULUS_TIMER_POSITION = (40, 80)

    DEATH_CIRCLE_COUNT = 8

    def __init__(self):
        self.previous_tick_time = 0

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

        self.ambulance_anim_countdown = 0
        self.death_anim_countdown = 0

        self.death_anim_frame = 0
        self.death_circles = []

        self.in_animation = False

        self.ambulance_entrance = curves.SineOut(1000, -250, 80)
        self.ambulance_exit = curves.SineOut(-250, -1000, 80)
        self.ambulance_x = 1000

        self.bottles = []
        self.allergies = []
        self.allergy_triggers = []

    def update(self):

        if not self.in_animation:

            if events.keys.pressed_key == pygame.K_LEFT:
                feed_press.play_random()
            elif events.keys.pressed_key == pygame.K_RIGHT:
                skip_press.play_random()

            # If you press the key to feed
            if events.keys.released_key == pygame.K_LEFT:
                toss.play_random()
                self._start_tossing()
                self.previous_bottle = self.current_bottle
                self.current_bottle = self.generator.next_item()
                self.bottles.append(self.current_bottle)

            # If you press the key to trash
            elif events.keys.released_key == pygame.K_RIGHT:
                slide.play_random()
                self._start_shifting()
                self.previous_bottle = self.current_bottle
                self.current_bottle = self.generator.next_item()
                self.bottles.append(self.current_bottle)

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
            if homunculus.frame == 4 and homunculus.delay == 0:
                eat.play_random()

            # TODO: Exploit, spamming FEED fast enough can bypass this check
            # If you feed faster than this animation takes to get to frame 5,
            # you can skip the game over check.  It takes some pretty quick
            # spamming, though, so it's not too much of an issue.
            if homunculus.frame == 5 and homunculus.delay == 0:
                self.previous_bottle.eaten = True

                # Applies all allergies
                for allergy in self.previous_bottle.allergies:
                    if allergy not in self.allergies:
                        self.allergies.append(allergy)
                        self.previous_bottle.adds_allergies.append(allergy)

                # Checks if the bottle has a lethal side effect
                lethal = self.previous_bottle.lethal

                # Checks if an allergy was triggered
                triggers_allergy = False
                for allergen in self.previous_bottle.allergens:
                    if allergen in self.allergies:
                        triggers_allergy = True
                        self.allergy_triggers.append(allergen)

                if lethal or triggers_allergy:
                    death.play_random()
                    self.game_over = True
                    self.in_animation = True
                    self.bottles.pop()  # Removes the bottle that's sliding in
                else:
                    self.death_time += self.bottle_time
                    self.green_timer_frame = 30
                    extra_time.play_random()

        # Handles winning and losing due to timers
        if self.death_time > self.ambulance_time and not self.win:
            self.in_animation = True
            self.ambulance_anim_countdown = time_math.ms_time_to(self.ambulance_time)
            self.death_anim_countdown = time_math.ms_time_to(self.death_time)
            self.win = True
            self.bottles.pop()  # Removes the bottle that's sliding in

        elif time_math.ms_time_to(self.death_time) < 0 and not self.game_over:
            self.in_animation = True
            self.game_over = True
            death.play_random()

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

        if not self.in_animation:
            prev_before = (self.death_time - self.previous_tick_time) % 1000 < 500
            next_after = time_math.ms_time_to(self.death_time) % 1000 > 500
            if prev_before and next_after:
                tick.play_random()

            time = time_math.ms_time_to(self.death_time)
            if time > 30000:
                interval = 1000
            elif time > 15000:
                interval = 500
            elif time > 5000:
                interval = 250
            else:
                interval = 125

            if (self.death_time - self.previous_tick_time) % interval < interval / 2:
                if time_math.ms_time_to(self.death_time) % interval > interval / 2:
                    subtick.play_random()

        self.previous_tick_time = pygame.time.get_ticks()

        # Win animation
        if self.win:
            if self.ambulance_entrance.frame == 1:
                ambulance_arrive.play_random()
            elif self.ambulance_exit.frame == 1:
                ambulance_pickup.play_random()

            if self.ambulance_anim_countdown > 0:
                self.ambulance_anim_countdown -= 400
                if self.ambulance_anim_countdown % 1600 < 400:
                    fast_tick.play_random()
                if self.ambulance_anim_countdown <= 0:
                    self.death_time = self.death_time - self.ambulance_anim_countdown
                    self.ambulance_anim_countdown = 0
                else:
                    self.death_anim_countdown -= 400
            else:
                if self.ambulance_entrance.frame < self.ambulance_entrance.length - 1:
                    self.ambulance_entrance.frame += 1
                    self.ambulance_x = self.ambulance_entrance.current_value
                else:
                    self.ambulance_exit.frame += 1

                    if self.ambulance_exit.frame > self.ambulance_exit.length:
                        self.in_animation = False
                    else:
                        self.ambulance_x = self.ambulance_exit.current_value

        elif self.game_over:
            if self.death_anim_frame % 10 == 0:
                if len(self.death_circles) < self.DEATH_CIRCLE_COUNT:
                    self.death_circles.append(0)
                else:
                    if self.death_circles[-1] >= 1000:
                        self.in_animation = False

            for index in range(len(self.death_circles)):
                if self.death_circles[index] < 1000:
                    self.death_circles[index] += 20

            self.death_anim_frame += 1

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
            surface.blit(self.render_bottle(bottle2), (x2, y2))

        x1 += self.shift.current_value
        surface.blit(self.render_bottle(bottle1), (x1, y1))

    def render_bottle(self, bottle):
        return bottle.render()

    def draw_bottles(self, surface):
        # Draws all bottles (except a bottle that's being tossed

        if self.is_shifting():
            self._draw_bottles_shifting(surface)
        else:
            bottle = self.current_bottle
            x, y = geometry.centered(self.BOTTLE_SECTION, bottle.total_size)
            surface.blit(self.render_bottle(bottle), (x, y))

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
        if self.win:
            time = time_math.ms_to_min_sec_ms(self.ambulance_anim_countdown)
        else:
            time = time_math.min_sec_ms_time_to(self.ambulance_time)
        position = self.AMBULANCE_TIMER_POSITION
        draw_countdown(surface, AMBULANCE_RED, time, position)

        # Homunculus timer
        milliseconds = time_math.ms_time_to(self.death_time)
        if self.win:
            shake = 0
        else:
            shake = max(0, (15000 - milliseconds) / 5000)
        if self.green_timer_frame > 0:
            color = TIME_ADDED_GREEN
        else:
            color = HOMUNCULUS_ORANGE

        if self.win:
            time = time_math.ms_to_min_sec_ms(self.death_anim_countdown)
        elif self.game_over:
            time = (0, 0, 0)
        else:
            time = time_math.min_sec_ms_time_to(self.death_time)
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

        if not self.win or self.ambulance_entrance.frame < self.ambulance_entrance.length - 1:
            self.draw_homunculus(surface)

        if self.win:
            ambulance.draw(surface, (self.ambulance_x, 162), 0)

        if self.game_over:
            for circle_num, circle in enumerate(self.death_circles):
                if circle_num > len(self.death_circles) - 5:
                    color = (circle_num * -20 + self.DEATH_CIRCLE_COUNT * 20 - 20, ) * 3
                    pygame.draw.circle(surface, color, (117, 229), circle)

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
        self.quit = False

    def update(self):
        homunculus.update()

        if homunculus.col_num == HOMUNCULUS_EAT and homunculus.done:
            homunculus.col_num = HOMUNCULUS_IDLE
            self.homunculus_eat_delay = 0

        if self.is_shifting():
            self.shift.frame += 1

        if events.keys.released_key == pygame.K_SPACE:
            start_release.play_random()
            self.selected = True

        elif events.keys.released_key == pygame.K_LEFT:
            menu_release.play_random()
            if self.current_level_number > 0:
                self.current_level_number -= 1

        elif events.keys.released_key == pygame.K_RIGHT:
            menu_release.play_random()
            if self.current_level_number < len(incident_list) - 1:
                self.current_level_number += 1

        if events.keys.pressed_key == pygame.K_ESCAPE:
            self.quit = True

        if events.keys.pressed_key == pygame.K_SPACE:
            start_press.play_random()
        elif events.keys.pressed_key == pygame.K_LEFT:
            menu_press.play_random()
        elif events.keys.pressed_key == pygame.K_RIGHT:
            menu_press.play_random()

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

        surface.blit(self.render_bottle(bottle1), (x1, y1))
        surface.blit(self.render_bottle(bottle2), (x2, y2))

    def draw(self, surface):
        super().draw(surface)

        # Handles the level description text
        text = self.current_level.text
        font = graphics.tahoma
        max_width = self.BOTTLE_SECTION_LEFT - 60
        text_surface = graphics.text_block_color_codes(text, font, max_width)

        # Handles the level description box
        width = text_surface.get_width() + 20
        height = surface.get_height() - 40
        text_rect = (20, 20, width, height)
        color = self.current_level.bottle.palette.label_color

        # Draws them both
        pygame.draw.rect(surface, color, text_rect)
        surface.blit(text_surface, (30, 30))

    def draw_controls(self, surface):
        # Prev text
        x = 338
        if events.keys.held_key == pygame.K_LEFT:
            x -= 10
        prev_text.draw(surface, (x, 10), 0)

        # Next text
        x = 481
        if events.keys.held_key == pygame.K_RIGHT:
            x += 10
        next_text.draw(surface, (x, 10), 0)


class ResultScreen(MenuScreen):

    def __init__(self):
        super().__init__()
        self.bottles = None
        self.background = None
        self._bottle_num = 0
        self.allergies = []
        self.win = False
        self.TEXT_SECTION = (0, 0, self.BOTTLE_SECTION_LEFT, screen.unscaled.get_height())

    def update(self):
        if self.is_shifting():
            self.shift.frame += 1

        if events.keys.released_key == pygame.K_SPACE:
            self.selected = True

        elif events.keys.released_key == pygame.K_LEFT:

            menu_release.play_random()

            if self.bottle_num > 0:
                for allergy in self.current_bottle.adds_allergies:
                    self.allergies.remove(allergy)

                self.bottle_num -= 1

        elif events.keys.released_key == pygame.K_RIGHT:

            menu_release.play_random()

            if self.bottle_num < len(self.bottles) - 1:
                self.bottle_num += 1

                for allergy in self.current_bottle.adds_allergies:
                    self.allergies.append(allergy)

        if events.keys.released_key == pygame.K_SPACE:
            start_release.play_random()
            self.selected = True

        if events.keys.pressed_key == pygame.K_SPACE:
            start_press.play_random()

        if events.keys.pressed_key == pygame.K_LEFT:
            menu_press.play_random()
        elif events.keys.pressed_key == pygame.K_RIGHT:
            menu_press.play_random()

    def render_bottle(self, bottle):
        return bottle.render_color_codes()

    def draw(self, surface):
        if self.win:
            self.background.draw(surface, (0, 0), 0)
        else:
            surface.fill(const.BLACK)

        self.draw_bottles(surface)
        if self.win:
            ui.draw(surface, (0, 0), 0)

        self.draw_controls(surface)

        # Draws return to menu text
        text = graphics.tahoma.render("Press SPACE to return to level select.", False, const.BLACK)
        text_x = (self.BOTTLE_SECTION_LEFT - text.get_width()) / 2

        rect = (text_x - 10, 250, text.get_width() + 20, text.get_height() + 20)
        pygame.draw.rect(surface, const.WHITE, rect)

        surface.blit(text, (text_x, 260))

        # Draws game analysis text
        if self.current_bottle.eaten:
            string = graphics.colorize("Eaten.", "r")
        else:
            string = graphics.colorize("Skipped.", "o")

        if self.allergies:
            string += " <br> Allergies: " + ", ".join(self.allergies)
        max_width = self.BOTTLE_SECTION[2] - 40
        text = graphics.text_block_color_codes(string, graphics.tahoma, max_width)

        text_x = self.BOTTLE_SECTION[0] + 20

        rect = (text_x - 10, 310, text.get_width() + 20, text.get_height() + 20)
        pygame.draw.rect(surface, const.WHITE, rect)

        surface.blit(text, (text_x, 320))

        # Draws win/lose text
        if self.win:
            sprite = win_text
            sprite.draw(surface, (48, 50), 0)
        else:
            sprite = lose_text

            size = (sprite.single_width, sprite.single_height)
            x, y = geometry.centered(self.TEXT_SECTION, size)
            y -= 50
            sprite.draw(surface, (x, y), 0)

    @property
    def bottle_num(self):
        return self._bottle_num

    @bottle_num.setter
    def bottle_num(self, value):
        if value < self._bottle_num:
            self._shift_direction = const.RIGHT
        elif value > self._bottle_num:
            self._shift_direction = const.LEFT
        else:
            return
        self._bottle_num = value
        self.previous_bottle = self.current_bottle
        self.current_bottle = self.bottles[value]
        self._start_shifting()


def menu_play_transition(menu, play):
    time = pygame.time.get_ticks()
    play.ambulance_time = time + menu.current_level.ambulance_time
    play.death_time = time + menu.current_level.homunculus_time
    play.bottle_time = menu.current_level.bottle_time

    play.previous_bottle = menu.current_level.bottle

    play.incident_num = menu.current_level.number
    play.generator.level = menu.current_level.number

    play.current_bottle = play.generator.next_item()
    play.bottles = [play.current_bottle]


def play_result_transition(play, result):
    allergies = []
    for bottle_index, bottle in enumerate(play.bottles):

        if bottle.eaten:
            allergies += bottle.allergies

        # Colors red any allergens that are deadly
        for allergen_index, allergen in enumerate(bottle.allergens):
            if allergen in allergies:
                string = graphics.colorize(allergen, "r")
                play.bottles[bottle_index].allergens[allergen_index] = string

        # Colors any allergies in orange
        for effect_index, effect in enumerate(bottle.effects):
            if effect.endswith("allergy"):
                string = graphics.colorize(effect, "o")
                play.bottles[bottle_index].effects[effect_index] = string

    result.allergies = play.allergies
    result.bottles = play.bottles
    result.current_bottle = play.previous_bottle
    result.bottle_num = len(result.bottles) - 1
    result.shift.frame = result.shift.length

    if play_screen.win:
        result.win = True
        win_sound.play_random()
    else:
        result.win = False
        lose_sound.play_random()


incident_list = [
    incidents.generate_basic_incident(),
    incidents.generate_allergen_incident(),
    incidents.generate_mixed_incident(),
    incidents.generate_fast_incident(),
    incidents.generate_basic_hard_incident(),
]

MENU_SCREEN = 0
menu_screen = MenuScreen()

PLAY_SCREEN = 1
play_screen = PlayScreen()

RESULT_SCREEN = 2
result_screen = ResultScreen()
result_screen.background = background

current_screen = MENU_SCREEN
running = True

while True:

    events.update()

    if events.quit_program:
        break

    if current_screen == MENU_SCREEN:
        menu_screen.update()
        menu_screen.draw(screen.unscaled)

        if menu_screen.quit:
            break

        if menu_screen.selected:
            menu_screen.selected = False
            current_screen = PLAY_SCREEN
            menu_play_transition(menu_screen, play_screen)

    elif current_screen == PLAY_SCREEN:
        play_screen.update()

        if (play_screen.game_over or play_screen.win) and not play_screen.in_animation:
            play_result_transition(play_screen, result_screen)

            play_screen.game_over = False
            play_screen.win = False
            current_screen = RESULT_SCREEN
            # Since play_screen is not drawn, skip a frame
            continue

        else:
            play_screen.draw(screen.unscaled)

    elif current_screen == RESULT_SCREEN:
        result_screen.update()
        result_screen.draw(screen.unscaled)

        if result_screen.selected:
            result_screen.selected = False
            current_screen = MENU_SCREEN

            play_screen = PlayScreen()

    screen.scale_blit()
    screen.update(60)
    screen.clear(const.WHITE)

pygame.quit()
