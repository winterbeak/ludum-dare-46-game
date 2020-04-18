import pygame

import window
import geometry
import curves
import graphics
import const
import events
import bottles

# TODO: change to full screen
# screen = window.PixelWindow(int(window.monitor_size[0] / 320), (0, 0))
screen = window.PixelWindow(2, (1280, 720))
# screen is 640 by 360, scaled to 2x for 720p and 3x for 1080p

# pygame.display.set_caption("Read The Label")

test_background = graphics.SpriteColumn("images/test.png", 1)

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


def draw_debug_countdown(end_time, surface, position):
    # TODO: Beautify the timers with custom drawn numbers
    time = (end_time - pygame.time.get_ticks()) / 1000
    text = graphics.tahoma.render(str(time), False, const.WHITE)
    surface.blit(text, position)


class PlayScreen:

    BOTTLE_SECTION_LEFT = 300
    BOTTLE_SECTION = (BOTTLE_SECTION_LEFT, 0,
                      screen.unscaled.get_width() - BOTTLE_SECTION_LEFT,
                      screen.unscaled.get_height())

    SHIFT_AMOUNT = 500
    SHIFT_LENGTH = 15

    HOMUNCULUS_EAT_DELAY_LENGTH = 5

    def __init__(self):
        # TODO: Set death_time in the switch_to_play_screen function
        self.death_time = pygame.time.get_ticks() + 15000
        self.ambulance_time = pygame.time.get_ticks() + 120000

        self.generator = bottles.BottleGenerator()
        self.current_bottle = self.generator.next_item()
        self.previous_bottle = bottles.ghost_bottle

        self.shift = curves.SineOut(-self.SHIFT_AMOUNT, 0, self.SHIFT_LENGTH)
        self.toss_x = curves.Linear(0, -280, self.SHIFT_LENGTH)
        self.toss_y = curves.QuadraticArc(0, -100, self.SHIFT_LENGTH - 4)
        self.toss_scale = curves.Linear(1, 0.05, self.SHIFT_LENGTH)
        self.toss_rotate = curves.Linear(0, 290, self.SHIFT_LENGTH)
        self.toss_x.frame = self.toss_x.length
        self.toss_y.frame = self.toss_y.length
        self.toss_scale.frame = self.toss_scale.length
        self.toss_rotate.frame = self.toss_rotate.length

        self.homunculus_eat_delay = 0

        self.game_over = False

    def update(self):

        # If you press the key to feed
        if events.keys.released_key == pygame.K_LEFT:
            if self.current_bottle.lethal:
                pass #self.game_over = True
            else:
                self._start_tossing()
                self.death_time += 15000
                self.current_bottle = self.generator.next_item()

        # If you press the key to trash
        elif events.keys.released_key == pygame.K_RIGHT:
            self.previous_bottle = self.current_bottle
            self.current_bottle = self.generator.next_item()
            self._start_shifting()

        # If currently in tossing animation
        if self._is_tossing():
            self.toss_x.frame += 1
            self.toss_y.frame += 1
            self.toss_scale.frame += 1
            self.toss_rotate.frame += 1
            self.homunculus_eat_delay += 1
            if self.homunculus_eat_delay == self.HOMUNCULUS_EAT_DELAY_LENGTH:
                homunculus.col_num = HOMUNCULUS_EAT

        # If currently in shifting animation
        if self._is_shifting():
            self.shift.frame += 1

        homunculus.update()
        if homunculus.col_num == HOMUNCULUS_EAT and homunculus.done:
            homunculus.col_num = HOMUNCULUS_IDLE
            self.homunculus_eat_delay = 0

    def _is_tossing(self):
        if self.toss_x.frame <= self.toss_x.last_frame:
            return True
        return False

    def _start_tossing(self):
        self.toss_x.frame = 0
        self.toss_y.frame = 0
        self.toss_scale.frame = 0
        self.toss_rotate.frame = 0
        self._start_shifting()

    def _is_shifting(self):
        if self.shift.frame <= self.shift.last_frame:
            return True
        return False

    def _start_shifting(self):
        self.shift.frame = 0

    def draw_bottles(self, surface):

        bottle1 = self.current_bottle
        x1, y1 = geometry.centered(self.BOTTLE_SECTION, bottle1.total_size)

        if self._is_tossing():
            bottle2 = self.previous_bottle
            x2, y2 = geometry.centered(self.BOTTLE_SECTION, bottle2.total_size)
            x2 += self.toss_x.current_value
            y2 += self.toss_y.current_value

            bottle2_sprite = bottle2.render()
            width = int(bottle2_sprite.get_width() * self.toss_scale.current_value)
            height = int(bottle2_sprite.get_height() * self.toss_scale.current_value)
            scaled = pygame.transform.scale(bottle2_sprite, (width, height))

            angle = self.toss_rotate.current_value
            rotated = pygame.transform.rotate(scaled, angle)

            surface.blit(rotated, (x2, y2))

        if self._is_shifting():

            if not self._is_tossing():
                bottle2 = self.previous_bottle
                x2, y2 = geometry.centered(self.BOTTLE_SECTION, bottle2.total_size)
                x2 += self.shift.current_value + self.SHIFT_AMOUNT
                surface.blit(bottle2.render(), (x2, y2))

            x1 += self.shift.current_value
            surface.blit(bottle1.render(), (x1, y1))

        else:
            surface.blit(bottle1.render(), (x1, y1))

    def draw(self, surface):
        # test_background.draw(surface, (0, 0), 0)

        draw_debug_countdown(self.death_time, surface, (456, 30))
        # draw_debug_countdown(self.ambulance_time, surface, (20, 36))

        self.draw_bottles(surface)

        x = 425
        if events.keys.held_key == pygame.K_LEFT:
            x -= 5

        surface.blit(graphics.tahoma.render("PRESS LEFT TO FEED", False, const.WHITE), (x, 320))

        x = 425
        if events.keys.held_key == pygame.K_RIGHT:
            x -= 5

        surface.blit(graphics.tahoma.render("PRESS RIGHT TO PASS", False, const.WHITE), (x, 336))

        y = screen.unscaled.get_height() - homunculus_idle.single_height
        homunculus.draw(surface, (30, y))


PLAY_SCREEN = 1
play_screen = PlayScreen()

GAME_OVER_SCREEN = 2

current_screen = 1
running = True

while True:

    events.update()

    if events.quit_program:
        break

    if current_screen == PLAY_SCREEN:
        play_screen.update()
        play_screen.draw(screen.unscaled)

        if play_screen.game_over:
            current_screen = GAME_OVER_SCREEN

    elif current_screen == GAME_OVER_SCREEN:
        screen.unscaled.blit(graphics.tahoma.render("GAME OVER", False, const.WHITE), (50, 100))

    screen.scale_blit()
    screen.update(60)
    screen.clear()

pygame.quit()
