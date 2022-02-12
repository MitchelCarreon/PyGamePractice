import pygame
import os

from Models.bullet import Bullet
from Utils.constants import WIDTH, HEIGHT
from Events.events import RED_HIT, YELLOW_HIT


# red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
# yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

class Spaceship:
    """
    p1 : If true, handles loading and rotation of Surface for yellow spaceship (Left).
    Pass false to instantiate red spaceship
    """
    INITIAL_YPOS = 300
    INITIAL_XPOS_P1 = 100
    INITIAL_XPOS_P2 = 700
    INITIAL_HEALTH = 10

    def __init__(self, velocity=5, max_bullets=3, width=55, height=40, p1=True):
        self.__velocity = velocity
        self.__max_bullets = max_bullets
        self.__width = width
        self.__height = height

        self.__is_p1 = p1
        """ Determines if yellow or red """

        self.__image = self.__init_surface()
        """ A Surface object from pygame  """

        self.__controls = None
        """ dict """

        self._rect = None
        """ pygame rect """

        self.__init_rect()

        self._bullets = []
        self._health = Spaceship.INITIAL_HEALTH

    @property
    def image(self):
        return self.__image

    @image.setter
    def image(self, value):
        self.__image = value

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def is_p1(self):
        return self.__is_p1

    @property
    def bullets(self):
        return self._bullets

    @bullets.setter
    def bullets(self, value):
        self._bullets = value

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value):
        self._rect = value

    @property
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, val):
        self.__velocity = val

    @property
    def max_bullets(self):
        return self.__max_bullets

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def __init_surface(self):

        if self.__is_p1:
            spaceship_image = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
        else:
            spaceship_image = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))

        rotation_angle = 90 if self.__is_p1 else 270
        return pygame.transform.rotate(
            pygame.transform.scale(spaceship_image, (self.width, self.height)), rotation_angle
        )

    def __init_rect(self):
        self.__x_pos = Spaceship.INITIAL_XPOS_P1 if self.__is_p1 else Spaceship.INITIAL_XPOS_P2
        self.__y_pos = Spaceship.INITIAL_YPOS
        self._rect = pygame.Rect(self.__x_pos, self.__y_pos, self.__width, self.__height)

    def handle_movement(self, keys_pressed, mid_border):
        curr_velocity = self.velocity

        if not self.__controls:
            self.__controls = {
                'Up': pygame.K_w if self.__is_p1 else pygame.K_UP,
                'Down': pygame.K_s if self.__is_p1 else pygame.K_DOWN,
                'Left': pygame.K_a if self.__is_p1 else pygame.K_LEFT,
                'Right': pygame.K_d if self.__is_p1 else pygame.K_RIGHT,
            }

        if keys_pressed[self.__controls['Up']] and self._rect.y - curr_velocity > 0:
            self._rect.y -= curr_velocity
        if keys_pressed[
            self.__controls['Down']] and self._rect.y + curr_velocity + self._rect.height < HEIGHT - 15:
            self._rect.y += curr_velocity

        if self.__is_p1:
            if keys_pressed[self.__controls['Left']] and self._rect.x - curr_velocity > 0:
                self._rect.x -= curr_velocity
            if keys_pressed[
                self.__controls['Right']] and self._rect.x + curr_velocity + self._rect.width < mid_border.x:
                self._rect.x += curr_velocity

        else:
            if keys_pressed[self.__controls['Left']] and self._rect.x - curr_velocity > mid_border.x + mid_border.width:
                self._rect.x -= curr_velocity
            if keys_pressed[
                self.__controls['Right']] and self._rect.x + curr_velocity + self._rect.width < WIDTH:
                self._rect.x += curr_velocity

    def handle_bullets(self, enemy_ship):
        if self.__is_p1:
            for bullet in self._bullets:
                bullet.x += Bullet.VELOCITY_INC
                if enemy_ship.rect.colliderect(bullet):  # only works if both objects are Rect
                    pygame.event.post(pygame.event.Event(RED_HIT))  # add to queue of events (i.e., pygame.event.get())
                    self._bullets.remove(bullet)
                elif bullet.x > WIDTH:
                    self._bullets.remove(bullet)

        else:
            for bullet in self._bullets:
                bullet.x -= Bullet.VELOCITY_INC
                if enemy_ship.rect.colliderect(bullet):  # only works if both objects are Rect
                    pygame.event.post(pygame.event.Event(YELLOW_HIT))
                    self._bullets.remove(bullet)
                elif bullet.x < 0:
                    self._bullets.remove(bullet)
