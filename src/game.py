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
    def Shadow():
        shadow = blocks.Block(current_block.shapes, (80, 80, 80))
        shadow.x, shadow.y = current_block.x, current_block.y
        shadow.rotation = current_block.rotation
        for i in range(GAME_HEIGHT):
            if shadow.borders(grid)[2]:
                break
            shadow.y += 1
        return shadow

    next_block = copy.copy(random.choice(blocks.shapes))
    current_block = copy.copy(random.choice(blocks.shapes))

    landed = False
    running = True
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
                current_block = next_block
                for cell in current_block.shapes[current_block.rotation]:
                    if cell[1] + current_block.y >= 0:
                        if grid[cell[0] + current_block.x, cell[1] + current_block.y] != BACKGROUND_COLOR:
                            Lose()
                next_block = copy.copy(random.choice(blocks.shapes))
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
                    if event.key == pygame.K_SPACE:
                        current_block.x, current_block.y = block_shadow.x, block_shadow.y
                        landed=True
                        move_time = game_time - 500
                        land_time = game_time - 2000
        
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

        block_shadow = Shadow()
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
        #draw block shadow
        for cell in block_shadow.shapes[block_shadow.rotation]:
            pygame.draw.rect(screen, (80, 80, 80), pygame.Rect(grid_x + (cell[0] + block_shadow.x) * CELL_SIZE, grid_y + (cell[1] + block_shadow.y) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # draw current block
        for cell in current_block.shapes[current_block.rotation]:
            if cell[1] + current_block.y >= 0:
                pygame.draw.rect(screen, current_block.color, pygame.Rect(grid_x + (cell[0] + current_block.x) * CELL_SIZE, grid_y + (cell[1] + current_block.y) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # draw next block
        for cell in next_block.shapes[next_block.rotation]:
            pygame.draw.rect(screen, next_block.color, pygame.Rect(1000 + cell[0] * CELL_SIZE, 200 + cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.update()
        clock.tick(15)
        game_time += clock.get_time()

if __name__ == "__main__":
    main()