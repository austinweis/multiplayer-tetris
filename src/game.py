import pygame, random
from grid import *
from tetromino import *    

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.SCALED)
clock = pygame.time.Clock()

# game constants
GRID_CELLS_X = 14
GRID_CELLS_Y = 28
GRID_CELL_SIZE = 25
GRID_OFF_X = screen.get_width() / 2 - GRID_CELLS_X * GRID_CELL_SIZE / 2
GRID_OFF_Y = screen.get_height() / 2 - GRID_CELLS_Y * GRID_CELL_SIZE / 2

MAX_SPEED = 100

PROTOTYPES = [
    Tetromino(I_SHAPES, 'cyan'),
    Tetromino(O_SHAPES, 'yellow')
]

# game functions
def check_overlap(block, grid):
    for row in range(len(block.get_shape()), 0, -1):
        y = row - 1 + block.y
        if y < 0:
            continue
        if y > grid.cells_y + 1:
            return True

        if sum(block.get_shape()[row - 1]) == 0:
            continue
        
        grid_row = grid.cells[y][block.left() : block.right()+1]
        if all(x is None for x in grid_row) == False:
            return True
        
    return False

def render_tetromino(block):
    # get offsets based on block position and grid properties
    off_x = block.x * GRID_CELL_SIZE + GRID_OFF_X
    off_y = block.y * GRID_CELL_SIZE + GRID_OFF_Y

    # the tetromino cells
    shape = block.get_shape()

    # draw the cells
    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if (shape[row][col]):
                x = off_x + col * GRID_CELL_SIZE
                y = off_y + row * GRID_CELL_SIZE

                if ((GRID_OFF_X + GRID_CELLS_X * GRID_CELL_SIZE > x >= GRID_OFF_X) and (GRID_OFF_Y + GRID_CELLS_Y * GRID_CELL_SIZE > y >= GRID_OFF_Y)):
                    pygame.draw.rect(screen, block.color, pygame.Rect(x, y, GRID_CELL_SIZE, GRID_CELL_SIZE))

def render_grid(grid):
    # render grid blocks
    for y in range(grid.cells_y):
        for x in range(grid.cells_x):
            color = grid.get_cell(x, y)
            if color:
                pygame.draw.rect(screen, color, pygame.Rect(x * GRID_CELL_SIZE + GRID_OFF_X, y * GRID_CELL_SIZE + GRID_OFF_Y, GRID_CELL_SIZE, GRID_CELL_SIZE))

    # render grid lines
    for i in range(grid.cells_x + 1):
        pygame.draw.line(screen, 'gray', pygame.math.Vector2(GRID_OFF_X + GRID_CELL_SIZE * i, GRID_OFF_Y), pygame.math.Vector2(GRID_OFF_X + GRID_CELL_SIZE * i, GRID_OFF_Y + GRID_CELL_SIZE * GRID_CELLS_Y))
    for i in range(grid.cells_y + 1):
        pygame.draw.line(screen, 'gray', pygame.math.Vector2(GRID_OFF_X, GRID_OFF_Y + GRID_CELL_SIZE * i), pygame.math.Vector2(GRID_OFF_X + GRID_CELLS_X * GRID_CELL_SIZE, GRID_OFF_Y + GRID_CELL_SIZE * i))

def new_tetromino():
    return PROTOTYPES[random.randint(0, len(PROTOTYPES) - 1)].create(GRID_CELLS_X // 2, -1)

# runtime vars
grid = Grid(GRID_CELLS_X, GRID_CELLS_Y)

running = True
last_update = 0
game_speed = 1


# create first tetromino
active_block = new_tetromino()

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # rotate
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                active_block.rotate()
                while active_block.left() < 0:
                    active_block.move(1, 0)
                while active_block.right() > grid.cells_x - 1:
                    active_block.move(-1, 0)
            # drop
            if event.key == pygame.K_SPACE:
                while not (active_block.bottom() == grid.cells_y or check_overlap(active_block, grid)):
                    active_block.y += 1
            # speed fall rate
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                game_speed = MAX_SPEED
                last_update = 0
        if event.type == pygame.KEYUP:
            # speed fall rate
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                game_speed = 1
                last_update = pygame.time.get_ticks() + 1000 / game_speed
    # move active tetromino left and right
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        active_block.move(-1, 0)
        if active_block.left() < 0 or check_overlap(active_block, grid): # check if move is valid
            active_block.move(1, 0)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        active_block.move(1, 0)
        if active_block.right() > grid.cells_x - 1 or check_overlap(active_block, grid):
            active_block.move(-1, 0)

    # update
    if (last_update + 1000 / game_speed <= pygame.time.get_ticks()):
        last_update = pygame.time.get_ticks() + 1000 / game_speed
        active_block.move(0, 1)

    if (active_block.bottom() == grid.cells_y) or check_overlap(active_block, grid):
        active_block.move(0, -1)
        shape = active_block.get_shape()
        for row in range(len(shape)):
            for col in range(len(shape[0])):
                if (shape[row][col]):
                    grid.set_cell(active_block.x + col, active_block.y + row, active_block.color)
        row = grid.cells_y
        while row != 0:
            row -= 1
            count = 0
            for col in range(grid.cells_x):
                if (grid.cells[row][col]):
                    count += 1
            if count == grid.cells_x:
                grid.cells[row] = [None for x in range(grid.cells_x)]
                grid.cells.insert(0, grid.cells.pop(row))
                row += 1

        active_block = new_tetromino()

    # render
    screen.fill('black')
    render_tetromino(active_block)
    render_grid(grid)

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(30)  # limits FPS to 30

pygame.quit()