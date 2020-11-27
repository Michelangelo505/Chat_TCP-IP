import sys
from PyQt5 import QtWidgets
import gui.MainChatRoom as gui
from Client.Client import ChatClient
import threading


class GuiApp(QtWidgets.QMainWindow, gui.Ui_MainWindow):

    def __init__(self, ip_address, port):
        super().__init__()
        self.setupUi(self)
        self.pushButtonSend.clicked.connect(self.send_message)
        self.actionExit.triggered.connect(self.exit_app)
        self.client = ChatClient(ip_server=ip_address, port=port)
        self.client.run()

    def listen_server(self):
        while True:
            data = self.client.listen()
            if data:
                print(data)
                # self.ChatRoom.appendPlainText(data)

    def send_message(self):
        data = self.MessageWindow.toPlainText()
        self.client.send(data=data)
        self.MessageWindow.clear()

    def exit_app(self):
        self.client.close_connection()
        QtWidgets.qApp.quit()


def main():
    ip = sys.argv[1]
    port = int(sys.argv[2])
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = GuiApp(ip, port)  # Создаём объект класса ExampleApp
    threading.Thread(target=window.listen_server, args=()).start()
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение





if __name__ == '__main__':
    main()  # то запускаем функцию main()
