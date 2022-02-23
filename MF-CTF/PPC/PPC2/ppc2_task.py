import hashlib
from time import sleep
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ppc2_image import Image
import config as cfg
import ppc_socket
import ppc2_image_helper as hlp


def main():
    connection_string = "mysql+pymysql://%s:%s@%s:%s/%s" % (
        cfg.mysql["user"], cfg.mysql["passwd"], cfg.mysql["host"], cfg.mysql["port"], cfg.mysql["db"])
    engine = create_engine(connection_string)
    session = Session(engine)

    sock = ppc_socket.CTFSocket(cfg.mf_ctf["host"], cfg.mf_ctf["port"])
    sock.ctf_connect()
    counter = 250
    try:
        while counter != 0:
            buffer = sock.read_data_from_socket(8096)
            print(buffer.decode())
            buffer = hlp.get_image_from_raw_data(buffer)
            image_md5 = hashlib.md5(buffer.encode('utf-8')).hexdigest()
            check = session.query(Image).filter(Image.image_hash == image_md5).first()
            print(check.image_text)
            sock.send_data_back(check.image_text)
            sleep(0.3)
            counter -= 1
    except BaseException as error:
        print("Exception: " + str(error))
    finally:
        print(sock.read_data_from_socket(8096))
        sock.sock.close()


if __name__ == "__main__":
    main()
