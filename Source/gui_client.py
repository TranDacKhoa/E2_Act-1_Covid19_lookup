import sys
from tkinter import *
import client
import socket
from tkinter import messagebox
from tkinter import ttk, scrolledtext


class connect_window():
    def __init__(self):
        self.bg = "#FFB266"
        self.window_connect = Tk()
        self.window_connect.title('CLIENT')
        self.window_connect.geometry("500x270")
        self.window_connect.configure(bg=self.bg)

        self.msg = Label(self.window_connect, font=("Arial Bold", 10), bg=self.bg, fg='red', pady=5)
        self.IP_entry = Entry(self.window_connect, bg='light yellow', fg='#FF6600')
        self.port_entry = Entry(self.window_connect, bg='light yellow', fg='#FF6600')

        self.bool_default = BooleanVar()
        self.bool_default.set(True)
        self.default_check = Checkbutton(self.window_connect, text='Sever default', font=("Arial Bold", 10), bg=self.bg
                                         , fg='#20639b', var=self.bool_default, command=self.check_btn_default)

    def show(self):
        Label(self.window_connect, text="CONNECT", font=("Arial Bold", 20), bg=self.bg, fg='#0099FF', pady=15).pack()
        Label(self.window_connect, text="IP Server", font=("Arial Bold", 10),
              bg=self.bg, fg='#6633FF', pady=5).place(x=110, y=70)
        Label(self.window_connect, text="Port Server", font=("Arial Bold", 10),
              bg=self.bg, fg='#6633FF', pady=5).place(x=110, y=110)

        self.IP_entry.place(x=190, y=77)
        self.port_entry.place(x=190, y=117)

        self.default_check.place(x=190, y=160)

        Button(self.window_connect, text="Connect", width=10, height=1, bg="#20639b", fg='floral white',
               command=self.handle_connect).place(x=210, y=200)

        self.IP_entry.focus()
        self.check_btn_default()
        self.window_connect.mainloop()

    def check_btn_default(self):
        if self.bool_default.get():
            ip_num = socket.gethostname()
            port_num = 20000
            self.IP_entry.delete(0, last=END)
            self.port_entry.delete(0, last=END)

            self.IP_entry.insert(0, ip_num)
            self.port_entry.insert(0, port_num)
        else:
            self.IP_entry.delete(0, last=END)
            self.port_entry.delete(0, last=END)

    def handle_connect(self):
        host = self.IP_entry.get()
        port = self.port_entry.get()

        try:
            port = int(port)
        except ValueError:
            self.msg.configure(text='Port must be type "int"')
            self.msg.place(x=180, y=230)
            return

        if host and port:
            if client.connect(host, port):
                self.window_connect.destroy()
                login_window().show()
            else:
                self.msg.configure(text='Connection failed')
                self.msg.place(x=190, y=230)
        else:
            self.msg.configure(text='Boxes cannot be empty')
            self.msg.place(x=170, y=230)


class login_window():
    def __init__(self):
        self.bg = "#FFB266"
        self.window_login = Tk()
        self.window_login.title('CLIENT')
        self.window_login.geometry("500x270")
        self.window_login.protocol("WM_DELETE_WINDOW", self.handle_close)
        self.window_login.configure(bg=self.bg)

        self.msg = Label(self.window_login, bg=self.bg, fg='red', pady=5)
        self.username_entry = Entry(self.window_login, bg='light yellow', fg='#FF6600')
        self.password_entry = Entry(self.window_login, bg='light yellow', fg='#FF6600', show='*')

    def show(self):
        Label(self.window_login, text="LOGIN", font=("Arial Bold", 20), bg=self.bg, fg='#0099FF', pady=15).pack()
        Label(self.window_login, text="Username * ", bg=self.bg, pady=5).pack()
        self.username_entry.pack()
        Label(self.window_login, text="Password * ", bg=self.bg, pady=5).pack()
        self.password_entry.pack()
        Label(self.window_login, text="", bg=self.bg).pack()
        Button(self.window_login, text="Login", width=10, height=1, bg="#20639b", fg='floral white',
               command=self.handle_login).pack()
        Button(self.window_login, text="Register", width=10, height=1, bg="#20639b", fg='floral white',
               command=self.handle_register).pack()

        self.username_entry.focus()
        self.window_login.mainloop()

    def login_thread(self, usr, psr):
        if client.login_success(usr, psr):
            self.window_login.destroy()
            search_window(usr).show()
        else:
            self.msg.configure(text='Account not found')
            self.msg.pack()

    def handle_login(self):
        usr = self.username_entry.get()
        psr = self.password_entry.get()
        if usr and psr:
            self.login_thread(usr, psr)
        else:
            self.msg.configure(text='Boxes cannot be empty')
            self.msg.pack()

    def register_thread(self, usr, psr):
        if client.register_success(usr, psr):
            self.msg.configure(text='Register success')
        else:
            self.msg.configure(text='Username has already existed!!!')
        self.msg.pack()

    def handle_register(self):
        usr = self.username_entry.get()
        psr = self.password_entry.get()
        if usr and psr:
            self.register_thread(usr, psr)
        else:
            self.msg.configure(text='Boxes cannot be empty')
            self.msg.pack()

    def handle_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window_login.destroy()
            client.send_list('quit')
            sys.exit()

class search_window():
    def __init__(self, username):
        self.window_search = Tk()
        self.window_search.title('CLIENT')
        self.window_search.geometry("1000x550")
        self.window_search.protocol("WM_DELETE_WINDOW", self.handle_close)
        self.bg = "#FFB266"
        self.window_search.configure(bg=self.bg)

        self.msg = Label(self.window_search, font=("Arial", 9), bg=self.bg, fg='RED', pady=5)

        self.avatar = Label(self.window_search, text=username, font=("Arial", 15), bg=self.bg, fg='#0066FF', pady=5)

        self.listbox_data = Listbox(self.window_search, width=135, height=20, bg='floral white', fg='#20639b')

        self.tab = '       |       '
        self.table_value = ['Date', 'Country', 'Total Case', 'Today Case',
                            'Active', 'Deaths', 'Today Deaths', 'Recovered', 'Critical']

        self.listbox_search = Listbox(self.window_search, width=100, height=3, bg='floral white', fg='#20639b')

        self.entry_country = Entry(self.window_search)
        self.combo_date = ttk.Combobox(self.window_search, width=25)
        self.combo_date['value'] = ("Date", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                                    20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31)
        self.combo_date.current(0)
        self.combo_month = ttk.Combobox(self.window_search, width=25)
        self.combo_month['value'] = ("Month", 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.combo_month.current(0)
        self.combo_year = ttk.Combobox(self.window_search, width=25)
        self.combo_year['value'] = ("Year", 2020, 2021)
        self.combo_year.current(0)

        self.btn_search = Button(self.window_search, text="SEARCH", bg="#20639b", fg='floral white',
                                 command=self.handle_search)
        self.btn_refresh = Button(self.window_search, text="REFRESH", bg='#20639b', fg='floral white',
                                 command=self.handle_refresh)
        self.btn_logout = Button(self.window_search, text="LOG OUT", bg='#20639b', fg='floral white',
                                 command=self.logout)

    def handle_data(self, all_data):
        self.listbox_data.delete(0, END)
        tab = '   '
        i_insert = 1
        for i in reversed(range(len(all_data))):
            data_j = ''

            for j in range(0, 2):
                data_j += all_data[i][j] + tab
            self.listbox_data.insert(i_insert, data_j)
            i_insert += 1
            data_j = ''

            for j in range(2, 9):
                data_j += tab + self.table_value[j] + ': ' + str(all_data[i][j]) + tab + '|'
            data_j = data_j[:-1]
            self.listbox_data.insert(i_insert, data_j)
            i_insert += 1

    def show(self):
        Label(self.window_search, text="FINDING THE WORLD'S COVID INFORMATION", bg=self.bg, fg='#0099FF'
              , font=("Arial Bold", 15), pady=10).place(x=0, y=0)

        self.avatar.place(x=900, y=0)
        Label(self.window_search, bg=self.bg, fg='#000033', text="Country", font=("Arial", 10)).place(x=100, y=75)
        Label(self.window_search, bg=self.bg, fg='#000033', text="Date", font=("Arial", 10)).place(x=250, y=75)
        Label(self.window_search, bg=self.bg, fg='#000033', text="Month", font=("Arial", 10)).place(x=495, y=75)
        Label(self.window_search, bg=self.bg, fg='#000033', text="Date", font=("Arial", 10)).place(x=740, y=75)
        self.entry_country.place(x=100, y=100)
        self.combo_date.place(x=250, y=100)
        self.combo_month.place(x=495, y=100)
        self.combo_year.place(x=740, y=100)

        self.btn_logout.place(x=900, y=36)
        self.btn_search.place(x=740, y=150)
        self.btn_refresh.place(x=840, y=150)
        self.listbox_search.place(x=100, y=140)
        self.listbox_data.place(x=100, y=200)
        #self.scrll.place(x=100, y=200)

        self.handle_refresh()
        self.entry_country.focus()
        self.window_search.mainloop()

    def handle_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window_search.destroy()
            client.send_list('quit')
            sys.exit()

    def handle_search(self):
        date = self.combo_date.get()
        month = self.combo_month.get()
        year = self.combo_year.get()
        country = self.entry_country.get()
        if country:
            data = client.search(date, month, year, country)
            if data == False:
                self.msg.configure(text='No data found')
                self.msg.place(x=775, y=175)
            else:
                self.msg.configure(text='')
                self.handle_search_data(data)
        else:
            self.msg.configure(text='Country box cannot be empty')
            self.msg.place(x=740, y=175)

    def handle_search_data(self, search_data):
        self.listbox_search.delete(0, END)
        tab = '    '
        i_insert = 1
        print(search_data)
        data_handle = ''

        for i in range(0, 2):
            data_handle += search_data[i] + tab

        self.listbox_search.insert(i_insert, data_handle)
        i_insert += 1
        data_handle = ''

        for i in range(2, 4):
            data_handle += tab + self.table_value[i] + ': ' + str(search_data[i]) + tab + '|'

        self.listbox_search.insert(i_insert, data_handle)
        i_insert += 1
        data_handle = ''

        for i in range(4, 9):
            data_handle += tab + self.table_value[i] + ': ' + str(search_data[i]) + tab + '|'

        data_handle = data_handle[:-1]
        self.listbox_search.insert(i_insert, data_handle)
        i_insert += 1

    def handle_refresh(self):
        all_data = client.get_all_data()
        self.handle_data(all_data)

    def logout(self):
        client.logout()
        self.window_search.destroy()
        login_window().show()
        #sys.exit()


connect_window().show()
