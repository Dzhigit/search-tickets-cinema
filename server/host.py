import asyncio
import socket
import pickle
import smtplib

from random import randint

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from data.config import host, port, smtp_login, smtp_password
from event_types import Events

from db_handler import BaseDBHandler


class RequestHandler(socket.socket):
    def __init__(self):
        super(RequestHandler, self).__init__(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.users_code = {}
        self.server_smtp = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        self.db = BaseDBHandler()

        self.event_loop = asyncio.new_event_loop()
        self.exception = self.event_loop.set_exception_handler(handler=None)

        self.set_up()

    def set_up(self):
        self.bind(
            (host, port)
        )
        self.listen()

        self.server_smtp.login(smtp_login, smtp_password)

        self.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.setblocking(False)
        self.settimeout(0)

    def start_server(self):
        self.event_loop.run_until_complete(self.accepted_client())

    async def accepted_client(self):
        while True:
            conn, addr = await self.event_loop.sock_accept(self)
            self.event_loop.create_task(self.listen_client(conn))

    async def listen_client(self, conn):
        while True:
            try:
                data = await self.event_loop.sock_recv(conn, 1024)
                obj = pickle.loads(data)
            except Exception as exc:
                break
            else:
                if not data:
                    continue
                else:
                    if obj['type'] == Events.LOGIN:
                        db_data = self.db.search_data()

                        for users in db_data:
                            for user in users:
                                if user == obj['user_name']:
                                    if obj['password'] == users[3]:
                                        await self.send_data(conn, status=Events.CONFIRMED)
                                    else:
                                        await self.send_data(conn, status=Events.NOT_CONFIRMED)

                    elif obj['type'] == Events.REGISTRATION:
                        db_data = self.db.search_data()

                        for users in db_data:
                            for user in users:
                                if user == obj['user_name']:
                                    await self.send_data(conn, status=Events.NOT_CONFIRMED)
                                else:
                                    if obj['code'] == self.users_code[conn]:
                                        del self.users_code[conn]
                                        self.db.insert_data(obj['user_name'], obj['email'], obj['password'])
                                        print(self.db.search_data())
                                        await self.send_data(conn, status=Events.CONFIRMED)
                                    else:
                                        await self.send_data(conn, status=Events.NOT_CONFIRMED)

                    elif obj['type'] == Events.RECOVERY:
                        db_data = self.db.search_data()

                        for users in db_data:
                            for user in users:
                                if user != obj['email']:
                                    await self.send_data(conn, status=Events.NOT_CONFIRMED)
                                else:
                                    if obj['code'] == self.users_code[conn]:
                                        del self.users_code[conn]
                                        self.db.update_data(obj['password'], obj['email'])
                                        print('confirmed')
                                        await self.send_data(conn, status=Events.CONFIRMED)
                                    else:
                                        await self.send_data(conn, status=Events.NOT_CONFIRMED)

                    elif obj['type'] == Events.REGISTRATION_CODE:
                        code = ''.join([str(randint(0, 9)) for i in range(6)])
                        self.users_code[conn] = code
                        self.send_email(obj['email'], 'Your registration code in STC', 'Your code - ' + code)

                    elif obj['type'] == Events.RECOVERY_CODE:
                        code = ''.join([str(randint(0, 9)) for i in range(6)])
                        self.users_code[conn] = code
                        self.send_email(obj['email'], 'Your recovery code in STC', 'Your code - ' + code)

    async def send_data(self, conn, **kwargs):
        if not kwargs:
            return
        else:
            await self.event_loop.sock_sendall(conn, pickle.dumps(kwargs))

    def send_email(self, to_addr, subject, text):
        msg = MIMEMultipart()
        msg['From'] = smtp_login
        msg['To'] = to_addr
        msg['Subject'] = subject

        msg.attach(
            MIMEText(text, 'plain')
        )

        self.server_smtp.sendmail(msg['From'], msg['To'], msg.as_string())


if __name__ == '__main__':
    import os

    if not os.path.exists('logs'):
        os.mkdir('logs')

    asyncio.set_event_loop_policy(
        asyncio.WindowsSelectorEventLoopPolicy()
    )

    server_tcp = RequestHandler()
    try:
        server_tcp.start_server()
    except Exception as exc:
        server_tcp.close()
        server_tcp.server_smtp.quit()
