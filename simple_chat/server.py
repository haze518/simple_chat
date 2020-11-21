import socket
import sys
from typing import Tuple
from threading import Thread


def encode(word: str) -> bytes:
    return word.encode('utf-8')


class Server:
    def __init__(self, address: Tuple[str, int], n_clients: int):
        self.address = address
        self.n_clients = n_clients
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind_server()
        self.sock.listen(n_clients)
        self.clients = {}

    def bind_server(self) -> None:
        self.sock.bind(self.address)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run_forever(self) -> None:
        while True:
            try:
                conn, addr = self.sock.accept()
                self.clients[conn] = addr
                Thread(target=self.handle_request, args=(conn,), daemon=True).start()
            except KeyboardInterrupt:
                self.sock.close()
                break

    def handle_request(self, client: socket) -> None:
        client.send(encode('Добро пожаловать в чат, для выхода вбейте: quit'))
        client.send(encode(''))
        while True:
            data = client.recv(1024)
            name = self.get_name(client)
            if data != b'quit':
                msg = name + encode(' говорит : ') + data
                self.send_message(msg)
            else:
                client.send(b'quit')
                msg = encode('Пользователь: ') + name + encode(' вышел')
                self.send_message(msg)
                client.close()
                del self.clients[client]
                break

    def get_name(self, client: socket) -> bytes:
        return b'_'.join([bytes(str(i), 'utf-8') for i in self.clients[client]])

    def send_message(self, message: bytes) -> None:
        for client in self.clients:
            client.send(message)


if __name__ == '__main__':
    if len(sys.argv) < 2 and ('@' in sys.argv[1]):
        sys.exit('Необходимо ввести ip и порт сервера')
    else:
        ip, port = sys.argv[1].split('@')
        address = (ip, int(port))
        s = Server(address, 2).run_forever()
