import pygame
from tetromino import *    

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.SCALED)
clock = pygame.time.Clock()

# game constants
GRID_OFF_X = 0
GRID_OFF_Y = 0
GRID_CELLS_X = 10
GRID_CELLS_Y = 20
GRID_CELL_SIZE = 20

# functions
def render_tetromino(instance):
    # get offsets based on block position and grid properties
    off_x = instance.x * GRID_CELL_SIZE + GRID_OFF_X
    off_y = instance.y * GRID_CELL_SIZE + GRID_OFF_Y

    # the tetromino cells
    shape = instance.get_shape()

    # draw the cells
    for row in range(len(shape)):
        for col in range(len(shape[0])):
            if (shape[row][col]):
                x = off_x + col * GRID_CELL_SIZE
                y = off_y + row * GRID_CELL_SIZE

                pygame.draw.rect(screen, instance.color, pygame.Rect(x, y, GRID_CELL_SIZE, GRID_CELL_SIZE))

def render_grid():
    for i in range(GRID_CELLS_X):
        pygame.draw.line(screen, 'gray', pygame.math.Vector2(GRID_OFF_X + GRID_CELL_SIZE * i, GRID_OFF_Y), pygame.math.Vector2(GRID_OFF_X + GRID_CELL_SIZE * i, GRID_OFF_Y + GRID_CELL_SIZE * GRID_CELLS_Y))

# runtime vars
running = True
last_update = 0
game_speed = 1

prototypes = {
    'I': Tetromino(I_SHAPES, 'cyan'),
    'O': Tetromino(O_SHAPES, 'yellow')
}

# create first tetromino
active_block = prototypes['I'].create(GRID_CELLS_X // 2, -2)

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
            # speed fall rate
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                # speed gravity
                pass
    # move active tetromino left and right
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        active_block.move(-1, 0)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        active_block.move(1, 0)

    # update
    if (last_update + 1000 / game_speed <= pygame.time.get_ticks()):
        last_update = pygame.time.get_ticks() + 1000 / game_speed
        active_block.move(0, 1)

    # render
    screen.fill('black')
    render_tetromino(active_block)
    render_grid()

    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(30)  # limits FPS to 30

pygame.quit()