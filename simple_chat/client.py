import socket
import sys
from typing import Tuple
from threading import Thread


class Client:
    def __init__(self, server_address: Tuple[str, int]):
        self.server_address = server_address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_server()

    def run_forever(self) -> None:
        Thread(target=self.listen_server, daemon=True).start()
        while True:
            new_message = input('->    ')
            self.sock.send(bytes(new_message, 'utf-8'))
            if new_message == 'quit':
                break

    def connect_server(self) -> None:
        try:
            self.sock.connect(self.server_address)
        except socket.error:
            print('Не удалось подключиться к серверу')
            sys.exit(0)

    def listen_server(self) -> None:
        while True:
            data = self.sock.recv(1024).decode('utf-8')
            print(data)


if __name__ == '__main__':
    if len(sys.argv) < 2 and ('@' in sys.argv[1]):
        sys.exit('Необходимо ввести ip и порт сервера')
    else:
        ip, port = sys.argv[1].split('@')
        server = (ip, int(port))
        c = Client(server).run_forever()
