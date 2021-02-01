import socket


class SocketClient:

    host = None
    port = None
    curr_socket = None

    def __init__(self):
        pass

    def connect(self, hst, prt):
        self.host = hst
        self.port = prt
        self.curr_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.curr_socket.connect((self.host, self.port))

        except ConnectionRefusedError:
            return 0x1

        return 0x0

    def recv_response(self):
        payload = self.curr_socket.recv(9216)
        return payload

    def send_payload(self, data):
        self.curr_socket.send(bytes(data, encoding="utf-8"))

    def close(self):
        self.curr_socket.close()
