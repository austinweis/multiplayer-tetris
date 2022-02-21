import pygame, gui, game, networking
from collections import namedtuple
pygame.init()

screen = pygame.display.set_mode((game.WINDOW_WIDTH, game.WINDOW_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
Scene = namedtuple('Scene', ['name', 'gui'])

clock = pygame.time.Clock()
runtime = 0
error_timer = 1000
error = False

# general elements
error1 = gui.Label((640, 250), 'red', 'game not found')
error1.toggle()

# main scene elements
server = gui.Button((500, 200), (640, 500),'blue', 'host game')
client = gui.Button((500, 200), (640, 200),'green', 'connect to game')
main_scene   = Scene('Main Scene', (server, client))

# client scene elements
connect = gui.Button((500, 100), (640, 600), 'green', 'connect')
address_label = gui.Label((640, 100), 'white', 'ip address:')
server_ip = gui.InputBox((500, 50), (640, 200),'white')
port_label = gui.Label((640, 300), 'white', 'port number:')
server_port = gui.InputBox(((500, 50)), (640, 400), 'white')
client_scene = Scene('Client Scene', (connect, server_ip, server_port, address_label, port_label))

# server scene elements
server_scene = Scene('Server Scene', ())

current_scene = None

def switch_scene(new_scene):
    gui.hide_all(screen)
    for element in new_scene.gui:
        element.toggle()
    scene = new_scene

switch_scene(main_scene)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        event_result = gui.call(event)
        if event_result == client:
            switch_scene(client_scene)
        if event_result == connect and error == False:
            #test_result = networking.test_connection(server_ip.text, server_port.text)
            #if test_result == False:
            #    error = True
            #    error1.toggle()
            #else:
            game.main(server_ip.text, server_port.text)
            running = False

    screen.fill(game.BACKGROUND_COLOR)
    gui.draw(screen)
    pygame.display.update()
    clock.tick(60)
    runtime += clock.get_time()

    if error:
        error_timer-=clock.get_time()
        if error_timer <= 0:
            error = False
            error_timer = 1000
            error1.toggle()