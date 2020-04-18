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

    def __init__(self):
        # TODO: Set death_time in the switch_to_play_screen function
        self.death_time = pygame.time.get_ticks() + 15000
        self.ambulance_time = pygame.time.get_ticks() + 120000

        self.generator = bottles.BottleGenerator()
        self.current_bottle = self.generator.next_item()
        self.previous_bottle = bottles.ghost_bottle

        self.shift = curves.SineOut(-self.SHIFT_AMOUNT, 0, 10)

        self.game_over = False

    def update(self):

        # If you press the key to feed
        if events.keys.released_key == pygame.K_LEFT:
            if self.current_bottle.lethal:
                self.game_over = True
            else:
                self.death_time += 15000
                self.current_bottle = self.generator.next_item()

        # If you press the key to trash
        elif events.keys.released_key == pygame.K_RIGHT:
            self.previous_bottle = self.current_bottle
            self.current_bottle = self.generator.next_item()
            self._start_shifting()

        # If currently in the shift animation
        if self._is_shifting():
            self.shift.frame += 1

    def _is_shifting(self):
        if self.shift.frame <= self.shift.last_frame:
            return True
        return False

    def _start_shifting(self):
        self.shift.frame = 0

    def draw_bottles(self, surface):

        bottle1 = self.current_bottle
        x1, y1 = geometry.centered(self.BOTTLE_SECTION, bottle1.total_size)

        if self._is_shifting():
            bottle2 = self.previous_bottle
            x2, y2 = geometry.centered(self.BOTTLE_SECTION, bottle2.total_size)
            x1 += self.shift.current_value
            x2 += self.shift.current_value + self.SHIFT_AMOUNT
            surface.blit(bottle1.render(), (x1, y1))
            surface.blit(bottle2.render(), (x2, y2))
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
