import socket


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
