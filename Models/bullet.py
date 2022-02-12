import pygame
import os

pygame.mixer.init()  # init sounds functionality



class Bullet:
    """
    keeps a reference to its owning spaceship
    """
    VELOCITY = 7
    SOUNDS = {
        'BULLET_HIT_SOUND': pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3')),
        'BULLET_FIRE_SOUND': pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
    }

    def __init__(self, spaceship, velocity=7):
        self.__velocity = velocity

        self.spaceship = spaceship

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
            self.__rect = pygame.Rect(self.spaceship.rect.x, self.spaceship.rect.y + self.spaceship.height // 2 - 2, 10, 5)


# pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)

# def handle_bullets(yellow_bullets, red_bullets, yellow, red):
#     for bullet in yellow_bullets:
#         bullet.x += BULLET_VELOCITY
#         if red.colliderect(bullet):  # only works if both objects are Rect
#             pygame.event.post(pygame.event.Event(RED_HIT))  # add to queue of events (i.e., pygame.event.get())
#             yellow_bullets.remove(bullet)
#         elif bullet.x > WIDTH:
#             yellow_bullets.remove(bullet)
#
#     for bullet in red_bullets:
#         bullet.x -= BULLET_VELOCITY
#         if yellow.colliderect(bullet):  # only works if both objects are Rect
#             pygame.event.post(pygame.event.Event(YELLOW_HIT))
#             red_bullets.remove(bullet)
#         elif bullet.x < 0:
#             red_bullets.remove(bullet)
#
#         if bullet.x > WIDTH:
#             yellow_bullets.remove(bullet)
