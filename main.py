import pygame

from Models.spaceship import Spaceship
from Models.display import Display
from Events.events import handle_events

pygame.font.init()  # initialize fonts functionality
pygame.display.set_caption("Window Title")


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
            break  # breaks out of the nearest containing loop

        keys_pressed = pygame.key.get_pressed()

        p1_ship.handle_movement(keys_pressed, window.border)
        p2_ship.handle_movement(keys_pressed, window.border)

        p1_ship.handle_bullets(p2_ship)
        p2_ship.handle_bullets(p1_ship)


        window.draw_window(p2_ship.rect, p1_ship.rect, p2_ship.bullets, p1_ship.bullets,
                           p2_ship.health, p1_ship.health, p1_ship.image, p2_ship.image)
        # draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    # pygame.quit()
    main()


if __name__ == '__main__':
    main()
