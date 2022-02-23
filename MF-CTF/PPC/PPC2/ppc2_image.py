import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text

Base = declarative_base()


class Image(Base):
    __tablename__ = 'ppc2_images'

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    image_hash = Column(String(32), unique=True)
    image_text = Column(Text)

    def __repr__(self):
        return "<ppc2_image (hash='%s', text='%s')>" \
               % (self.image_hash, self.text)

    @staticmethod
    def is_image_exists(session: sqlalchemy.orm.session, checking_hash: str) -> bool:
        check = session.query(Image).filter(Image.image_hash == checking_hash).all()
        if len(check) > 0:
            return True
        return False
