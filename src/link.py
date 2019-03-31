from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Link(Base):
    __tablename__ = 'link'
    from_page = Column(Integer, primary_key=True)
    to_page = Column(Integer, primary_key=True)

    def __repr__(self):
        return '<Link {0} {1}>'.format(self.from_page,
                                       self.to_page)
