import socket
import threading
import json

class Server:
    def __init__(self):
        self.IP = socket.gethostbyname(socket.gethostname())
        self.PORT = 5050
        self.HEADER = 64
        self.FORMAT = "utf-8"

        self.DISCONNECT_PROTOCOL = "x0"
        self.CHECK_USERNAME_PROTOCOL = "x1"
        self.MAKER_USER_RETURN_PROTOCOL = "x2"

        self.connected = None

    def send_to_client(self, client, protocol, msg):
        msg = f"{protocol}///{msg}"
        message = msg.encode(self.FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        client.send(send_length)
        client.send(message)

    def handle_client(self, client, addr):
        print(f"{addr} connected")

        self.connected = True
        while self.connected:
            msg_length = client.recv(self.HEADER).decode(self.FORMAT)
            if msg_length and msg_length != "":
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(self.FORMAT)
                print(f"{addr}: {msg}")
                self.check(client, msg)
        client.close()

    def check(self,client,  msg):
        splited = msg.split("///")
        if splited[0] == self.DISCONNECT_PROTOCOL:
            self.connected = False
        elif splited[0] == self.CHECK_USERNAME_PROTOCOL:
            is_make_user_sccessful = self.make_user(splited[1])
            self.send_to_client(client, self.MAKER_USER_RETURN_PROTOCOL, is_make_user_sccessful)


    def main(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.IP, self.PORT))

        server.listen()

        print("server listening on " + self.IP)
        while True:
            client, addr = server.accept()
            client_handle_thread = threading.Thread(target=self.handle_client, args=(client, addr))
            client_handle_thread.start()


    def make_user(self, username):
        with open('database.json', 'r') as database:
            data = json.load(database)

        with open('database.json', 'w') as database:
            if username in data['users']:
                json.dump(data, database, indent=4)
                return False
            else:
                data['users'].append(username)
                json.dump(data, database, indent=4)
                return True
Server().main()
