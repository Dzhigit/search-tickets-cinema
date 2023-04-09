import logging

import socket
import pickle

from client.data.config import host, port


class BasicDispatchClient(socket.socket):
    def __init__(self):
        super(BasicDispatchClient, self).__init__(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.host, self.port = host, port
        self.logger = logging.getLogger('connection')

    def set_up(self):
        self.logger.debug('Connect to server host {}, port {}'.format(self.host, self.port))
        self.connect(
            (self.host, self.port)
        )

    def listen_server(self):
        while True:
            self.logger.debug('Waiting for the data to be received from the server')
            data = pickle.loads(self.recv(102400))
            if not data:
                self.logger.debug('Data on server has not information')
                continue
            else:
                self.logger.debug('Data received {}'.format(data))
                return data

    def send_data(self, **kwargs):
        self.logger.debug('Sending data to server')
        self.sendall(pickle.dumps(kwargs))
        self.logger.debug('Data sent successfully')


# For debugging
if __name__ == '__main__':
    with BasicDispatchClient() as connection:
        connection.set_up()