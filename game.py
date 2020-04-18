import pygame
import window
import const

# TODO: change to full screen
# screen = window.PixelWindow(int(window.monitor_size[0] / 320), (0, 0))
screen = window.PixelWindow(4, (1280, 720))

font = pygame.font.SysFont("Tahoma", 8)

class PlayScreen:

    def __init__(self):
        # TODO: Set death_time in the switch_to_play_screen function
        self.death_time = pygame.time.get_ticks() + 15000
        self.ambulance_time = pygame.time.get_ticks() + 120000

    def update(self):
        pass

    def draw_timer(self, end_time, surface, position):
        # TODO: Beautify the timers with custom drawn numbers
        time = (end_time - pygame.time.get_ticks()) / 1000
        text = font.render(str(time), False, const.WHITE)
        surface.blit(text, position)

    def draw(self, surface):
        self.draw_timer(self.death_time, surface, (0, 0))
        self.draw_timer(self.ambulance_time, surface, (0, 16))


PLAY_SCREEN = 1
play_screen = PlayScreen()

current_screen = 1

for frame in range(300):

    if current_screen == PLAY_SCREEN:
        play_screen.update()
        play_screen.draw(screen.unscaled)

    screen.scale_blit()
    screen.update(60)
    screen.clear()