from client.data.config import theme
from client.utils.misc.connection import connection

from client.frames.mainWindow import MainWindow
from client.frames.authWindow import AuthorizationWindow


def on_startup(connect=connection):
    try:
        # AuthorizationWindow(title='Log in', themename=theme, connection=connect).mainloop()
        connect.set_up()
    except Exception as exc:
        AuthorizationWindow(title='Auth from STC', themename=theme, connection=connect).mainloop()
        # MainWindow(title='Search cinema info', themename=theme, connection=connect).mainloop()
        # ErrorWindow(title='Error window', themename=theme, connection=connection, exception=exc).mainloop()
        connect.close()
    else:
        AuthorizationWindow(title='Auth from STC', themename=theme, connection=connect).mainloop()
    finally:
        #shutil.rmtree(setup.temp_path + '/img')
        connect.close()

on_startup()