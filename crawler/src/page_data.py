from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PageData(Base):
    __tablename__ = 'page_data'
    id = Column(Integer, primary_key=True)
    page_id = Column(Integer)
    data_type_code = Column(String(100))
    data = Column(LargeBinary)

    def __repr__(self):
        return '<Page {0} {1}: {2}>'.format(self.page_id,
                                            self.data_type_code,
                                            self.data)
