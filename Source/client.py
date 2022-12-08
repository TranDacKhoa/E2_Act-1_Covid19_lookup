import socket

FORMAT = 'utf8'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\

HOST = ''
PORT = int
server_address = (HOST, PORT)


def connect(host, port):
    global server_address
    server_address = (host, port)
    try:
        print(server_address)
        client.connect(server_address)
        print('connected to ' + str(server_address))
        return True
    except:
        return False


def send_list(list):
    global server_address, client
    size_data = 1024

    if isinstance(list, str):
        print('client gửi', list)
        client.sendall(list.encode(FORMAT))
        client.recv(size_data).decode()
    else:
        for item in list:
            print('client gửi', item)
            client.sendall(item.encode(FORMAT))
            client.recv(size_data).decode()

    client.sendall('end'.encode(FORMAT))


def receive_list():
    size_data = 1024
    list = []
    msg = 'received'

    data = client.recv(size_data).decode(FORMAT)
    while data != 'end':
        list.append(data)
        client.sendall(msg.encode(FORMAT))
        data = client.recv(size_data).decode(FORMAT)

    return list


def login_success(usr, psr):
    global server_address, client
    account = ["login", usr, psr]
    send_list(account)
    data = receive_list()
    print(data)
    if data[0] == 'login success':
        return True
    else:
        return False


def register_success(usr, psr):
    global server_address, client
    account = ["register", usr, psr]
    send_list(account)
    data = receive_list()
    print(data)
    if data[0] == 'register success':
        return True
    else:
        return False


def get_all_data():
    global server_address, client
    send_list("all data")

    size_data = 1024
    list = []
    msg = 'received'
    i = 0

    data = client.recv(size_data).decode(FORMAT)
    while data != 'end':
        list.append([])
        while data != 'end_i':
            list[i].append(data)
            client.sendall(msg.encode(FORMAT))
            data = client.recv(size_data).decode(FORMAT)
        data = client.recv(size_data).decode(FORMAT)
        i += 1

    return list


def receive_data_search():
    global server_address, client
    size_data = 1024
    list = []
    msg = 'received'

    data = client.recv(size_data).decode(FORMAT)
    while data != 'end':
        if data == 'end_i':
            data = client.recv(size_data).decode(FORMAT)
        else:
            list.append(data)
            client.sendall(msg.encode(FORMAT))
            data = client.recv(size_data).decode(FORMAT)

    return list


def search(date, month, year, country):
    global server_address, client
    key_search = ['search', date, month, year, country]
    send_list(key_search)
    data = receive_data_search()

    if data[0] == 'search failed':
        return False
    else:
        return data


def logout():
    global server_address, client
    data = 'logout'
    send_list(data)








