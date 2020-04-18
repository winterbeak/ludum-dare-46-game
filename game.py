import pygame

import window
import const
import events
import food

# TODO: change to full screen
# screen = window.PixelWindow(int(window.monitor_size[0] / 320), (0, 0))
screen = window.PixelWindow(2, (1280, 720))
# screen is 640 by 360, scaled to 2x for 720p and 3x for 1080p

tahoma = pygame.font.SysFont("Tahoma", 10)


def text_block(text, font, color, max_width):
    """ Renders a block of text, and automatically wraps it to a width. """
    line = ""
    lines = []

    first_word = True
    current_width = 0

    # Determines where to split the lines up
    for word in text.split():
        width = font.size(word + " ")[0]

        if current_width + width > max_width and not first_word:
            lines.append(line)
            line = word + " "

            current_width = width

        else:
            line += word + " "

            current_width += width

        first_word = False

    lines.append(line)

    # Makes the final rendered surface that all the text is rendered on
    line_height = font.get_linesize()
    height = len(lines) * line_height

    surface = pygame.Surface((max_width, height))
    surface.set_colorkey(const.TRANSPARENT)
    surface.fill(const.TRANSPARENT)

    # Renders all the lines
    y = 0
    for text_line in lines:
        rendered_text = font.render(text_line, False, color)
        surface.blit(rendered_text, (0, y))
        y += line_height

    return surface


def draw_debug_countdown(end_time, surface, position):
    # TODO: Beautify the timers with custom drawn numbers
    time = (end_time - pygame.time.get_ticks()) / 1000
    text = tahoma.render(str(time), False, const.WHITE)
    surface.blit(text, position)


class PlayScreen:

    def __init__(self):
        # TODO: Set death_time in the switch_to_play_screen function
        self.death_time = pygame.time.get_ticks() + 15000
        self.ambulance_time = pygame.time.get_ticks() + 120000

        self.generator = food.FoodGenerator()
        self.current_food = self.generator.next_item()

        self.game_over = False

    def update(self):

        # If you press the key to feed
        if events.keys.released_key == pygame.K_LEFT:
            if self.current_food.lethal:
                self.game_over = True
            else:
                self.death_time += 15000
                self.current_food = self.generator.next_item()

        # If you press the key to trash
        elif events.keys.released_key == pygame.K_RIGHT:
            self.current_food = self.generator.next_item()

    def draw_food(self, surface):
        text = ", ".join(self.current_food.effects)
        side_effects = text_block(text, tahoma, const.WHITE, 200)

        surface.blit(side_effects, (100, 20))

    def draw(self, surface):
        draw_debug_countdown(self.death_time, surface, (20, 20))
        #draw_debug_countdown(self.ambulance_time, surface, (20, 36))

        self.draw_food(surface)

        if events.keys.held_key == pygame.K_LEFT:
            x = 120
        else:
            x = 125
        surface.blit(tahoma.render("PRESS LEFT TO FEED", False, const.WHITE), (x, 100))

        if events.keys.held_key == pygame.K_RIGHT:
            x = 120
        else:
            x = 125
        surface.blit(tahoma.render("PRESS RIGHT TO PASS", False, const.WHITE), (x, 116))


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
        screen.unscaled.blit(tahoma.render("GAME OVER", False, const.WHITE), (50, 100))

    screen.scale_blit()
    screen.update(60)
    screen.clear()

pygame.quit()
