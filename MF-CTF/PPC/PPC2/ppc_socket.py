import socket
import string
import time
import random

import ppc2_image_helper as hlp


class CTFSocket:
    def __init__(self, url, port) -> socket:
        self.port = port
        self.url = url
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def ctf_connect(self):
        self.sock.connect((self.url, self.port))

    def send_data_back(self: socket, message: str, eof='\r\n', encoding='utf-8'):
        """

        used for MF-CTF PPC tasks
        function sends an arbitrary message to socket

        :param self: socket information ip:port (based on socket class)
        :param message: message to send -> text
        :param eof: end of message should be \r\n to communicate with mf-ctf ppc tasks
        :param encoding: provide encoding to encode 'message' :param
        :return:
        """
        self.sock.send((message + eof).encode(encoding))

    def read_data_from_socket(self: socket, size: int) -> bytes:
        """

        used for MF-CTF PPC tasks
        function reads byte-stream from socket

        :param self: socket information ip:port (based on socket class)
        :param size: size in bytes to read
        :return: bytearray with data
        """
        return self.sock.recv(size)

    def trinity(self, size: int, sleep_time=0.1) -> list:
        """

        One-time triple action: send data o get image -> send reply with intentionally wrong answer -> get correct one

        :param size: size in bytes to read from socket
        :param sleep_time: time in seconds to sleep before operations
        :return: list with base64 image and correct answer
        """
        data = self.read_data_from_socket(size)
        b64image = hlp.get_image_from_raw_data(data)
        time.sleep(sleep_time)
        self.send_data_back(''.join(random.choice(string.ascii_letters) for x in range(10)))
        time.sleep(sleep_time)
        data = self.read_data_from_socket(size)
        answer = hlp.get_correct_answer(data.decode())
        return [b64image, answer]
