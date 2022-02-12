import pygame

from Models.spaceship import Spaceship
from Models.display import Display
from Events.events import handle_events

pygame.font.init()  # initialize fonts functionality
pygame.display.set_caption("Window Title")


def handle_ship_and_bullet_movement(p1_ship, p2_ship, window):
    keys_pressed = pygame.key.get_pressed()
    p1_ship.handle_movement(keys_pressed, window.border)
    p2_ship.handle_movement(keys_pressed, window.border)

    p1_ship.handle_bullets(p2_ship)
    p2_ship.handle_bullets(p1_ship)


def main():
    p1_ship = Spaceship()
    p2_ship = Spaceship(p1=False)
    window = Display()

    clock = pygame.time.Clock()  # for FPS
    run = True
    while run:
        clock.tick(window.fps)  # constraint to FPS

        handle_events(p1_ship, p2_ship)

        winner_text = ""
        if p2_ship.health <= 0:
            winner_text = "Yellow wins!"

        if p1_ship.health <= 0:
            winner_text = "Red wins!"

        if winner_text != "":
            window.draw_winner(winner_text)
            break

        handle_ship_and_bullet_movement(p1_ship, p2_ship, window)
        window.draw_window(p1_ship, p2_ship)

    main()


if __name__ == '__main__':
    main()
