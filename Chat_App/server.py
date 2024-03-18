import socket
import threading
import os
import time


class Server:
    def __init__(self) -> None:
        self.IP, self.PORT = socket.gethostbyname(socket.gethostname()), 5050

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []

    def show_info(self) -> None:
        while True:
            os.system('clear')

            print(f"Server Running On {self.IP}")
            print(f"Active Connections {threading.active_count() - 2}")
            time.sleep(2)

    def handle_client(self, conn, addr) -> None:
        # print(f"New Connection: {addr} Connected.")
        self.clients.append(conn)

        while conn:
            message = conn.recv(1024).decode()

            if len(message) > 0:
                self.send_to_clients(message)
            else:
                break

        conn.close()
        self.clients.remove(conn)

    def send_to_clients(self, message: str) -> None:
        for client in self.clients:
            client.sendall(message.encode())

    def start(self) -> None:
        self.server.bind((self.IP, self.PORT))
        self.server.listen()

        info = threading.Thread(target=self.show_info)
        info.start()

        while True:
            conn, addr = self.server.accept()
            print(conn, addr)

            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()


if __name__ == "__main__":
    server = Server()
    server.start()
