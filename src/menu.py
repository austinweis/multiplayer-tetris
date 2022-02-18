import pygame, ui, game
pygame.init()

screen = pygame.display.set_mode((game.WINDOW_WIDTH, game.WINDOW_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
start = ui.Button((500, 200), 'red', 'start')

running = True
while running:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
    screen.fill(game.BACKGROUND_COLOR)
    start.draw(screen, game.WINDOW_WIDTH/2, game.WINDOW_HEIGHT/2)
    pygame.display.update()