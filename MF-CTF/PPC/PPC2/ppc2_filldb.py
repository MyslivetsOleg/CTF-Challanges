import hashlib

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import config as cfg
import ppc2_image as db_image
import ppc2_image_helper as hlp
import ppc_socket


def main():
    connection_string = "mysql+pymysql://%s:%s@%s:%s/%s" % (
        cfg.mysql["user"], cfg.mysql["passwd"], cfg.mysql["host"], cfg.mysql["port"], cfg.mysql["db"])
    engine = create_engine(connection_string)
    db_image.Base.metadata.create_all(engine)
    session = Session(engine)

    sock = ppc_socket.CTFSocket(cfg.mf_ctf["host"], cfg.mf_ctf["port"])
    sock.ctf_connect()

    img_info = sock.trinity(cfg.mf_ctf["size"]*4)
    print(img_info[0])
    print(img_info[1])
    if hlp.is_correct_image(img_info[0]) and hlp.is_correct_answer(img_info[1]):
        img_hash = hashlib.md5(img_info[0].encode('utf-8')).hexdigest()
        if not db_image.Image.is_image_exists(session, img_hash):
            session.add(db_image.Image(
                image_hash=img_hash,
                image_text=img_info[1]
            ))
            session.commit()


if __name__ == "__main__":
    main()
