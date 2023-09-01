import json
import os
import threading
import time

import client
import signup_screen
import log_screen



with open('data.json', 'r') as data_file:
    data = json.load(data_file)


class SignUp(client.Client, signup_screen.SignUp):
    def main(self):
        self.connected = False

        threading.Thread(target=self.run).start()

        time.sleep(.4)  # need this if not, it won't find the gui components because they are not loaded yet
        while True:
            try:
                self.client_main()
                self.connect()
                self.root.ids.connection_status.text = "connection status : connected!"

                self.root.ids.connection_status.color = 0, 1, 0, 1
                self.connected = True
                break
            except ConnectionRefusedError:
                self.root.ids.connection_status.text = "connection status : failed to connect\nretrying in 2 seconds"
                self.connected = False
                time.sleep(2)

    def on_stop(self):
        if self.connected:
            self.send(self.DISCONNECT_PROTOCOL)
            os._exit(0)
        else:
            os._exit(0)

    def make_user(self, username):
        self.protocol_send(self.CHECK_USERNAME_PROTOCOL, username)

    def recv(self):
        while True:
            msg_length = self.server.recv(self.HEADER).decode(self.FORMAT)
            if msg_length and msg_length != "":
                msg_length = int(msg_length)
                msg = self.server.recv(msg_length).decode(self.FORMAT)

                # checking
                self.check_recveived_message(msg)

    def check_recveived_message(self, message):
        splited = message.split("///")
        if splited[0] == self.MAKER_USER_RETURN_PROTOCOL:
            result = eval(splited[1])
            self.root.ids.connection_status.text = (f"account creation result : {result}")
            if result: 
                self.root.ids.connection_status.color = 0, 1, 0, 1  # green
                data['has_account'] = True
                data['username'] = self.root.ids.username_input.text

                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)

            elif not result:
                self.root.ids.connection_status.color = 1, 1, 0, 1  # red

class Log(client.Client, log_screen.Log):
    def main(self):
        self.connected = False

        threading.Thread(target=self.run).start()

        time.sleep(.4)  # needs this delay, if not it won't find the gui components because they are not loaded yet thus throwing an error
        while True:
            try:
                self.client_main()
                self.connect()
                break
            except ConnectionRefusedError:
                self.connected = False
                time.sleep(2)

    def recv(self):
        while True:
            msg_length = self.server.recv(self.HEADER).decode(self.FORMAT)
            if msg_length and msg_length != "":
                msg_length = int(msg_length)
                msg = self.server.recv(msg_length).decode(self.FORMAT)

                # checking


    def on_stop(self):
        os._exit(0)

if data['has_account']:
    Log().main()
else:
    SignUp().main()
