from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text


Base = declarative_base()


class Image(Base):
    __tablename__ = 'ppc2_images'

    image_id = Column(Integer, primary_key=True, autoincrement=True)
    image_hash = Column(String(32), unique=True)
    image_text = Column(Text)

    def __repr__(self):
        return "<User(content='%s', hash='%s', text='%s')>" \
               % (self.image_hash, self.text)
