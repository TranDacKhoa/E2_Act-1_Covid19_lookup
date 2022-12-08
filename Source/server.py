import socket
import pyodbc
from threading import Thread
import api


FORMAT = 'utf8'
receive = 'received'
list_client = []
list_client_activate_addr = []
list_client_activate = []
tab = '      |      '


class LoginRegister:
    def __init__(self, username, password):
        self.User = username
        self.Pass = password
        self.conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                    SERVER=LGGRAM\SQLEXPRESS; Database=Socket_MMT; UID=lc; PWD=1;')

        self.cursor = self.conn.cursor()
        self.cursor.execute("select * from Account")
        self.data = self.cursor.fetchall()

        self.n = len(self.data)

    def user_is_empty(self):
        for i in range(0, self.n):
            if self.data[i][0] == self.User:
                return False
        return True

    def register_success(self):
        if(self.user_is_empty()):
            self.cursor.execute(f"insert Account values ('{self.User}','{self.Pass}')")
            self.conn.commit()
            self.conn.close()
            return True
        return False

    def LoginSuccess(self):
        for i in range(0, self.n):
            if self.data[i][0] == self.User and self.data[i][1] == self.Pass:
                return True
        return False


class threading_sever:
    def __init__(self, HOST, PORT):
        self.host = HOST
        self.port = PORT
        self.socket_sever = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_sever.bind((self.host, self.port))

    def auto_update_data(self):
        api.cycleGetAPI()

    def accept(self):
        self.socket_sever.listen(5)
        global list_client
        while True:
            conn, addr = self.socket_sever.accept()
            print('Conected by ', addr)
            #conn.settimeout(60)

            list_client.append(addr)
            list_client_activate_addr.append(addr)
            list_client_activate.append('connected')

            thr = Thread(target=self.MainThread, args=(conn, addr))
            thr.daemon = True
            thr.start()

    def handle_login(self, data, conn, addr):
        usr = data[1]
        pswr = data[2]

        if not LoginRegister(usr, pswr).LoginSuccess():
            self.send_list(conn, "Account doesn't correct!!!\nRe-input Account!!")
            list_client_activate_addr.append(addr)
            list_client_activate.append('login failed')
            print('login failed')
        else:
            print(addr, 'Login success')
            list_client_activate_addr.append(addr)
            list_client_activate.append('login success' + tab + 'username: '+usr)
            self.send_list(conn, 'login success')

    def handle_register(self, data, conn, addr):
        usr = data[1]
        pswr = data[2]

        if not LoginRegister(usr, pswr).register_success():
            self.send_list(conn, "Username has already existed!!!\nRe-input Account!!")
            list_client_activate_addr.append(addr)
            list_client_activate.append('register failed')
        else:
            print(addr, 'Register success')
            list_client_activate_addr.append(addr)
            list_client_activate.append('register success' + tab + 'username: '+usr)
            self.send_list(conn, 'register success')

    def send_pyodbc(self, conn, list):
        size_data = 1024
        for i in range(len(list)):
            for item in list[i]:
                conn.sendall(str(item).encode(FORMAT))
                conn.recv(size_data).decode()
            conn.sendall('end_i'.encode(FORMAT))

        conn.sendall('end'.encode(FORMAT))

    def handle_send_all_data(self, conn, addr):
        all_data = list(api.all_data())
        self.send_pyodbc(conn, all_data)

    def handle_search(self, key_search, conn, addr):
        date = key_search[1]
        month = key_search[2]
        year = key_search[3]
        country = key_search[4]
        data = api.search(date, month, year, country)
        if data:
            print('search success')
            self.send_pyodbc(conn, data)
            list_client_activate_addr.append(addr)
            list_client_activate.append('search success')
        else:
            print('search failed')
            self.send_list(conn, 'search failed')
            list_client_activate_addr.append(addr)
            list_client_activate.append('search failed')


    def send_list(self, conn, list):
        size_data = 1024

        if isinstance(list, str):
            conn.sendall(list.encode(FORMAT))
            conn.recv(size_data).decode()
        else:
            for item in list:
                conn.sendall(item.encode(FORMAT))
                conn.recv(size_data).decode()

        conn.sendall('end'.encode(FORMAT))

    def receive_list(self, conn):
        size_data = 1024
        list = []
        msg = 'received'

        data = conn.recv(size_data).decode(FORMAT)
        while data != 'end':
            list.append(data)
            conn.sendall(msg.encode(FORMAT))
            data = conn.recv(size_data).decode(FORMAT)

        return list

    def MainThread(self, conn, addr):
        try:
            while True:
                data = self.receive_list(conn)
                print(data)
                if data[0] == "logout":
                    list_client_activate_addr.append(addr)
                    list_client_activate.append('logout')
                if data[0] == "login":
                    self.handle_login(data, conn, addr)
                if data[0] == "register":
                    self.handle_register(data, conn, addr)
                if data[0] == "all data":
                    self.handle_send_all_data(conn, addr)
                if data[0] == "search":
                    self.handle_search(data, conn, addr)
                if data[0] == "quit":
                    break

        finally:
            print(addr, 'closed')
            list_client.remove(addr)
            list_client_activate_addr.append(addr)
            list_client_activate.append('disconnect')
            conn.close()


while True:
    ip_num = socket.gethostname()
    port_num = 20000
    try:
        port_num = int(port_num)
        break
    except ValueError:
        pass

print(ip_num)
api.getAPI()

server = threading_sever(ip_num, port_num)

thr1 = Thread(target=server.accept)
thr2 = Thread(target=server.auto_update_data)

thr1.daemon = True
thr2.daemon = True

thr1.start()
thr2.start()











