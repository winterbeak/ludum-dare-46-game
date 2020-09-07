import sound

import pygame
import pygame.gfxdraw

import events
import window
import geometry
import curves
import graphics
import save
import files
import time_math
import misc

import const
import colors

import bottles
import incidents
import countdowns

# TODO: Fix this window sizing code.
# Sets window size
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


# Caption and image of the game window
pygame.display.set_caption("READ THE LABEL")
pygame.display.set_icon(pygame.image.load(files.png_path("icon_large")))


# Graphics loading
background = files.load_png_sprite("background")
ui = files.load_png_sprite("test")

feed_text = files.load_png_sprite("feed_text")
skip_text = files.load_png_sprite("skip_text")

key_left = files.load_png_sprite("key_left")
key_right = files.load_png_sprite("key_right")

row_cap_left = files.load_png_sprite("row_cap_left")
row_cap_right = files.load_png_sprite("row_cap_right")
row_pointer = files.load_png_sprite("row_pointer")

homunculus_idle = files.load_png_column("homunculus", 4)
homunculus_eat = files.load_png_column("homunculus_eat", 8)
homunculus_sprite_sheet = graphics.SpriteSheet([homunculus_idle,
                                                homunculus_eat
                                                ])
HOMUNCULUS_IDLE = 0
HOMUNCULUS_EAT = 1

homunculus = graphics.Animation(homunculus_sprite_sheet)
homunculus.set_frame_delay(HOMUNCULUS_IDLE, 3)
homunculus.set_frame_delay(HOMUNCULUS_EAT, 3)

homunculus_text = files.load_png_sprite("homunculus_text")
ambulance_text = files.load_png_sprite("ambulance_text")

one_more_text = files.load_png_sprite("one_more_text")
win_text = files.load_png_sprite("win")
lose_text = files.load_png_sprite("lose")

ambulance = files.load_png_sprite("ambulance")

checkmark = files.load_png_sprite("checkmark")
cross = files.load_png_sprite("cross")


# Sound loading
menu_press = sound.load_numbers("menu_press%d", 1, volumes=0.5)
menu_release = sound.load_numbers("menu_release%d", 1, volumes=0.5)

feed_press = sound.load_numbers("feed_press%d", 3, volumes=0.3)
feed_release = sound.load_numbers("feed_release%d", 3)

skip_press = sound.load_numbers("skip_press%d", 3, volumes=0.3)
skip_release = sound.load_numbers("skip_release%d", 3)

tick = sound.load_numbers("tick%d", 1, volumes=0.3)
subtick = sound.load_numbers("subtick%d", 1, volumes=0.3)

death = sound.load_numbers("death%d", 1, volumes=0.5)

start_release = sound.load_numbers("start_release%d", 1, volumes=0.8)
start_press = sound.load_numbers("start_press%d", 1, volumes=0.8)

correct = sound.load_numbers("correct%d", 1, volumes=0.6)
incorrect = sound.load_numbers("incorrect%d", 1, volumes=0.6)

ambulance_arrive = sound.load_numbers("ambulance%d", 1, volumes=0.5)

fast_tick = sound.load_numbers("fast_tick%d", 1, volumes=0.3)
ambulance_pickup = sound.load_numbers("ambulance_pickup_%d", 1, volumes=0.5)

eat = sound.load_numbers("eat%d", 1, volumes=0.8)

win_sound = sound.load_numbers("win%d", 1, volumes=0.5)
lose_sound = sound.load_numbers("lose%d", 1, volumes=0.4)


class BottleIconRow:
    ICON_SCALE = 10
    ICON_SPACING = 12

    def __init__(self, bottle_list, position, width):
        self.bottles = bottle_list
        self._position = position
        self._width = width
        self._scroll = 0
        self.selected_bottle_num = 0

    def update(self):
        self._update_scroll()

    def draw(self, surface, symbols=None):

        bottle_position = self._position.offset(2, 3)
        bottle_row = self._render_icons(symbols)
        surface.blit(bottle_row, bottle_position)

        self._draw_ui(surface)

    def _update_scroll(self):
        target = self._center_x_of_selected_bottle()
        diff = target - self._scroll
        if abs(diff) > 0.001:
            self._scroll += diff / 5

    def _center_x_of_selected_bottle(self):
        scale = self.ICON_SCALE
        bottle_num = self.selected_bottle_num

        x = 0
        for i in range(bottle_num):
            x += self.bottles[i].downscaled_total_width(scale)
            x += self.ICON_SPACING
        x += self.bottles[bottle_num].downscaled_total_width(scale) // 2
        return x

    def _max_icon_height(self):
        scale = self.ICON_SCALE

        height = 0
        for bottle in self.bottles:
            bottle_height = bottle.downscaled_total_height(scale)
            height = max(height, bottle_height)

        return height

    def _render_icons(self, symbols=None):
        if symbols:
            misc.force_length(symbols, len(self.bottles), const.SYMBOL_NONE)
        else:
            symbols = [const.SYMBOL_NONE] * len(self.bottles)

        scale = self.ICON_SCALE

        height = self._max_icon_height() + 4
        surface = graphics.new_surface((self._width, height))

        x = -self._scroll + self._width // 2
        for bottle, symbol in zip(self.bottles, symbols):
            bottle_width = bottle.downscaled_total_width(scale)

            # Skips any bottle that isn't rendered due to the offset
            if x + bottle_width > 0:
                y = (height - bottle.downscaled_total_height(scale)) // 2
                sprite = bottle.render_downscaled_body(scale)
                surface.blit(sprite, (x, y))

                if symbol == const.SYMBOL_CHECK:
                    check_x = x + bottle_width - 8
                    check_y = y + bottle.downscaled_total_height(scale) - 10
                    checkmark.draw(surface, (check_x, check_y))

                elif symbol == const.SYMBOL_CROSS:
                    cross_x = x + bottle_width - 8
                    cross_y = y + bottle.downscaled_total_height(scale) - 10
                    cross.draw(surface, (cross_x, cross_y))

            x += bottle_width + self.ICON_SPACING

            # Stops rendering bottles if the end of the surface is reached
            if x > self._width:
                break

        return surface

    def _draw_ui(self, surface):
        surface.blit(row_cap_left.render(), self._position.coords)

        self._draw_pointer(surface)

        right_cap_position = self._position.offset(self._width, 0)
        surface.blit(row_cap_right.render(), right_cap_position)

    def _draw_pointer(self, surface):
        x = self._position.x + (self._width // 2) - 3
        x += self._center_x_of_selected_bottle()
        x -= int(self._scroll)

        bottle = self.bottles[self.selected_bottle_num]
        y = self._position.y + 6
        y -= bottle.downscaled_total_height(self.ICON_SCALE) // 2
        surface.blit(row_pointer.render(), (x, y))


class Screen:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self, surface):
        pass


class BottleScreen(Screen):
    SHIFT_AMOUNT = 600
    SHIFT_LENGTH = 16

    def __init__(self, bottle_container):
        super().__init__()
        self._bottles = []
        self._current_bottle_num = 0
        self._previous_bottle_num = 0

        self.bottle_container = bottle_container

        self._shift = curves.SineOut(0, self.SHIFT_AMOUNT, self.SHIFT_LENGTH)
        self._shift_direction = const.LEFT

        self.show_color_codes = False

    @property
    def bottles(self):
        return self._bottles

    @bottles.setter
    def bottles(self, value):
        self._bottles = value

    @property
    def current_bottle(self):
        return self.bottles[self.current_bottle_num]

    @property
    def current_bottle_num(self):
        return self._current_bottle_num

    @current_bottle_num.setter
    def current_bottle_num(self, value):
        """ current_bottle_num must be within the bounds of [0, index of last
        bottle in bottles list].  If the value trying to be set is outside the
        bounds, current_bottle_num is set to the closest bound instead.
        """
        self._previous_bottle_num = self._current_bottle_num

        if value < 0:
            self._current_bottle_num = 0
        elif value >= len(self.bottles):
            self._current_bottle_num = len(self.bottles) - 1
        else:
            self._current_bottle_num = value

    @property
    def previous_bottle(self):
        return self.bottles[self._previous_bottle_num]

    @property
    def previous_bottle_num(self):
        return self._previous_bottle_num

    def update(self):
        self._shift.update()

    def draw(self, surface):
        if len(self.bottles) > 0:
            self._draw_current_bottle(surface)

            if self._shift.active:
                self._draw_previous_bottle(surface)

    def _shift_to_next_bottle(self):
        if self.current_bottle_num < len(self.bottles) - 1:
            self._shift.restart()
            self._shift_direction = const.LEFT
            self.current_bottle_num += 1

    def _shift_to_previous_bottle(self):
        if self.current_bottle_num > 0:
            self._shift.restart()
            self._shift_direction = const.RIGHT
            self.current_bottle_num -= 1

    def _draw_current_bottle(self, surface):
        bottle = self.current_bottle
        base_x, base_y = geometry.centered(self.bottle_container, bottle.total_size)

        if self._shift.active:
            if self._shift_direction == const.LEFT:
                x = base_x - self._shift.current_value + self.SHIFT_AMOUNT
            else:
                x = base_x + self._shift.current_value - self.SHIFT_AMOUNT

            surface.blit(bottle.render(self.show_color_codes), (x, base_y))

        else:
            surface.blit(bottle.render(self.show_color_codes), (base_x, base_y))

    def _draw_previous_bottle(self, surface):
        bottle = self.previous_bottle
        base_x, base_y = geometry.centered(self.bottle_container, bottle.total_size)

        if self._shift.active:
            if self._shift_direction == const.LEFT:
                x = base_x - self._shift.current_value
            else:
                x = base_x + self._shift.current_value

            surface.blit(bottle.render(self.show_color_codes), (x, base_y))

        else:
            surface.blit(bottle.render(self.show_color_codes), (base_x, base_y))


class PlayScreen:
    """ Handles the main gameplay. """

    BOTTLE_SECTION_LEFT = 300
    BOTTLE_SECTION = (BOTTLE_SECTION_LEFT, 0,
                      screen.unscaled.get_width() - BOTTLE_SECTION_LEFT,
                      screen.unscaled.get_height())

    SHIFT_AMOUNT = 600
    SHIFT_LENGTH = 16

    HOMUNCULUS_EAT_DELAY_LENGTH = 5

    AMBULANCE_COUNTDOWN_POSITION = (40, 6)
    HOMUNCULUS_COUNTDOWN_POSITION = (40, 80)

    CONTROLS_POSITION = (328, 322)

    DEATH_CIRCLE_COUNT = 8

    # Length of delay is the sum of the first five frames of the eating animation
    JUDGEMENT_TIMER_LENGTH = sum(homunculus.frame_lengths[HOMUNCULUS_EAT][:5])

    def __init__(self):
        self.previous_time = 0

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

        self.countdown_color = colors.HOMUNCULUS_ORANGE
        self.countdown_flash_frame = 0
        self.one_more_frame = 0

        self.game_over = False
        self.win = False

        self.ambulance_anim_countdown = 0
        self.death_anim_countdown = 0

        self.death_anim_frame = 0
        self.death_circles = []

        self.in_ending_cutscene = False

        self.ambulance_entrance = curves.SineOut(1000, -250, 80)
        self.ambulance_exit = curves.SineOut(-250, -1000, 80)
        self.ambulance_x = 1000

        self.bottles = []
        self.allergies = []
        self.previous_brand = ""

        self.bottles_to_judge = []
        self.judgement_timers = []

        self.alternating = False
        self.has_eaten = False
        self.last_eaten_is_safe = False

        self.menu_level_num = 0

        self._feed_skip_locked = False

    def _next_bottle(self):
        """ Generates the next bottle.

        Does not start any animations.  Those must be started separately.
        """
        self.previous_bottle = self.current_bottle
        self.current_bottle = self.generator.next_item()
        self.bottles.append(self.current_bottle)

    def _feed_current_bottle(self):
        """ Feeds a bottle to the homunculus. """
        feed_release.play_random()

        self.bottles_to_judge.append(self.current_bottle)
        self.judgement_timers.append(self.JUDGEMENT_TIMER_LENGTH)
        self.current_bottle.eaten = True

        self._start_tossing_animation()
        self._next_bottle()

    def _skip_current_bottle(self):
        """ Skips a bottle, and doesn't feed it to the homunculus. """
        skip_release.play_random()
        self._start_shifting_animation()
        self._next_bottle()

    def _determine_minor_tick_interval(self):
        current = time_math.ms_time_to(self.death_time)

        if current > 30000:
            interval = 1000
        elif current > 15000:
            interval = 500
        elif current > 5000:
            interval = 250
        else:
            interval = 125

        return interval

    def _play_timer_sounds(self):
        """ Handles the playing of the timer ticks. """

        # Plays a major tick every time the timer crosses a second.
        previous = self.death_time - self.previous_time
        current = time_math.ms_time_to(self.death_time)
        if time_math.crosses_interval(previous, current, 1000):
            tick.play_random()

        # The amount of time between subticks depends on the time left.
        interval = self._determine_minor_tick_interval()
        if time_math.crosses_interval(previous, current, interval):
            subtick.play_random()

    def _update_win_cutscene(self):
        # Plays ambulance sounds
        if self.ambulance_entrance.frame == 1:
            ambulance_arrive.play_random()
        elif self.ambulance_exit.frame == 1:
            ambulance_pickup.play_random()

        # Speeds up the countdown if there is any time left
        if self.ambulance_anim_countdown > 0:
            self.ambulance_anim_countdown -= 400
            self.death_anim_countdown -= 400

            # Plays a tick every 4 frames
            if self.ambulance_anim_countdown % 1600 < 400:
                fast_tick.play_random()

            # If the countdown reaches the end
            if self.ambulance_anim_countdown <= 0:
                self.death_time = self.death_time - self.ambulance_anim_countdown
                self.ambulance_anim_countdown = 0

        # Animates the ambulance
        else:
            if self.ambulance_entrance.frame < self.ambulance_entrance.length - 1:
                self.ambulance_entrance.frame += 1
                self.ambulance_x = self.ambulance_entrance.current_value
            else:
                self.ambulance_exit.frame += 1

                if self.ambulance_exit.frame > self.ambulance_exit.length:
                    self.in_ending_cutscene = False
                else:
                    self.ambulance_x = self.ambulance_exit.current_value

    def _update_lose_cutscene(self):
        # Every 10 frames
        if self.death_anim_frame % 10 == 0:

            # Spawn a new circle, if there are not already too many
            if len(self.death_circles) < self.DEATH_CIRCLE_COUNT:
                self.death_circles.append(0)

            # Ends the cutscene when the last circle gets too big
            elif self.death_circles[-1] >= 1000:
                self.in_ending_cutscene = False

        # Increases the radius of all the circles
        for index in range(len(self.death_circles)):
            if self.death_circles[index] < 1000:
                self.death_circles[index] += 20

        self.death_anim_frame += 1

    def _win(self, last_bottle=None):
        if last_bottle:
            while self.bottles[-1] is not last_bottle:
                self.bottles.pop()

        self.in_ending_cutscene = True
        self._feed_skip_locked = True
        self.win = True
        self.ambulance_anim_countdown = time_math.ms_time_to(self.ambulance_time)
        self.death_anim_countdown = time_math.ms_time_to(self.death_time)

    def _lose(self, last_bottle=None):
        if last_bottle:
            while self.bottles[-1] is not last_bottle:
                self.bottles.pop()

        self.in_ending_cutscene = True
        self._feed_skip_locked = True
        self.game_over = True
        death.play_random()

    def _update_toss_animation(self):
        self.toss_x.frame += 1
        self.toss_y.frame += 1
        self.toss_scale.frame += 1
        self.toss_rotate.frame += 1

    def _update_shift_animation(self):
        self.shift.frame += 1

    def _apply_allergies(self, bottle):
        # Applies all allergies
        for allergy in bottle.allergies:
            if allergy not in self.allergies:
                self.allergies.append(allergy)
                bottle.adds_allergies.append(allergy)

    def _does_this_kill_me(self, bottle):

        # Typically, a safe bottle doesn't kill you and a deadly bottle does
        if not self.alternating:
            return not self.bottle_is_safe(bottle)

        # However, some levels have an "alternation" gimmick
        # First thing eaten when alternating is always safe
        if not self.has_eaten:
            return False

        # Kills you if this and the last bottle were both safe or both
        # deadly.  Otherwise, it doesn't.
        else:
            return self.bottle_is_safe(bottle) == self.last_eaten_is_safe

    def _countdown_flash(self, length, color):
        self.countdown_flash_frame = length
        self.countdown_color = color

    def _apply_bottle_eaten_reward(self):
        self.death_time += self.bottle_time  # Adds time

        # Makes countdown turn green for 30 frames
        self._countdown_flash(30, colors.TIME_ADDED_GREEN)

        correct.play_random()  # Plays time-gain sound

    def _reached_win_condition(self):
        return self.death_time > self.ambulance_time and not self.win

    def _time_ran_out(self):
        if self.in_ending_cutscene:
            return False

        return time_math.ms_time_to(self.death_time) < 0

    def update(self):

        if not self._feed_skip_locked:
            if events.keys.pressed_key == pygame.K_LEFT:
                feed_press.play_random()
            elif events.keys.pressed_key == pygame.K_RIGHT:
                skip_press.play_random()

            if events.keys.released_key == pygame.K_LEFT:
                self._feed_current_bottle()
            elif events.keys.released_key == pygame.K_RIGHT:
                self._skip_current_bottle()

        # Updates bottle tossing animation
        if self.is_tossing():
            self._update_toss_animation()
            self.homunculus_eat_delay += 1
            if self.homunculus_eat_delay == self.HOMUNCULUS_EAT_DELAY_LENGTH:
                homunculus.col_num = HOMUNCULUS_EAT

        # Verdict of whether the bottle eaten was lethal or not
        if not self.in_ending_cutscene:

            # Counts down timers
            for i in range(len(self.judgement_timers)):
                self.judgement_timers[i] -= 1

            # Judges the first bottle in the list once its timer runs out
            if self.judgement_timers and self.judgement_timers[0] <= 0:
                bottle = self.bottles_to_judge[0]
                self._apply_allergies(bottle)

                # Stores whether the bottle was deadly or not
                # Note: This detects whether the bottle is deadly, not
                # whether you survive eating it.  Level specifics can
                # make it so you survive a deadly bottle, for instance
                # in alternating levels where you must switch between
                # eating something not deadly and then deadly.
                bottle.judged_lethal = not self.bottle_is_safe(bottle)

                # Lose if you eat something that kills you
                if self._does_this_kill_me(bottle):
                    self._lose(bottle)

                # Consume the bottle if you eat something that doesn't kill you
                else:
                    self._apply_bottle_eaten_reward()
                    self.previous_brand = bottle.brand  # Updates brand

                    # If you won, this handles winning
                    if self._reached_win_condition():
                        self._win(bottle)

                # Updates some variables (mostly used for alternating stages)
                self.has_eaten = True
                self.last_eaten_is_safe = self.bottle_is_safe(bottle)

                # Removes the bottle from the judgement list
                del self.judgement_timers[0]
                del self.bottles_to_judge[0]

        # Plays the homunculus eating sound when it eats something
        if homunculus.frame == 4 and homunculus.delay == 0:
            eat.play_random()

        # Lose if time runs out
        if self._time_ran_out():
            self._lose()

        # If the countdown is flashing, count down until it stops flashing
        if self.countdown_flash_frame > 0:
            self.countdown_flash_frame -= 1

            # Turns the countdown back to orange
            if self.countdown_flash_frame == 0:
                self.countdown_color = colors.HOMUNCULUS_ORANGE

            # If you die, the countdown stops being colored.
            if self.game_over:
                self.countdown_flash_frame = 0

        # If currently in shifting animation
        if self.is_shifting():
            self._update_shift_animation()

        homunculus.update()
        if homunculus.col_num == HOMUNCULUS_EAT and homunculus.finished_once:
            homunculus.col_num = HOMUNCULUS_IDLE
            self.homunculus_eat_delay = 0

        # Handles the timer ticking sound
        if not self.in_ending_cutscene:
            self._play_timer_sounds()

        self.previous_time = pygame.time.get_ticks()

        # Updates end of game cutscenes
        if self.win:
            self._update_win_cutscene()
        elif self.game_over:
            self._update_lose_cutscene()

    def bottle_is_safe(self, bottle):
        # If it has any lethal side effects
        if bottle.has_deadly_effect:
            return False

        # If it triggers an allergy
        for allergen in bottle.allergens:
            if allergen in self.allergies:
                return False

        # If it has the same brand as the previous bottle
        if bottle.brand and bottle.brand == self.previous_brand:
            return False

        # If it is a bootleg
        if bottle.bootleg:
            return False

        # If the verification code is invalid
        if bottle.code:
            if not bottles.verification_code_is_valid(bottle.code):
                return False

        return True

    def is_tossing(self):
        if self.toss_x.frame <= self.toss_x.last_frame:
            return True
        return False

    def _start_tossing_animation(self):
        self.toss_x.frame = 0
        self.toss_y.frame = 0
        self.toss_scale.frame = 0
        self.toss_rotate.frame = 0
        self._start_shifting_animation()

    def is_shifting(self):
        if self.shift.frame <= self.shift.last_frame:
            return True
        return False

    def _start_shifting_animation(self):
        self.shift.frame = 0

    def _draw_bottles_shifting(self, surface):
        bottle1 = self.current_bottle
        x1, y1 = geometry.centered(self.BOTTLE_SECTION, bottle1.total_size)

        if not self.is_tossing():
            bottle2 = self.previous_bottle
            x2, y2 = geometry.centered(self.BOTTLE_SECTION, bottle2.total_size)
            x2 += int(self.shift.current_value) + self.SHIFT_AMOUNT
            surface.blit(self.render_bottle(bottle2), (x2, y2))

        x1 += int(self.shift.current_value)
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
        x2 += int(self.toss_x.current_value)
        y2 += int(self.toss_y.current_value)

        bottle_sprite = bottle.render()
        width = int(bottle_sprite.get_width() * self.toss_scale.current_value)
        height = int(bottle_sprite.get_height() * self.toss_scale.current_value)
        scaled = pygame.transform.scale(bottle_sprite, (width, height))

        angle = self.toss_rotate.current_value
        rotated = pygame.transform.rotate(scaled, angle)

        surface.blit(rotated, (x2, y2))

    def draw_countdowns(self, surface):
        # Ambulance countdown
        if self.win:
            time = time_math.ms_to_min_sec_ms(self.ambulance_anim_countdown)
        else:
            time = time_math.min_sec_ms_time_to(self.ambulance_time)
        position = self.AMBULANCE_COUNTDOWN_POSITION
        countdowns.draw_timer(surface, colors.AMBULANCE_RED, time, position)

        # Homunculus countdown
        milliseconds = time_math.ms_time_to(self.death_time)
        if self.win:
            shake = 0
        else:
            shake = max(0, (15000 - milliseconds) / 5000)

        if self.win:
            time = time_math.ms_to_min_sec_ms(self.death_anim_countdown)
        elif self.game_over:
            time = (0, 0, 0)
        else:
            time = time_math.min_sec_ms_time_to(self.death_time)
        position = self.HOMUNCULUS_COUNTDOWN_POSITION
        countdowns.draw_timer(surface, self.countdown_color, time, position, shake)

    def draw_controls(self, surface, position):

        # Feed text
        x = position[0] + 10
        y = position[1]
        if pygame.K_LEFT in events.keys.queue:
            x -= 10
        feed_text.draw(surface, (x, y))

        # Skip text
        x = position[0] + 153
        y = position[1] + 2
        if pygame.K_RIGHT in events.keys.queue:
            x += 10
        skip_text.draw(surface, (x, y))

    def draw_ui_text(self, surface):
        self.draw_countdowns(surface)

        # Homunculus and ambulance countdown labels
        ambulance_text.draw(surface, (5, 7))
        homunculus_text.draw(surface, (5, 88))

        self.draw_controls(surface, self.CONTROLS_POSITION)

    def draw_homunculus(self, surface):
        y = screen.unscaled.get_height() - homunculus_idle.single_height
        homunculus.draw(surface, (0, y))

    def draw(self, surface):
        background.draw(surface, (0, 0))

        # Bottles that are not tossed appear below UI
        self.draw_bottles(surface)

        ui.draw(surface, (0, 0))
        self.draw_ui_text(surface)

        # Bottles that are tossed appear above UI
        if self.is_tossing():
            self.draw_tossed_bottle(surface)

        if not self.win or self.ambulance_entrance.frame < self.ambulance_entrance.length - 1:
            self.draw_homunculus(surface)

        if self.win:
            ambulance.draw(surface, (self.ambulance_x, 162))

        if self.game_over:
            for circle_num, circle in enumerate(self.death_circles):
                if circle_num > len(self.death_circles) - 5:
                    color = (circle_num * -20 + self.DEATH_CIRCLE_COUNT * 20 - 20, ) * 3
                    pygame.draw.circle(surface, color, (117, 229), circle)

        # fps_text = graphics.tahoma.render(str(screen.clock.get_fps()), False, colors.WHITE, colors.BLACK)
        # surface.blit(fps_text, (10, 10))


class RaceScreen(PlayScreen):
    def __init__(self):
        super().__init__()
        self.starting_bottles = 10
        self._bottles_left = 0
        self._percentage_left = 0

        self.incorrect_penalty = 2
        self.start_time = 0

        self._showing_mistake = False

        original_position = super().AMBULANCE_COUNTDOWN_POSITION
        x = original_position[0] - 30
        y = original_position[1]
        self.AMBULANCE_COUNTDOWN_POSITION = (x, y)

        original_position = super().HOMUNCULUS_COUNTDOWN_POSITION
        x = original_position[0] - 30
        y = original_position[1]
        self.HOMUNCULUS_COUNTDOWN_POSITION = (x, y)

    @property
    def bottles_left(self):
        return self._bottles_left

    @bottles_left.setter
    def bottles_left(self, value):
        self._bottles_left = value
        self._percentage_left = value / self.starting_bottles

    @property
    def percentage_left(self):
        return self._percentage_left

    def update(self):
        super().update()

        if self._showing_mistake:
            if events.keys.released_key == pygame.K_SPACE:
                self._showing_mistake = False
                self._feed_skip_locked = False

    def _win(self, last_bottle=None):
        super()._win(last_bottle)
        self.ambulance_anim_countdown = 0
        self.death_anim_countdown = 0

    def _lose(self, last_bottle=None):
        self.bottles_left += self.incorrect_penalty
        self._countdown_flash(30, colors.AMBULANCE_RED)
        self._showing_mistake = True
        incorrect.play_random()

    def _time_ran_out(self):
        return False

    def _apply_bottle_eaten_reward(self):
        self.bottles_left -= 1
        self._countdown_flash(30, colors.TIME_ADDED_GREEN)
        correct.play_random()

    def _reached_win_condition(self):
        return self.bottles_left <= 0

    def _determine_minor_tick_interval(self):
        # Should always tick fastest if 1 bottle is left
        if self.bottles_left == 1:
            return 125

        if self.percentage_left > 0.5:
            interval = 1000
        elif self.percentage_left > 0.25:
            interval = 500
        elif self.percentage_left > 0.08:
            interval = 250
        else:
            interval = 125

        return interval

    def _feed_current_bottle(self):
        super()._feed_current_bottle()
        if self._does_this_kill_me(self.previous_bottle):
            self._feed_skip_locked = True

    def draw(self, surface):
        super().draw(surface)

        if self._showing_mistake:
            screen_rect = (0, 0, surface.get_width(), surface.get_height())
            pygame.gfxdraw.box(surface, screen_rect, (0, 0, 0, 100))

            bottle_sprite = self.previous_bottle.render(True)
            object_size = bottle_sprite.get_size()
            position = geometry.centered(screen_rect, object_size)

            surface.blit(bottle_sprite, position)

            # Continue text
            text = graphics.tahoma.render("Press SPACE to continue.", False, colors.BLACK)
            bottle_bottom = position[1] + bottle_sprite.get_height()
            container_height = surface.get_height() - bottle_bottom
            text_container = (0, bottle_bottom, surface.get_width(), container_height)
            text_position = geometry.centered(text_container, text.get_size())

            box_x = text_position[0] - 10
            box_y = text_position[1] - 10
            rect = (box_x, box_y, text.get_width() + 20, text.get_height() + 20)
            pygame.draw.rect(surface, colors.WHITE, rect)

            surface.blit(text, text_position)

    def draw_countdowns(self, surface):
        milliseconds = pygame.time.get_ticks() - self.start_time
        time = time_math.ms_to_min_sec_ms(milliseconds)
        position = self.AMBULANCE_COUNTDOWN_POSITION
        countdowns.draw_timer(surface, colors.AMBULANCE_RED, time, position)

        count = self.bottles_left
        exclamation = self.bottles_left == 1
        color = self.countdown_color
        shake = max(0, int((1 - self.percentage_left) * 3))
        text = countdowns.render_left_count(count, exclamation, color, shake)
        surface.blit(text, self.HOMUNCULUS_COUNTDOWN_POSITION)

    def draw_ui_text(self, surface):
        self.draw_countdowns(surface)
        self.draw_controls(surface, self.CONTROLS_POSITION)


class MenuScreen(PlayScreen):
    BOTTLE_ICON_SPACING = 12
    BOTTLE_ICON_SCALE = 10

    def __init__(self):
        super().__init__()
        self._incidents = incident_list
        self.bottles = [incident.bottle for incident in self._incidents]
        self.current_bottle = self.bottles[0]

        self._current_level = self._incidents[0]
        self._current_level_number = 0
        self._shift_direction = const.LEFT

        self._bottle_icon_row_scroll = 0

        self.selected = False
        self.quit = False

    def update(self):
        homunculus.update()

        if homunculus.col_num == HOMUNCULUS_EAT and homunculus.finished_once:
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
            if self.current_level_number < len(self._incidents) - 1:
                self.current_level_number += 1

        if events.keys.pressed_key == pygame.K_ESCAPE:
            self.quit = True

        if events.keys.pressed_key == pygame.K_SPACE:
            start_press.play_random()
        elif events.keys.pressed_key == pygame.K_LEFT:
            menu_press.play_random()
        elif events.keys.pressed_key == pygame.K_RIGHT:
            menu_press.play_random()

        self._scroll_to_bottle(self._current_level_number)

    def _scroll_to_bottle(self, bottle_num):
        target = self._center_of_bottle_icon_in_row(bottle_num)
        diff = target - self._bottle_icon_row_scroll
        if abs(diff) > 0.001:
            self._bottle_icon_row_scroll += diff / 5

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
        self._current_level = self._incidents[value]
        self.previous_bottle = self.current_bottle
        self.current_bottle = self._current_level.bottle
        self._start_shifting_animation()

    @property
    def current_level(self):
        return self._current_level

    def draw_ui_text(self, surface):
        self.draw_controls(surface, (334, 18))

    def draw_homunculus(self, surface):
        pass

    def _draw_bottles_shifting(self, surface):
        bottle1 = self.current_bottle
        x1, y1 = geometry.centered(self.BOTTLE_SECTION, bottle1.total_size)

        bottle2 = self.previous_bottle
        x2, y2 = geometry.centered(self.BOTTLE_SECTION, bottle2.total_size)

        if self._shift_direction == const.LEFT:
            x1 -= int(self.shift.current_value)
            x2 -= int(self.shift.current_value) + self.SHIFT_AMOUNT
        else:
            x1 += int(self.shift.current_value)
            x2 += int(self.shift.current_value) + self.SHIFT_AMOUNT

        surface.blit(self.render_bottle(bottle1), (x1, y1))
        surface.blit(self.render_bottle(bottle2), (x2, y2))

    def draw(self, surface):
        super().draw(surface)

        # Determines if a bottle should have a completion checkmark
        symbols = []
        for completed in progress_tracker.completed_levels:
            if completed:
                symbols.append(const.SYMBOL_CHECK)
            else:
                symbols.append(const.SYMBOL_NONE)

        # Draws the row of bottle icons
        position = (368, 13)
        selected_bottle = self._current_level_number
        self._draw_bottle_select(surface, position, selected_bottle, symbols)

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

    def draw_controls(self, surface, position):

        x = position[0] + 10
        y = position[1]
        if pygame.K_LEFT in events.keys.queue:
            x -= 6
        key_left.draw(surface, (x, y))

        x = position[0] + 243
        if pygame.K_RIGHT in events.keys.queue:
            x += 6
        key_right.draw(surface, (x, y))

    def _draw_bottle_select(self, surface, position, selected_bottle_num, symbols=None):

        # Draws the bottles
        offset = int(self._bottle_icon_row_scroll)
        bottle_icon_row = self.render_bottle_icon_row(200, offset - 100, symbols)
        x = position[0] + 2
        y = position[1] + 3
        surface.blit(bottle_icon_row, (x, y))

        # Draws the left cap
        surface.blit(row_cap_left.render(), position)

        # Draws the pointer
        x = position[0] + 98
        x += self._center_of_bottle_icon_in_row(selected_bottle_num) - offset

        bottle = self.bottles[selected_bottle_num]
        y = position[1] + 6
        y -= bottle.downscaled_total_height(self.BOTTLE_ICON_SCALE) // 2
        surface.blit(row_pointer.render(), (x, y))

        # Draws the right cap
        x = position[0] + 200
        y = position[1]
        surface.blit(row_cap_right.render(), (x, y))

    def render_bottle_icon_row(self, width, offset, symbols=None):
        if symbols:
            misc.force_length(symbols, len(self.bottles), const.SYMBOL_NONE)
        else:
            symbols = [const.SYMBOL_NONE] * len(self.bottles)

        scale = self.BOTTLE_ICON_SCALE

        height = self._max_bottle_icon_height() + 4
        surface = graphics.new_surface((width, height))

        x = -offset
        for bottle, symbol in zip(self.bottles, symbols):
            bottle_width = bottle.downscaled_total_width(scale)

            # Skips any bottle that isn't rendered due to the offset
            if x + bottle_width > 0:
                y = (height - bottle.downscaled_total_height(scale)) // 2
                sprite = bottle.render_downscaled_body(scale)
                surface.blit(sprite, (x, y))

                if symbol == const.SYMBOL_CHECK:
                    check_x = x + bottle_width - 8
                    check_y = y + bottle.downscaled_total_height(scale) - 10
                    checkmark.draw(surface, (check_x, check_y))

                elif symbol == const.SYMBOL_CROSS:
                    cross_x = x + bottle_width - 8
                    cross_y = y + bottle.downscaled_total_height(scale) - 10
                    cross.draw(surface, (cross_x, cross_y))

            x += bottle_width + self.BOTTLE_ICON_SPACING

            # Stops rendering bottles if the end of the surface is reached
            if x > width:
                break

        return surface

    def _center_of_bottle_icon_in_row(self, bottle_num):
        scale = self.BOTTLE_ICON_SCALE

        x = 0
        for i in range(bottle_num):
            x += self.bottles[i].downscaled_total_width(scale)
            x += self.BOTTLE_ICON_SPACING
        x += self.bottles[bottle_num].downscaled_total_width(scale) // 2
        return x

    def _max_bottle_icon_height(self):
        scale = self.BOTTLE_ICON_SCALE
        height = 0
        for bottle in self.bottles:
            bottle_height = bottle.downscaled_total_height(scale)
            height = max(height, bottle_height)

        return height


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

        self._scroll_to_bottle(self._bottle_num)

    def render_bottle(self, bottle):
        return bottle.render(text_color_codes=True)

    def draw(self, surface):
        if self.win:
            self.background.draw(surface, (0, 0))
        else:
            surface.fill(colors.BLACK)

        self.draw_bottles(surface)
        if self.win:
            ui.draw(surface, (0, 0))

        self.draw_controls(surface, (334, 18))

        # Draws the row of bottle icons
        symbols = []
        for bottle in self.bottles:
            if bottle.eaten and bottle.judged_lethal:
                symbols.append(const.SYMBOL_CROSS)
            elif bottle.eaten:
                symbols.append(const.SYMBOL_CHECK)
            else:
                symbols.append(const.SYMBOL_NONE)

        self._draw_bottle_select(surface, (368, 13), self._bottle_num, symbols)

        # Draws return to menu text
        text = graphics.tahoma.render("Press SPACE to return to level select.", False, colors.BLACK)
        text_x = (self.BOTTLE_SECTION_LEFT - text.get_width()) // 2

        rect = (text_x - 10, 250, text.get_width() + 20, text.get_height() + 20)
        pygame.draw.rect(surface, colors.WHITE, rect)

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
        pygame.draw.rect(surface, colors.WHITE, rect)

        surface.blit(text, (text_x, 320))

        # Draws win/lose text
        if self.win:
            sprite = win_text
            sprite.draw(surface, (48, 50))
        else:
            sprite = lose_text

            size = sprite.size
            x, y = geometry.centered(self.TEXT_SECTION, size)
            y -= 50
            sprite.draw(surface, (x, y))

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
        self._start_shifting_animation()


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

    play.alternating = menu.current_level.alternating
    play.menu_level_num = menu.current_level_number


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

    if play.win:
        result.win = True
        win_sound.play_random()

        progress_tracker.complete_level(play.menu_level_num)
        progress_tracker.save_progress()
    else:
        result.win = False
        lose_sound.play_random()


def menu_race_transition(menu, race):
    menu_play_transition(menu, race)
    race.starting_bottles = menu.current_level.racemode_starting_bottles
    race.bottles_left = race.starting_bottles
    race.incorrect_penalty = menu.current_level.racemode_incorrect_penalty
    race.start_time = pygame.time.get_ticks()


INCIDENTS_PATH = files.json_path("incidents")
INCIDENT_NAMES = [
    incidents.EFFECTS,
    incidents.ALLERGENS,
    incidents.EFFECTS_ALLERGENS,
    incidents.FAST,
    incidents.EFFECTS_HARD,
    incidents.EFFECTS_ALLERGENS_HARD,
    incidents.FASTER,
    incidents.EFFECTS_BRANDS,
    incidents.EFFECTS_ALLERGENS_BRANDS,
    incidents.EFFECTS_BOOTLEGS,
    incidents.EFFECTS_VERIFICATION,
    incidents.EFFECTS_ALTERNATION,
]
incident_list = incidents.load_incidents(INCIDENTS_PATH, INCIDENT_NAMES)

SAVE_FILE_PATH = files.json_path("save_file")
progress_tracker = save.ProgressTracker(len(incident_list), SAVE_FILE_PATH)
progress_tracker.load_progress()

MENU_SCREEN = 0
menu_screen = MenuScreen()

PLAY_SCREEN = 1
play_screen = PlayScreen()

RESULT_SCREEN = 2
result_screen = ResultScreen()
result_screen.background = background

RACE_SCREEN = 3
race_screen = RaceScreen()

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
            if pygame.K_r in events.keys.queue:
                current_screen = RACE_SCREEN
                menu_race_transition(menu_screen, race_screen)
            else:
                current_screen = PLAY_SCREEN
                menu_play_transition(menu_screen, play_screen)

    elif current_screen == PLAY_SCREEN:
        play_screen.update()

        if (play_screen.game_over or play_screen.win) and not play_screen.in_ending_cutscene:
            play_result_transition(play_screen, result_screen)

            play_screen.game_over = False
            play_screen.win = False
            current_screen = RESULT_SCREEN
            # Since play_screen is not drawn, skip a frame
            continue

        else:
            play_screen.draw(screen.unscaled)

    elif current_screen == RACE_SCREEN:
        race_screen.update()

        if (race_screen.game_over or race_screen.win) and not race_screen.in_ending_cutscene:
            play_result_transition(race_screen, result_screen)
            race_screen.game_over = False
            race_screen.win = False
            current_screen = RESULT_SCREEN
            # Since result_screen is not drawn, skip a frame
            continue

        else:
            race_screen.draw(screen.unscaled)

    elif current_screen == RESULT_SCREEN:
        result_screen.update()
        result_screen.draw(screen.unscaled)

        if result_screen.selected:
            result_screen.selected = False
            current_screen = MENU_SCREEN

            play_screen = PlayScreen()
            race_screen = RaceScreen()

    screen.scale_blit()
    screen.update(60)
    screen.clear(colors.WHITE)

pygame.quit()
