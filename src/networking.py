import socket, json, time

conn =       None
peer_grid =  {}
peer_block = []
peer_score = 0
connection_established = False

# start socket server, listen for data
def start_server(host, port):
    global conn, peer_grid, peer_block, peer_score, game_started, connection_established

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', port))
        s.listen()
        conn, addr = s.accept()
        connection_established = True
        with conn:
            incoming = ['', '']
            while True:
                data = incoming[1]
                while True:
                    incoming = conn.recv(1024).decode("utf8").split("E")
                    data += incoming[0]

                    if len(incoming) > 1:
                        break  
                data = json.loads(data)
                peer_block = data[1]
                peer_score = data[2]
                for key in data[0].keys():
                    new_key = key.split()
                    new_key = (int(new_key[0]), int(new_key[1]))
                    
                    new_val = data[0][key]
                    new_val = new_val.split()
                    new_val = (int(new_val[0]), int(new_val[1]), int(new_val[2]))

                    peer_grid[new_key] = new_val


# connect to server, listen for data
def connect_server(host, port):
    global conn, peer_grid, peer_block, peer_score, game_started, connection_established

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        while connection_established == False:
            try:
                s.connect((host, port))
                conn = s
                connection_established = True
            except:
                print("connection not made")
        with conn:
            incoming = ['', '']
            while True:
                data = incoming[1]
                while True:
                    incoming = conn.recv(1024).decode("utf8").split("E")
                    data += incoming[0]

                    if len(incoming) > 1:
                        break
                
                data = json.loads(data)
                peer_block = data[1]
                peer_score = data[2]
                for key in data[0].keys():
                    new_key = key.split()
                    new_key = (int(new_key[0]), int(new_key[1]))
                    
                    new_val = data[0][key]
                    new_val = new_val.split()
                    new_val = (int(new_val[0]), int(new_val[1]), int(new_val[2]))

                    peer_grid[new_key] = new_val

def get_network_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    ip = s.getsockname()[-2]
    s.close()
    return ip
def init_connection(address, port, hosting):
    if hosting:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((address, int(port)-1))
            s.listen()
            conn, addr = s.accept()
            with conn:
                conn.send('ready'.encode("utf8"))     
                conn.close()
                s.close()
        return True
    else:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((address, int(port)-1))
                data = s.recv(1024).decode("utf8")
                if not data == 'ready':
                    raise Exception("Data not returned properly")
                s.close()
                return True
            except:
                return False

def send_data(tuple):
    dictionary = tuple[0]
    formatted_dict = {}
    for key in dictionary.keys():
        formatted_dict[' '.join(map(str, key))] = ' '.join(map(str, dictionary[key]))

    block = tuple[1]
    score = tuple[2]

    data = (formatted_dict, block, score)
    formatted_data = json.dumps(data).encode("utf8")

    conn.sendall(formatted_data)
    conn.send('E'.encode("utf8"))