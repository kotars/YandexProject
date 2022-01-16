import os
import sys
import pygame
from pygame import mixer
import random

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


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    new_pipe = pipe_surface.get_rect(midtop=(300, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(300, random_pipe_pos - 175))
    return new_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 512:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_s = mixer.Sound('sound/sfx_hit.wav')
            hit_s.set_volume(0.01)
            hit_s.play()
            return 2
        if bird_rect.top <= -50 or bird_rect.bottom >= 450:
            hit_s = mixer.Sound('sound/sfx_hit.wav')
            hit_s.set_volume(0.01)
            hit_s.play()
            return 2
    return 1


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(50, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Time: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(144, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Time: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(144, 425))
        screen.blit(high_score_surface, high_score_rect)


def update_score(scor, high_scor):
    if high_scor < scor:
        high_scor = scor
    if time_ == '':
        time = open('high_time.txt', 'w')
        time.seek(0)
        time.write(str(int(high_scor)))
        time.close()
    elif int(time_) > high_scor:
        high_scor = int(time_)
    elif int(time_) < high_scor:
        time = open('high_time.txt', 'w')
        time.seek(0)
        time.write(high_scor)
        time.close()
    return high_scor


gravity = 0.25
bird_movement = 0
game_active = 0
score = 0
high_score = 0

time = open('high_time.txt', 'r')
time_ = time.read()
time.close()

game_font = pygame.font.Font('04B_19.TTF', 20)

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

pipe_surface = load_image('pipe-green.png')
pipe_list = []
pipe_list_between = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [200, 250, 300, 350, 400]

game_over_img = load_image('gameover.png')
menu_img = load_image('message.png')

mixer.music.load('sound/Vint.wav')
mixer.music.set_volume(0.025)  # 0.025 было
mixer.music.play(-1)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                wings_s = mixer.Sound('sound/sfx_wing.wav')
                wings_s.set_volume(0.025)
                wings_s.play()
                bird_movement = 0
                bird_movement -= 8
            if event.key == pygame.K_SPACE and game_active == 0 or game_active == 2:
                game_active = 1
                pipe_list.clear()
                bird_rect.center = (50, 256)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))
    if game_active == 0:
        screen.blit(menu_img, (0, 0))
    elif game_active == 1:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        score += 0.01
        game_active = check_collision(pipe_list)
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score_display('main_game')
    elif game_active == 2:
        screen.blit(game_over_img, (50, 200))
        high_score = update_score(score, high_score)
        score_display('game_over')

    floor_x_pos -= 5
    draw_floor()

    if floor_x_pos <= -288:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
pygame.quit()
