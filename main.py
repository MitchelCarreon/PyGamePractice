import pygame
import os

import pygame.font


pygame.font.init()  # fonts
pygame.mixer.init()  # for sounds


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT,))
pygame.display.set_caption("Window Caption")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

MID_BORDER = pygame.Rect((WIDTH // 2) - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

# FONTS
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60

VELOCITY = 5
BULLET_VELOCITY = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH = 55
SPACESHIP_HEIGHT = 40

YELLOW_HIT = pygame.USEREVENT + 1  # new event types
RED_HIT = pygame.USEREVENT + 2

# NOTE: Union[Surface, SurfaceType] == Surface (as per docs)
# load image
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))

# resize image and rotate
YELLOW_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270
)

# scale image background
SPACE_BG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


# TODO: Move rendering to separate package
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # try deleting this and see what happens. images drawn in the Surface are still there! 1:15:13 --> https://www.youtube.com/watch?v=jO6qQDNa2UY
    WIN.blit(SPACE_BG, (0, 0))  # WIN.fill(WHITE)

    red_health_text = HEALTH_FONT.render(f'Health {red_health}', 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(f'Health {yellow_health}', 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    # NOTE: Union[Surface, SurfaceType] == Surface
    pygame.draw.rect(WIN, BLACK, MID_BORDER)  # draw border

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))  # WIN.blit(YELLOW_SPACESHIP, (300, 100)) draw spaceship
    WIN.blit(RED_SPACESHIP, (red.x, red.y))  # WIN.blit(RED_SPACESHIP, (600, 100))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))

    pygame.display.update()  # Pauses the game for 5000 ms automatically after win.
    pygame.time.delay(5000)


def handle_yellow_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VELOCITY > 0:  # left (See pygame docs : pygame.key)
        yellow.x -= VELOCITY
    if keys_pressed[pygame.K_d] and yellow.x + VELOCITY + yellow.width < MID_BORDER.x:
        yellow.x += VELOCITY
    if keys_pressed[pygame.K_w] and yellow.y - VELOCITY > 0:
        yellow.y -= VELOCITY
    if keys_pressed[pygame.K_s] and yellow.y + VELOCITY + yellow.height < HEIGHT - 15:
        yellow.y += VELOCITY


def handle_red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VELOCITY > MID_BORDER.x + MID_BORDER.width:
        red.x -= VELOCITY
    if keys_pressed[pygame.K_RIGHT] and red.x + VELOCITY < WIDTH - 40:
        red.x += VELOCITY
    if keys_pressed[pygame.K_UP] and red.y - VELOCITY > 0:
        red.y -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and red.y + VELOCITY + red.height < HEIGHT - 15:
        red.y += VELOCITY


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):  # only works if both objects are Rect
            pygame.event.post(pygame.event.Event(RED_HIT))  # add to queue of events (i.e., pygame.event.get())
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):  # only works if both objects are Rect
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

        if bullet.x > WIDTH:
            yellow_bullets.remove(bullet)


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = yellow_health = 10

    clock = pygame.time.Clock()  # for FPS
    run = True
    while run:
        clock.tick(FPS)  # constraint to FPS
        for event in pygame.event.get():  # (See pygame.event for diff event types)
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "Yellow wins!"

        if yellow_health <= 0:
            winner_text = "Red wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break  # breaks out of the nearest containing loop

        keys_pressed = pygame.key.get_pressed()
        handle_yellow_movement(keys_pressed, yellow=yellow)
        handle_red_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    # pygame.quit()
    main()


if __name__ == '__main__':
    main()
