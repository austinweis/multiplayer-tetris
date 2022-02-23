#!/usr/bin/python3
import pygame, sys, threading
from src import game,gui,networking
from collections import namedtuple

def switch_scene(new_scene):
    global previous_scene, current_scene
    gui.hide_all(screen)
    for element in new_scene.gui:
        element.toggle()
    previous_scene = current_scene
    current_scene = new_scene

def main():
    global screen, current_scene, previous_scene

    pygame.init()
    screen = pygame.display.set_mode((game.WINDOW_WIDTH, game.WINDOW_HEIGHT), pygame.RESIZABLE | pygame.SCALED)
    Scene = namedtuple('Scene', ['name', 'gui'])

    clock = pygame.time.Clock()
    runtime = 0

    error_timer = 1500
    error = False

    # general elements
    error1 = gui.Label((640, 250), 'red', 'game not found')
    error1.toggle()

    connecting = gui.Label((640, 250), 'yellow', 'connecting...')
    wait_connect = gui.Label((640, 250), 'yellow', 'waiting for connection...')

    back = gui.Button((100, 50), (80, 50), 'red', '<--')

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
    client_scene = Scene('Client Scene', (connect, server_ip, server_port, address_label, port_label, back))

    # server scene elements
    start = gui.Button((500, 100), (640, 600), 'green', 'start')
    ip_label = gui.Label((640, 200), 'white', 'ip address: '+ networking.get_network_ip())
    server_scene = Scene('Server Scene', (start, ip_label, port_label, server_port, back))

    network_thread = threading.Thread()

    current_scene = None
    previous_scene = None



    switch_scene(main_scene)

    running = True
    while running:
        if networking.peer_found:
            if current_scene == server_scene:
                gui.hide_all(screen)
                network_thread.join()
                running = False
                game.main('localhost', server_port.text)
                pygame.quit()
            if current_scene == client_scene:
                gui.hide_all(screen)
                running = False
                game.main(server_ip.text, server_port.text)
                pygame.quit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            event_result = gui.call(event)
            if event_result == client:
                switch_scene(client_scene)
            if event_result == server:
                switch_scene(server_scene)
            if event_result == connect and error == False:
                connecting.toggle()
                network_thread = threading.Thread(target=networking.init_connection, args=(server_ip.text, server_port.text, False))
                network_thread.start()
                network_thread.join()
                if networking.peer_found == False:
                    connecting.toggle()
                    error = True
                    error1.toggle()
            if event_result == start:
                wait_connect.toggle()
                network_thread = threading.Thread(target=networking.init_connection, args=('', server_port.text, True))
                network_thread.start()
            if event_result == back and not network_thread.is_alive():
                switch_scene(previous_scene)
                    
        screen.fill(game.BACKGROUND_COLOR)
        gui.draw(screen)
        pygame.display.update()
        clock.tick(15)
        runtime += clock.get_time()

        if error:
            error_timer-=60.24
            if error_timer <= 0:
                error = False
                error_timer = 1000
                error1.toggle()

if __name__ == "__main__":
    main()