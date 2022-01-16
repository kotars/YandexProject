import os
import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((288, 512))


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 450))
    screen.blit(floor_surface, (floor_x_pos + 288, 450))


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_bird_rect


gravity = 0.25
bird_movement = 0

bg_surface = load_image('background.png')

floor_surface = load_image('base.png')
floor_x_pos = 0

bird_downflap = load_image('bluebird-downflap.png')
bird_midflap = load_image('bluebird-midflap.png')
bird_upflap = load_image('bluebird-upflap.png')
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(50, 256))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

clock = pygame.time.Clock()
running = True

while running:
    # обработчик событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 8
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))
    bird_movement += gravity
    rotated_bird = rotate_bird(bird_surface)
    bird_rect.centery += bird_movement
    screen.blit(rotated_bird, bird_rect)

    floor_x_pos -= 5
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
pygame.quit()
