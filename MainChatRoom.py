import sys
import tkinter
from Client.Client import ChatClient
import threading
import time


class WindowApp:
    def __init__(self, ip, port, name):
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
                else:
                    self.msg_list.insert(tkinter.END, data)
            time.sleep(2)

    def send_message(self):
        msg = self.my_msg.get()
        self.my_msg.set("")  # Clears input field.
        self.client.send(msg)

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
