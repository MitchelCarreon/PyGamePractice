import pygame
import os

from Utils.constants import *


class Display:
    HEALTH_FONT = 'health_font'
    WINNER_FONT = 'winner_font'

    def __init__(self, fps=60):
        self._window = pygame.display.set_mode((WIDTH, HEIGHT))
        self._border = pygame.Rect((WIDTH // 2) - 5, 0, 10, HEIGHT)

        self._background = None
        self.__init_background()

        self._fps = fps

        self._fonts = {}
        self.init_fonts()

    @property
    def border(self):
        return self._border

    @property
    def fps(self):
        return self._fps

    def init_fonts(self, font_info=None):
        """
        :param font_info: Keys = health_font_style, health_font_size, winner_font_style, winner_font_size
        :return: None
        """
        if font_info:
            self._fonts[Display.HEALTH_FONT] = pygame.font.SysFont(
                font_info['health_font_style'],
                font_info['health_font_size']
            )

            self._fonts[Display.WINNER_FONT] = pygame.font.SysFont(
                font_info['winner_font_style'],
                font_info['winner_font_size']
            )
        else:
            self._fonts[Display.HEALTH_FONT] = pygame.font.SysFont('comicsans', 40)
            self._fonts[Display.WINNER_FONT] = pygame.font.SysFont('comicsans', 100)

    def __init_background(self):
        self.choose_background()

    def choose_background(self, file_name='space.png'):
        self._background = pygame.transform.scale(
            pygame.image.load(os.path.join('Assets', file_name)), (WIDTH, HEIGHT))

    @property
    def window(self):
        return self._window

    def draw_window(self, p1_ship, p2_ship):
        self._window.blit(self._background, (0, 0))

        red_health_text = self._fonts[Display.HEALTH_FONT].render(f'Health {p2_ship.health}', 1, WHITE)
        yellow_health_text = self._fonts[Display.HEALTH_FONT].render(f'Health {p1_ship.health}', 1, WHITE)

        self._window.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
        self._window.blit(yellow_health_text, (10, 10))

        # NOTE: Union[Surface, SurfaceType] == Surface
        pygame.draw.rect(self._window, BLACK, self._border)

        self._window.blit(p1_ship.image,
                          (p1_ship.rect.x, p1_ship.rect.y))
        self._window.blit(p2_ship.image, (p2_ship.rect.x, p2_ship.rect.y))

        for bullet in p2_ship.bullets:
            pygame.draw.rect(self._window, RED, bullet)

        for bullet in p1_ship.bullets:
            pygame.draw.rect(self._window, YELLOW, bullet)

        pygame.display.update()

    def draw_winner(self, text):
        draw_text = self._fonts[Display.WINNER_FONT].render(text, 1, WHITE)
        self._window.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))

        pygame.display.update()
        pygame.time.delay(5000)
