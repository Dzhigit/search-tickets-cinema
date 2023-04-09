from ttkbootstrap.constants import *
import ttkbootstrap as ttk

from client.frames.regFrame import RegFrame
from client.frames.recoveryFrame import RecoveryFrame
from client.API.server_handler.constants import *
from client.frames.mainFrame import MainFrame
from client.data.config import theme

from threading import Thread


class LoginFrame(ttk.Frame):
    def __init__(self, parent, connection, **kwargs):
        super(LoginFrame, self).__init__(parent, **kwargs)

        self.parent = parent
        self.connection = connection

        # form variables
        self.login = ttk.StringVar(value='')
        self.password = ttk.StringVar(value='')

        self.create_form_entry('login:', self.login)
        self.create_form_entry('password:', self.password, '*')

        self.create_button_box()

    def create_form_entry(self, label, variable, mask=None):
        container = ttk.Frame(self)
        container.pack(fill=X, pady=5)

        lbl = ttk.Label(container, width=10, text=label.title())
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(container, width=50, textvariable=variable, show=mask)
        ent.pack(side=LEFT, fill=X, padx=5)

    def create_button_box(self):
        container = ttk.Frame(self)
        container.pack(fill=X)

        forgot_label = ttk.Label(
            container,
            bootstyle=INFO,
            text='Forgot password?',
            cursor='hand2'
        )
        forgot_label.bind('<Button-1>', self.on_forgot)
        forgot_label.pack(side=TOP)

        login_btn = ttk.Button(
            container,
            bootstyle=SECONDARY,
            width=10,
            text='login',
            takefocus=0,
            command=self.on_login
        )
        login_btn.pack(side=RIGHT, pady=15, padx=5)

        reg_btn = ttk.Button(
            container,
            bootstyle=SECONDARY,
            width=10,
            text='registration',
            takefocus=0,
            command=self.on_reg
        )
        reg_btn.pack(side=RIGHT, pady=15, padx=5)

    def on_forgot(self, event=None):
        self.pack_forget()
        RecoveryFrame(self.parent, self, self.connection).pack()

    def on_login(self):
        user_name = self.login.get()
        password = self.password.get()

        self.connection.send_data(type=LOGIN, user_name=user_name, password=password)
        status = self.connection.listen_server()['status']
        if status == CONFIRMED:
            self.pack_forget()
            MainFrame(self.parent, connection=self.connection).pack()
        else:
            pass

    def on_reg(self):
        self.pack_forget()
        RegFrame(self.parent, self, self.connection).pack()


if __name__ == '__main__':

    # from client.utils.misc.connection import connection

    root = ttk.Window(title='Login frame')
    LoginFrame(root, connection=None).pack()
    root.mainloop()
