import pygame
import random

screen_width = 500
screen_height = 1000

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

TETROMINO_SHAPES = {
    'I': [ [0, 0], [0, 1], [0, 2], [0, 3] ],
    'O': [ [0, 0], [1, 0], [0, 1], [1, 1] ],
    'T': [ [0, 0], [1, 0], [2, 0], [1, 1] ],
    'L': [ [0, 0], [0, 1], [0, 2], [1, 2] ],
    'J': [ [0, 0], [0, 1], [0, 2], [-1, 2] ],
    'S': [ [0, 0], [1, 0], [1, 1], [2, 1] ],
    'Z': [ [0, 1], [1, 1], [1, 0], [2, 0] ],
}

TETROMINO_COLORS = {
    'I': (0, 255, 255),
    'O': (255, 255, 0),
    'T': (128, 0, 128),
    'L': (255, 165, 0),
    'J': (0, 0, 255),
    'S': (0, 255, 0),
    'Z': (255, 0, 0),
}

def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            return False
    return True

def generate_tetromino():
    shape_name = random.choice(list(TETROMINO_SHAPES.keys()))
    shape = TETROMINO_SHAPES[shape_name]
    color = TETROMINO_COLORS[shape_name]
    return {'shape': shape, 'color': color, 'x': 200, 'y': 0}

def draw_tetromino(screen, tetromino):
    for block in tetromino['shape']:
        pygame.draw.rect(screen, tetromino['color'], (tetromino['x'] + block[0] * 50, tetromino['y'] + block[1] * 50, 50, 50))
        pygame.draw.rect(screen, (0, 0, 0), (tetromino['x'] + block[0] * 50, tetromino['y'] + block[1] * 50, 50, 50), 2)

        semi_transparent_color = (tetromino['color'][0], tetromino['color'][1], tetromino['color'][2], 128)
        temp_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        temp_surface.fill(semi_transparent_color)
        
        screen.blit(temp_surface, (tetromino['x'] + block[0] * 50, tetromino['y'] + block[1] * 50))

def draw_locked_tetrominoes(screen, tetrominoes):
    for tetromino in tetrominoes:
        for block in tetromino['shape']:
            pygame.draw.rect(screen, tetromino['color'], (tetromino['x'] + block[0] * 50, tetromino['y'] + block[1] * 50, 50, 50))
            pygame.draw.rect(screen, (0, 0, 0), (tetromino['x'] + block[0] * 50, tetromino['y'] + block[1] * 50, 50, 50), 2)

def draw_grid(screen):
    blockSize = 50 #Set the size of the grid block
    for x in range(0, screen_width, blockSize):
        for y in range(0, screen_height, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, BLACK, rect, 1)

def check_collision(tetromino, locked_tetrominoes):
    for block in tetromino['shape']:
        block_x = tetromino['x'] + block[0] * 50
        block_y = tetromino['y'] + block[1] * 50
        for locked in locked_tetrominoes:
            for locked_block in locked['shape']:
                locked_x = locked['x'] + locked_block[0] * 50
                locked_y = locked['y'] + locked_block[1] * 50
                if block_x == locked_x and block_y == locked_y:
                    return True
    return False

def lock_tetromino(tetromino, locked_tetrominoes):
    locked_tetrominoes.append(tetromino)
    return locked_tetrominoes

def check_oob(tetromino):
    min_block = min(tetromino['shape'], key=lambda block: block[0])
    max_block = max(tetromino['shape'], key=lambda block: block[0])
    if min_block[0] * 50 + tetromino['x'] < 0 or (max_block[0] + 1) * 50 + tetromino['x'] > screen_width:
        return True
    
def check_oob_y(tetromino):
    max_block = max(tetromino['shape'], key=lambda block: block[1])
    if (max_block[1] + 1) * 50 + tetromino['y'] > screen_height:
        return True
    return False

def update_tetromino(tetromino, current_time, time_since_gravity, time_since_directional_input, last_move_time, locked_tetrominoes):
    if current_time - time_since_gravity >= 1000:
        time_since_gravity = current_time
        tetromino['y'] += 50

        if check_collision(tetromino, locked_tetrominoes) or check_oob_y(tetromino):
            tetromino['y'] -= 50
            locked_tetrominoes = lock_tetromino(tetromino, locked_tetrominoes)
            locked_tetrominoes = clear_lines(locked_tetrominoes)
            tetromino = generate_tetromino()
            return tetromino, time_since_gravity, time_since_directional_input, last_move_time, locked_tetrominoes

    
    keys = pygame.key.get_pressed()
    das = 150
    arr = 50
    sarr = 30

    if keys[pygame.K_a]:
        if last_move_time['key'] != 'left':
            last_move_time['key'] = 'left'
            last_move_time['time'] = current_time
            time_since_directional_input = current_time
            tetromino['x'] -= 50
            if check_collision(tetromino, locked_tetrominoes) or check_oob(tetromino):
                tetromino['x'] += 50
        elif current_time - last_move_time['time'] >= das:
            if current_time - time_since_directional_input >= arr:
                time_since_directional_input = current_time
                tetromino['x'] -= 50
                if check_collision(tetromino, locked_tetrominoes) or check_oob(tetromino):
                    tetromino['x'] += 50
    elif keys[pygame.K_d]:
        if last_move_time['key'] != 'right':
            last_move_time['key'] = 'right'
            last_move_time['time'] = current_time
            time_since_directional_input = current_time
            tetromino['x'] += 50
            if check_collision(tetromino, locked_tetrominoes) or check_oob(tetromino):
                tetromino['x'] -= 50
        elif current_time - last_move_time['time'] >= das:
            if current_time - time_since_directional_input >= arr:
                time_since_directional_input = current_time
                tetromino['x'] += 50
            if check_collision(tetromino, locked_tetrominoes) or check_oob(tetromino):
                tetromino['x'] -= 50
    if keys[pygame.K_s]:
        if last_move_time['key'] != 'down':
            if current_time - last_move_time['time'] >= das:
                last_move_time['key'] = 'down'
                last_move_time['time'] = current_time
                time_since_directional_input = current_time
                tetromino['y'] += 50

                if check_collision(tetromino, locked_tetrominoes) or check_oob_y(tetromino):
                    tetromino['y'] -= 50
                    locked_tetrominoes = lock_tetromino(tetromino, locked_tetrominoes)
                    locked_tetrominoes = clear_lines(locked_tetrominoes)
                    tetromino = generate_tetromino()
                    return tetromino, time_since_gravity, time_since_directional_input, last_move_time, locked_tetrominoes
        elif current_time - last_move_time['time'] >= das:
            if current_time - time_since_directional_input >= sarr:
                time_since_directional_input = current_time
                tetromino['y'] += 50

                if check_collision(tetromino, locked_tetrominoes) or check_oob_y(tetromino):
                    tetromino['y'] -= 50
                    locked_tetrominoes = lock_tetromino(tetromino, locked_tetrominoes)
                    locked_tetrominoes = clear_lines(locked_tetrominoes)
                    tetromino = generate_tetromino()
                    return tetromino, time_since_gravity, time_since_directional_input, last_move_time, locked_tetrominoes
    
    if not (keys[pygame.K_s] or keys[pygame.K_d] or keys[pygame.K_a]):
        last_move_time['key'] = None

    if keys[pygame.K_SPACE]:
        for i in range(20):
            tetromino['y'] += 50
            
            if check_collision(tetromino, locked_tetrominoes) or check_oob_y(tetromino):
                    tetromino['y'] -= 50
                    locked_tetrominoes = lock_tetromino(tetromino, locked_tetrominoes)
                    locked_tetrominoes = clear_lines(locked_tetrominoes)
                    tetromino = generate_tetromino()
                    return tetromino, time_since_gravity, time_since_directional_input, last_move_time, locked_tetrominoes
    
   
    return tetromino, time_since_gravity, time_since_directional_input, last_move_time, locked_tetrominoes

def clear_lines(locked_tetrominoes):

    full_lines = []

    for y in range(20):
        full = True
        for x in range(10):
            block_found = False
            for tetromino in locked_tetrominoes:
                for block in tetromino['shape']:
                    block_x = tetromino['x'] + block[0] * 50
                    block_y = tetromino['y'] + block[1] * 50
                    if block_y == y * 50 and block_x // 50 == x:
                        block_found = True
                        break
                if block_found:
                    break
            if not block_found:
                full = False
                break
        if full:
            full_lines.append(y)

    if not full_lines:
        return locked_tetrominoes
    

    new_locked_tetrominoes = []
    
    for tetromino in locked_tetrominoes:
        new_shape = []
        for block in tetromino['shape']:
            block_y = block[1] * 50 + tetromino['y']
            if block_y // 50 not in full_lines:
                new_shape.append(block)
        tetromino['shape'] = new_shape

        for i in range(len(full_lines)):
            if tetromino['y'] < full_lines[i] * 50:
                tetromino['y'] += 50
            

    return locked_tetrominoes
