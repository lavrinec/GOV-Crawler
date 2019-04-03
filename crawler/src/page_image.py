from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PageImage(Base):
    __tablename__ = 'page_image'
    page_id = Column(Integer, primary_key=True)
    image_id = Column(Integer, primary_key=True)

    def __repr__(self):
        return '<Link {0} {1}>'.format(self.page_id,
                                       self.image_id)
