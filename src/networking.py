import socket, sys
import threading

hosting = False

options = [
    ("help", "h"),
    ("server", "s"),
    ]

def parse_args():
    global hosting
    if argument in ("--"+options[0][0], "-"+options[0][1]):
        print("--help, -h       print this message\n--server, -s     start game in server mode\n--client, -c     start game in client mode")
        sys.exit()
    elif argument in ("--"+options[1][0], "-"+options[1][1]):
        hosting = True
    else:
        raise Exception("%s is not a possible argument" % argument)

def handler():


if len(sys.argv) > 1:
    argument = sys.argv[1]
    parse_args()

server_thread = threading.Thread()

HOST = "127.0.0.1"
PORT = 1234

if hosting == True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("starting server...")
        s.bind((HOST, PORT))
        print("binding socket to host...")
        s.listen()
        print("listening on port...\n")
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                conn.sendall(b"message received")
                if data.decode("UTF-8") == "close":
                    print("closing...")
                    break
else:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        name = input("enter a username: ")
        while True:
            message = input("send a message: ")
            s.sendall(message.encode("UTF-8"))
            data = s.recv(1024)

            print(data.decode("UTF-8"))
