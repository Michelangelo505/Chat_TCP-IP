import sys
import tkinter
from Client.Client import ChatClient
import threading
import time


class frame():
    def __init__(self, ip, port):
        self.client = ChatClient(ip_server=ip, port=port)
        self.client.run()
        self.top = tkinter.Tk()
        self.top.title("Chatter")
        self.messages_frame = tkinter.Frame(self.top)
        self.my_msg = tkinter.StringVar()  # For the messages to be sent.
        self.my_msg.set("Type your messages here.")
        self.scrollbar = tkinter.Scrollbar(self.messages_frame)  # To navigate through past messages.
        self.msg_list = tkinter.Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.entry_field = tkinter.Entry(self.top, textvariable=self.my_msg)
        self.entry_field.bind("<Return>", self.send_message)
        self.send_button = tkinter.Button(self.top, text="Send", command=self.send_message)
        self.top.protocol("WM_DELETE_WINDOW", self.exit_app)

    def listen_server(self):
        while True:
            data = self.client.listen()
            if data:
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
        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.msg_list.pack()
        self.messages_frame.pack()
        self.send_button.pack()
        self.entry_field.pack()
        threading.Thread(target=self.listen_server, args=(), daemon=True).start()
        tkinter.mainloop()


def main():
    ip = sys.argv[1]
    port = int(sys.argv[2])
    window = frame(ip, port)
    window.run()


if __name__ == '__main__':
    main()  # то запускаем функцию main()
