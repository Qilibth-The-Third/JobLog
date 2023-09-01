import socket
import threading


class Client:
    def client_main(self):
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = 5050
        self.FORMAT = "utf-8"
        self.HEADER = 64

        self.DISCONNECT_PROTOCOL = "x0"
        self.CHECK_USERNAME_PROTOCOL = "x1"
        self.MAKER_USER_RETURN_PROTOCOL = "x2"

        self.connected = False

    def connect(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((self.IP, self.PORT))
        recv_thread = threading.Thread(target=self.recv)
        recv_thread.start()
        self.connected = True

    def send(self, msg):
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.server.send(send_length)
        self.server.send(message)

    def protocol_send(self, protocol, content):
        if self.connected:
            self.send(f"{protocol}///{content}")
        else:
            print("NOT CONNECTED")
