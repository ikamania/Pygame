import socket

class Client:
    def __init__(self) -> None:
        self.IP, self.PORT = socket.gethostbyname(socket.gethostname()), 5050

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self) -> None:
        self.client.connect((self.IP, self.PORT))

    def disconnect(self) -> None:
        self.client.close()

    def send_to_server(self, message: str) -> None:
        self.client.sendall(message.encode())

    def receive_from_server(self) -> str:
        data = self.client.recv(1024)
        data = data.decode()

        return data