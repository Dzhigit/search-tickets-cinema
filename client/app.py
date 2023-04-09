from client.data.config import theme
from client.utils.misc.connection import connection

from client.frames.authWindow import AuthorizationWindow


def on_startup(connect=connection):
    try:
        connect.set_up()
    except Exception as exc:
        connect.close()
    else:
        AuthorizationWindow(title='Auth from STC', themename=theme, connection=connect).mainloop()
    finally:
        connect.close()

on_startup()