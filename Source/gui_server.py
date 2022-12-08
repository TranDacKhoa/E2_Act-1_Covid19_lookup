import sys
import time
from tkinter import *
from tkinter import messagebox
import server
from threading import Thread
'''from threading import Thread
from tkinter import scrolledtext
from tkinter import ttk
from tkinter.ttk import Frame, Style'''


class main_window():
    def __init__(self):
        self.window_server = Tk()
        self.window_server.title('SERVER')
        self.window_server.geometry("1000x550")
        self.window_server.protocol("WM_DELETE_WINDOW", self.handle_close)

        self.ip_server = Listbox(self.window_server, height=1, width=20, bg='floral white', fg='#20639b')
        self.port_server = Listbox(self.window_server, height=1, width=20, bg='floral white', fg='#20639b')
        self.refresh_btn = Button(self.window_server, text="REFRESH", bg='light yellow', fg='#000033',
                                  command=self.refresh_data)
        self.ip_server.insert(1, server.ip_num)
        self.port_server.insert(1, server.port_num)

        self.on_of_radio = IntVar()
        self.rad_on = Radiobutton(self.window_server, text='On', value=1,
                                  variable=self.on_of_radio, command=self.thread_auto_refresh)
        self.rad_off = Radiobutton(self.window_server, text='Off', value=2, variable=self.on_of_radio)

        self.client_activate = Listbox(self.window_server, height=22, width=75, bg='floral white', fg='#20639b')
        self.client_ip = Listbox(self.window_server, height=22, width=60, bg='floral white', fg='#20639b')

    def show(self):
        Label(self.window_server, text="SERVER THE WORLD'S COVID INFORMATION", fg='#FF9966', font=("Arial Bold", 15),
              pady=10).place(x=0, y=0)

        Label(self.window_server, fg='#000033', text="IP Server", font=("Arial", 10)).place(x=50, y=65)
        Label(self.window_server, fg='#000033', text="Port Server", font=("Arial", 10)).place(x=350, y=65)
        Label(self.window_server, fg='#000033', text="Auto Refresh Activate Client"
              , font=("Arial", 10)).place(x=560, y=65)
        self.ip_server.place(x=55, y=90)
        self.port_server.place(x=355, y=90)
        self.rad_on.place(x=575, y=90)
        self.rad_off.place(x=650, y=90)
        self.refresh_btn.place(x=800, y=85)

        Label(self.window_server, fg='#000033', text="Client Activate", font=("Arial", 10)).place(x=65, y=155)
        Label(self.window_server, fg='#000033', text="Client List", font=("Arial", 10)).place(x=565, y=155)
        self.client_activate.place(x=55, y=180)
        self.client_ip.place(x=555, y=180)

        self.window_server.mainloop()

    def refresh_data(self):
        self.client_activate.delete(0, END)
        self.client_ip.delete(0, END)
        for i in range(len(server.list_client)):
            self.client_ip.insert(i, str(server.list_client[i]))

        for i in range(len(server.list_client_activate_addr)):
            temp = str(server.list_client_activate_addr[i]) + ' ' + server.list_client_activate[i]
            self.client_activate.insert(i, temp)

    def auto_refresh_active(self):
        self.refresh_data()
        time.sleep(30)
        if self.on_of_radio.get() == 1:
            self.auto_refresh_active()

    def thread_auto_refresh(self):
        thr = Thread(target=self.auto_refresh_active)
        thr.daemon = True
        thr.start()

    def handle_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window_server.destroy()
            sys.exit()


main_window().show()
