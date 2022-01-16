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


gravity = 0.25
bird_movement = 0

bg_surface = load_image('background.png')

floor_surface = load_image('base.png')
floor_x_pos = 0

bird_surface = load_image('bluebird-midflap.png')
bird_rect = bird_surface.get_rect(center=(50, 256))

clock = pygame.time.Clock()
running = True

while running:
    # обработчик событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(bg_surface, (0, 0))
    bird_movement += gravity
    bird_rect.centery += bird_movement
    screen.blit(bird_surface, bird_rect)

    floor_x_pos -= 5
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
pygame.quit()
