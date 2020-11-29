import struct
import base64

class Message:
    __fixed_size = 4

    @staticmethod
    def get_data(connection, length_data):
        # Функция для получения данных
        data = b''
        while len(data) < length_data:
            # packet = connection.recv(length_data - len(data))
            # if not packet:
            #     # TODO переделать условие
            #     return None
            # data += packet
            try:
                packet = connection.recv(length_data - len(data))
                if not packet:
                    # TODO переделать условие
                    return None
                data += packet
            except Exception as error:
                pass
        return data

    @staticmethod
    def get_package(data):
        binary_data = data.encode("UTF-8")
        binary_data = base64.b64encode(binary_data)
        length_message = len(binary_data)
        package_message = struct.pack('>I', length_message) + binary_data
        return package_message

    def get_message(self, connection):
        # Получение длины сообщения и распаковка
        package_length_msg = self.get_data(connection=connection, length_data=self.__fixed_size)
        if not package_length_msg:
            # TODO переделать условие
            return None
        length_message = struct.unpack('>I', package_length_msg)[0]
        # Получение данных
        binary_message = self.get_data(connection=connection, length_data=length_message)
        binary_message = base64.b64decode(binary_message)
        message = binary_message.decode("UTF-8")
        return message
