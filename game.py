import pygame

import window
import geometry
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

    def __init__(self):
        # TODO: Set death_time in the switch_to_play_screen function
        self.death_time = pygame.time.get_ticks() + 15000
        self.ambulance_time = pygame.time.get_ticks() + 120000

        self.generator = bottles.BottleGenerator()
        self.current_bottle = self.generator.next_item()

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
            self.current_bottle = self.generator.next_item()

    def draw_bottle(self, surface):
        bottle = self.current_bottle

        position = geometry.centered(self.BOTTLE_SECTION, bottle.total_size)
        surface.blit(bottle.render(), position)

    def draw(self, surface):
        test_background.draw(surface, (0, 0), 0)

        draw_debug_countdown(self.death_time, surface, (20, 20))
        # draw_debug_countdown(self.ambulance_time, surface, (20, 36))

        self.draw_bottle(surface)

        if events.keys.held_key == pygame.K_LEFT:
            x = 120
        else:
            x = 125
        surface.blit(graphics.tahoma.render("PRESS LEFT TO FEED", False, const.WHITE), (x, 100))

        if events.keys.held_key == pygame.K_RIGHT:
            x = 120
        else:
            x = 125
        surface.blit(graphics.tahoma.render("PRESS RIGHT TO PASS", False, const.WHITE), (x, 116))


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
