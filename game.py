import pygame
import sys
from game_functions import handle_events, draw_tetromino, update_tetromino, generate_tetromino, draw_locked_tetrominoes, draw_grid

pygame.init()

WHITE = (255,255,255)
RED = (255, 0, 0)

# screen stuff
screen = pygame.display.set_mode((500, 1000))
pygame.display.set_caption("Tetris")

# clock stuff
clock = pygame.time.Clock()
time_since_gravity = pygame.time.get_ticks()
time_since_directional_input = pygame.time.get_ticks() 
last_move_time = {'key': None, 'time': pygame.time.get_ticks()}

# gamestate stuff
tetromino = generate_tetromino()
locked_tetrominoes = []

running = True
while running:
    running = handle_events()

    current_time = pygame.time.get_ticks()

    tetromino, time_since_gravity, time_since_directional_input, last_move_time, locked_tetrominoes = update_tetromino(tetromino, current_time, time_since_gravity, time_since_directional_input, last_move_time, locked_tetrominoes)

    screen.fill(WHITE)
    draw_grid(screen)

    s = pygame.Surface((1000,750), pygame.SRCALPHA)   # per-pixel alpha
    s.fill((255,255,255,128))                         # notice the alpha value in the color
    screen.blit(s, (0,0))

    draw_tetromino(screen, tetromino)
    draw_locked_tetrominoes(screen, locked_tetrominoes)

    pygame.display.flip()

    clock.tick(244)

pygame.quit()
sys.exit()