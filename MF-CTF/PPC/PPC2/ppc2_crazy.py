import socket
import base64
import io
from time import sleep

import PIL
from PIL.Image import Image


def send_data_back(sock: socket, message: str):
    sock.send((message + '\r\n').encode())


def read_data_from_socket(sock: socket):
    return sock.recv(SIZE * 8)


def get_image_from_raw_data(data: bytearray):
    data = data.decode('utf-8')
    result = ''
    start = 0
    end = 0
    for i in range(0, len(data) - 1):
        if data[i] == chr(39) and start == 0:
            start = i
        if data[i] == chr(39) and start > 0:
            end = i
    result = data[start + 1:end]
    return result


URL = '195.50.2.219'
PORT = 9007
SIZE = 1024
SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCK.connect((URL, PORT))
COUNTER = 250
try:
    while COUNTER != 0:
        buffer = read_data_from_socket(SOCK)
        print(buffer.decode())
        buffer = get_image_from_raw_data(buffer)
        # b_decoded = base64.b64decode(buffer)
        # img = Image.open(io.BytesIO(b_decoded))
        send_data_back(SOCK, "text")
        sleep(0.2)
        COUNTER -= 1
except PIL.UnidentifiedImageError as error:
    print("Exception: " + str(error))
finally:
    print(read_data_from_socket(SOCK))
    SOCK.close()