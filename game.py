import pygame, random, blocks, copy

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
GAME_WIDTH, GAME_HEIGHT     = 10, 20

BACKGROUND_COLOR = (20, 20, 20)
CELL_SIZE = 30

def main():
    pygame.init()

    grid = {}
    # create grid
    for x in range(GAME_WIDTH):
        for y in range(GAME_HEIGHT):
            grid[(x, y)] = BACKGROUND_COLOR

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
    clock = pygame.time.Clock()
    move_time, land_time, game_time, last_move = 0, 0, 0, 0
    gravity = 1 # spaces moved every second
    grid_x, grid_y = (WINDOW_WIDTH-(CELL_SIZE * GAME_WIDTH))/2, (WINDOW_HEIGHT-(CELL_SIZE * GAME_HEIGHT))/2

    def Lose():
        running = False
        pygame.quit()

    landed = False
    running = True
    current_block = copy.copy(random.choice(blocks.shapes))
    # game loop
    while running:
        # check if landed
        if current_block.borders(grid)[2] and landed == False:
            land_time = game_time
            move_time = game_time
            landed = True
        elif current_block.borders(grid)[2]:
            last_move = game_time
            if game_time >= land_time + 2000 or game_time >= move_time + 500:
                for cell in current_block.shapes[current_block.rotation]:
                    grid[cell[0] + current_block.x, cell[1] + current_block.y] = current_block.color
                current_block = copy.copy(random.choice(blocks.shapes))
                for cell in current_block.shapes[current_block.rotation]:
                    if cell[1] + current_block.y >= 0:
                        if grid[cell[0] + current_block.x, cell[1] + current_block.y] != BACKGROUND_COLOR:
                            Lose()
                landed = False
        elif landed == False:
            land_time = game_time

        screen.fill(BACKGROUND_COLOR)

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        current_block.rotate(grid)
        
        # move current block
        if game_time >= last_move + (1/gravity)*1000 and not current_block.borders(grid)[2]:
            current_block.y += 1
            last_move = game_time
        if pygame.key.get_pressed()[pygame.K_DOWN] and not current_block.borders(grid)[2] and not current_block.borders(grid)[2]:
            current_block.y += 1
        if pygame.key.get_pressed()[pygame.K_LEFT] and not current_block.borders(grid)[1]:
            current_block.x -= 1
            move_time = game_time
        if pygame.key.get_pressed()[pygame.K_RIGHT] and not current_block.borders(grid)[0]:
            current_block.x += 1
            move_time = game_time

        # break lines
        y = GAME_HEIGHT
        while y != 0:
            y-=1
            count=0
            for x in range(GAME_WIDTH):
                if grid[(x, y)] == BACKGROUND_COLOR:
                    break
                count+=1
            if count==GAME_WIDTH:
                for l in range(GAME_WIDTH):
                    grid[(l, y)] = BACKGROUND_COLOR
                    for i in range(y-1, 0, -1):
                        grid[(l, i+1)]=grid[(l,i)]
                gravity+=0.1
                y+=1

        # draw board
        for cell in grid.keys():
            # draw blocks
            pygame.draw.rect(screen, grid[cell], 
                pygame.Rect(grid_x + (cell[0] * CELL_SIZE), grid_y + (cell[1] * CELL_SIZE), 
                    CELL_SIZE, CELL_SIZE))
            # draw grid
            pygame.draw.rect(screen, (80, 80, 80), 
                pygame.Rect(grid_x + (cell[0] * CELL_SIZE), grid_y + (cell[1] * CELL_SIZE), 
                    CELL_SIZE, CELL_SIZE), width=2)
        # draw current block
        for cell in current_block.shapes[current_block.rotation]:
            if cell[1] + current_block.y >= 0:
                pygame.draw.rect(screen, current_block.color, pygame.Rect(grid_x + (cell[0] + current_block.x) * CELL_SIZE, grid_y + (cell[1] + current_block.y) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        pygame.display.update()
        clock.tick(15)
        game_time += clock.get_time()

if __name__ == "__main__":
    main()