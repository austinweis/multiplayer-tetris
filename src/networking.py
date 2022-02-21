import socket, json

conn =       None
peer_grid =  {}
peer_block = []
peer_score = 0

# start socket server, listen for data
def start_server(host, port):
    global conn, peer_grid, peer_block, peer_score

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
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
    global conn, peer_grid, peer_block, peer_score

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        conn = s
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

def test_connection(address, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((address, port))
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