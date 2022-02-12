import pygame
from Models.bullet import Bullet

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2


def handle_events(yellow_ship, red_ship):
    for event in pygame.event.get():  # (See pygame.event for diff event types)
        if event.type == pygame.QUIT:
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL and len(yellow_ship.bullets) < yellow_ship.max_bullets:
                bullet = Bullet(yellow_ship)
                yellow_ship.bullets.append(bullet.rect)
                Bullet.SOUNDS['BULLET_FIRE_SOUND'].play()

            if event.key == pygame.K_RCTRL and len(red_ship.bullets) < red_ship.max_bullets:
                bullet = Bullet(red_ship)
                red_ship.bullets.append(bullet.rect)
                Bullet.SOUNDS['BULLET_FIRE_SOUND'].play()

        if event.type == RED_HIT:
            red_ship.health -= 1
            Bullet.SOUNDS['BULLET_HIT_SOUND'].play()

        if event.type == YELLOW_HIT:
            yellow_ship.health -= 1
            Bullet.SOUNDS['BULLET_HIT_SOUND'].play()
