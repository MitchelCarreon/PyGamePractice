import pygame
import os

pygame.mixer.init()  # init sounds functionality


class Bullet:
    VELOCITY_INC = 7
    SOUNDS = {
        'BULLET_HIT_SOUND': pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3')),
        'BULLET_FIRE_SOUND': pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
    }

    def __init__(self, spaceship, velocity=7):
        self.__velocity = velocity

        self.spaceship = spaceship
        """ referece to owning Spaceship """

        self.__rect = None
        self.__init_rect()

    @property
    def rect(self):
        return self.__rect

    @property
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, value):
        self.__velocity = value

    def __init_rect(self):
        if self.spaceship.is_p1:
            self.__rect = pygame.Rect(self.spaceship.rect.x + self.spaceship.width,
                                      self.spaceship.rect.y + self.spaceship.height // 2 - 2, 10, 5)
        else:
            self.__rect = pygame.Rect(self.spaceship.rect.x, self.spaceship.rect.y + self.spaceship.height // 2 - 2, 10,
                                      5)
