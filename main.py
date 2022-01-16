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


bg_surface = load_image('background.png')

floor_surface = load_image('base.png')
floor_x_pos = 0

clock = pygame.time.Clock()
running = True

while running:
    # обработчик событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(bg_surface, (0, 0))

    floor_x_pos -= 5
    draw_floor()
    if floor_x_pos <= -288:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
pygame.quit()
