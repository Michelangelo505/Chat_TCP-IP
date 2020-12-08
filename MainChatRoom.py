import sys
import tkinter
from Client.Client import ChatClient
from encryption.protocols import DH
import threading
import time


class WindowApp:
    def __init__(self, ip, port, name):
        self.protocol = DH()
        self.client = ChatClient(ip_server=ip, port=port, name=name)
        self.top = tkinter.Tk()
        self.top.title("ChatRoom")
        self.messages_frame = tkinter.Frame(self.top)
        self.users_frame = tkinter.Frame(self.top)
        self.my_msg = tkinter.StringVar()  # For the messages to be sent.
        self.scrollbar_msg = tkinter.Scrollbar(self.messages_frame)  # To navigate through past messages.
        self.scrollbar_users = tkinter.Scrollbar(self.users_frame)
        self.msg_list = tkinter.Listbox(self.messages_frame, height=40, width=100,
                                        yscrollcommand=self.scrollbar_msg.set)
        self.users_list = tkinter.Listbox(self.users_frame, height=40, width=30,
                                          yscrollcommand=self.scrollbar_users.set)
        self.entry_field = tkinter.Entry(self.top, textvariable=self.my_msg, width=60)
        self.entry_field.bind("<Return>", self.send_message)
        self.send_button = tkinter.Button(self.top, text="Send", command=self.send_message)
        self.top.protocol("WM_DELETE_WINDOW", self.exit_app)

    def listen_server(self):
        while True:
            data = self.client.listen()
            if data:
                if data == "users":
                    self.users_list.delete(0, tkinter.END)
                    users = self.client.listen().split(',')
                    for user in users:
                        self.users_list.insert(tkinter.END, user)
                elif data == "100":
                    self.client.send(self.client.user.key_pub)
                    key_pub_users_1 = self.client.listen()
                    key_pub_users_2 = self.client.listen()
                    self.protocol.public_key1 = int(key_pub_users_1)
                    self.protocol.public_key2 = int(key_pub_users_2)
                    self.protocol.private_key = int(self.client.user.key_private)
                    self.client.user.key_partial = self.protocol.generate_partial_key()
                    print(f'KEYprivate = {self.client.user.key_private}\n'
                          f'KEYpub_user_1 = {key_pub_users_1}\n'
                          f'KEYpub_user_2 = {key_pub_users_2}\n')
                elif data == "101":
                    partial_key = str(self.client.user.key_partial)
                    self.client.send(partial_key)
                    key_partial_user = self.client.listen()
                    self.client.user.full_key = self.protocol.generate_full_key(int(key_partial_user))
                    print(self.client.user.full_key)
                    print(f'KEYpartial_user_1 = {self.client.user.key_partial}\n'
                          f'KEYpartial_user_2 = {key_partial_user}\n'
                          f'KEYfull = {self.client.user.full_key}\n')
                elif data == "102":
                    msg = 'connection established'
                    self.msg_list.insert(tkinter.END, msg)
                elif data == "103":
                    msg = 'The connection is lost. Another user left the chat'
                    self.msg_list.insert(tkinter.END, msg)
                else:
                    split_msg = data.split(':')
                    nickname = split_msg[0]
                    msg = split_msg[1]
                    decrypt_msg = self.protocol.decrypt_message(msg)
                    full_msg = f"{nickname}:{decrypt_msg}"
                    self.msg_list.insert(tkinter.END, full_msg)
            time.sleep(3)

    def send_message(self):
        msg = self.my_msg.get()
        self.my_msg.set("")  # Clears input field.
        encrypt_msg = self.protocol.encrypt_message(msg)
        self.client.send(encrypt_msg)

    def exit_app(self):
        self.client.close_connection()
        self.top.quit()

    def run(self):
        self.scrollbar_users.grid(row=0, column=0)
        self.users_list.grid(row=0, column=0)
        self.users_frame.grid(row=0, column=0)
        self.scrollbar_msg.grid(row=0, column=1)
        self.msg_list.grid(row=0, column=1)
        self.messages_frame.grid(row=0, column=1)
        self.send_button.grid(row=1, column=2)
        self.entry_field.grid(row=1, column=0, columnspan=4)
        self.client.run()
        threading.Thread(target=self.listen_server, args=(), daemon=True).start()
        tkinter.mainloop()


def main():
    ip = sys.argv[1]
    port = int(sys.argv[2])
    name = sys.argv[3]
    window = WindowApp(ip, port, name)
    window.run()


if __name__ == '__main__':
    main()  # то запускаем функцию main()
