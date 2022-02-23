import hashlib
import socket
from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import app_logger
from Image import Image, Base


def send_data_back(sock: socket, message: str):
    sock.send((message + '\r\n').encode())


def read_data_from_socket(sock: socket):
    return sock.recv(SIZE * 8)


def get_image_from_raw_data(data: bytearray):
    data = data.decode('utf-8')
    result = ''
    start = 0
    end = len(data)-1
    for i in range(0, len(data) - 1):
        if data[i] == chr(39) and start == 0:
            start = i
        if data[i] == chr(39) and start > 0:
            end = i
    result = data[start + 1:end]
    return result


def get_correct_answer_from_socket(data: str):
    data = data.split(":")
    return data[1].strip()


def main():
    logger = app_logger.get_logger(__name__)
    USER = 'root'
    HOST = "192.168.35.11"
    PORT = 13306
    DATABASE = 'ppc2_images'
    connection_string = "mysql+pymysql://%s:%s@%s:%s/%s" % (USER, "qRIAP", HOST, PORT, DATABASE)
    engine = create_engine(connection_string)
    Base.metadata.create_all(engine)
    session = Session(engine)
    URL = '195.50.2.219'
    PORT = 9007
    # COUNTER = 250
    try:
        SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SOCK.connect((URL, PORT))
        buffer = read_data_from_socket(SOCK)
        image = get_image_from_raw_data(buffer)
        send_data_back(SOCK, "text")
        sleep(0.1)
        answer = read_data_from_socket(SOCK).decode('utf-8')
        correct_answer = get_correct_answer_from_socket(answer)
        print(correct_answer)
        if '&' in correct_answer:
            sql_hash = hashlib.md5(image.encode('utf-8')).hexdigest()
            sql_text = correct_answer
            check = session.query(Image).filter(Image.image_hash == sql_hash).first()
            if not check:
                session.add(Image(image_hash=sql_hash,
                                  image_text=sql_text))
                session.commit()
        print("[+]:" + correct_answer)
        sleep(0.1)
    except BaseException as error:
        logger.info(str(error))
    finally:
        print(read_data_from_socket(SOCK))
        SOCK.close()
        exit(1)


SIZE = 1024
if __name__ == "__main__":
    main()
