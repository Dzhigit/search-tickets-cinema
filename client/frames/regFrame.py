from ttkbootstrap.constants import *
import ttkbootstrap as ttk

from client.API.server_handler.constants import *
from client.frames.mainWindow import MainWindow
from client.data.config import theme

from threading import Thread


class RegFrame(ttk.Frame):
    def __init__(self, parent, previous, connection, **kwargs):
        super(RegFrame, self).__init__(parent, **kwargs)

        self.parent = parent
        self.previous = previous
        self.connection = connection

        # form variables
        self.email = ttk.StringVar(value='')
        self.name = ttk.StringVar(value='')
        self.password = ttk.StringVar(value='')
        self.re_password = ttk.StringVar(value='')
        self.code = ttk.StringVar(value='')

        # Head
        ttk.Label(self, text='Fill in the following information if you are creating an account').pack(side=TOP, pady=5)

        # creating
        email_head = 'Enter your future mail'
        self.create_form_entry(email_head, 'mail', self.email)

        name_head = 'Enter your future name'
        self.create_form_entry(name_head, 'name', self.name)

        password_head = 'Enter your future password'
        self.create_form_entry(password_head, 'password', self.password)

        re_password_head = 'Repeat the password you entered'
        self.create_form_entry(re_password_head, 're-password', self.re_password)

        code_head = 'Code sent to your email'
        self.create_form_entry(code_head, 'code', self.code)

        self.create_button_box()

    def create_form_entry(self, head, label, variable):
        container = ttk.Frame(self)
        container.pack(fill=X, pady=5)

        ttk.Label(container, text=head).pack(side=TOP, fill=X)

        lbl = ttk.Label(container, width=15, text=label.title())
        lbl.pack(side=LEFT, padx=5)

        ent = ttk.Entry(container, width=45, textvariable=variable)
        ent.pack(side=LEFT, fill=X, padx=5)

    def create_button_box(self):
        container = ttk.Frame(self)
        container.pack(fill=X, expand=TRUE)

        send_code_label = ttk.Label(
            container,
            bootstyle=INFO,
            text='send code to email',
            cursor='hand2'
        )
        send_code_label.bind('<Button-1>', lambda _: self.on_send_code(send_code_label))
        send_code_label.pack(side=TOP, pady=10)

        send_btn = ttk.Button(
            container,
            width=10,
            text='send',
            takefocus=0,
            command=self.on_send
        )
        send_btn.pack(side=RIGHT, pady=25, padx=5)

        cancel_btn = ttk.Button(
            container,
            width=10,
            text='cancel',
            takefocus=0,
            command=self.on_cancel
        )
        cancel_btn.pack(side=RIGHT, pady=25, padx=5)

    def on_send_code(self, label, event=None):
        label.configure(bootstyle=SECONDARY, cursor='arrow', state=DISABLED)

        email = self.email.get()
        if len(email) > 0:
            self.connection.send_data(type=REGISTRATION_CODE, email=email)

    def on_send(self):
        user_name = self.name.get()
        email = self.email.get()
        password = self.password.get()
        re_password = self.re_password.get()
        code = self.code.get()

        if password == re_password:
            self.connection.send_data(
                type=REGISTRATION,
                user_name=user_name,
                email=email,
                password=password,
                code=code
            )
            status = self.connection.listen_server()['status']
            if status == CONFIRMED:
                self.parent.destroy()
                MainWindow(title='Cinema Searcher', themename=theme).mainloop()
            else:
                pass

    def on_cancel(self):
        self.pack_forget()
        self.previous.pack()


if __name__ == '__main__':
    # from client.utils.misc.connection import connection
    from loginFrame import LoginFrame

    root = ttk.Window(title='Registration frame')
    RegFrame(root, LoginFrame(root, connection=None), connection=None).pack()
    root.mainloop()