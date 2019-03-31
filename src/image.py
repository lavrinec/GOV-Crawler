from sqlalchemy import Column, Integer, String, TIMESTAMP, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, primary_key=True)
    filename = Column(String(255))
    content_type = Column(String(50))
    data = Column(LargeBinary)
    accessed_time = Column(TIMESTAMP)
    url = Column(String(3000))

    def __repr__(self):
        return '<Page {0} {1}: {2}>'.format(self.filename,
                                            self.url,
                                            self.data)
