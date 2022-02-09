import socket, json

conn =       None
peer_grid =  {}
peer_block = []

# start socket server, listen for data
def start_server(host, port):
    global conn
    global peer_grid
    global peer_block
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                data = b''
                while True:
                    incoming = conn.recv(1024)
                    data += incoming
                    if 'END' == incoming.decode("utf8")[-3:]:
                        break
                data = data.decode("utf8")
                data = data[:-3]

                data = json.loads(data)
                peer_block = data[1]
                for key in data[0].keys():
                    new_key = key.split()
                    new_key = (int(new_key[0]), int(new_key[1]))
                    
                    new_val = data[0][key]
                    new_val = new_val.split()
                    new_val = (int(new_val[0]), int(new_val[1]), int(new_val[2]))

                    peer_grid[new_key] = new_val


# connect to server, listen for data
def connect_server(host, port):
    global conn
    global peer_grid
    global peer_block
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        conn = s
        while True:
            data = b''
            while True:
                incoming = conn.recv(1024)
                data += incoming
                if 'END' == incoming.decode("utf8")[-3:]:
                    break
            data = data.decode("utf8")
            data = data[:-3]

            data = json.loads(data)
            peer_block = data[1]
            for key in data[0].keys():
                new_key = key.split()
                new_key = (int(new_key[0]), int(new_key[1]))
                
                new_val = data[0][key]
                new_val = new_val.split()
                new_val = (int(new_val[0]), int(new_val[1]), int(new_val[2]))

                peer_grid[new_key] = new_val

def send_data(tuple):
    dictionary = tuple[0]
    formatted_dict = {}
    for key in dictionary.keys():
        formatted_dict[' '.join(map(str, key))] = ' '.join(map(str, dictionary[key]))

    block = tuple[1]

    data = (formatted_dict, block)
    formatted_data = json.dumps(data).encode("utf8")

    conn.sendall(formatted_data)
    conn.send('END'.encode("utf8"))