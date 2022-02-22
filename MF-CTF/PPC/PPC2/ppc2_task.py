import hashlib
import socket
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from Image import Image


def send_data_back(sock: socket, message: str):
    sock.send((message + '\r\n').encode('utf-8'))


def read_data_from_socket(sock: socket):
    return sock.recv(SIZE * 4)


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


USER = 'root'
HOST = "192.168.35.11"
PORT = 13306
DATABASE = 'ppc2_images'
connection_string = "mysql+pymysql://%s:%s@%s:%s/%s" % (USER, "qRIAP", HOST, PORT, DATABASE)
engine = create_engine(connection_string)
session = Session(engine)

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
        image_md5 = hashlib.md5(buffer.encode('utf-8')).hexdigest()
        check = session.query(Image).filter(Image.image_hash == image_md5).first()
        print(check.image_text)
        send_data_back(SOCK, check.image_text)
        sleep(0.3)
        # sleep(0.1)
        COUNTER -= 1
except BaseException as error:
    print("Exception: " + str(error))
finally:
    print(read_data_from_socket(SOCK))
    SOCK.close()
