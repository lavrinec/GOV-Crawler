from sqlalchemy import Column, Integer, String, TIMESTAMP, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Page(Base):
    # Base.metadata.schema = 'crawldb';
    __tablename__ = 'page'
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer)
    page_type_code = Column(String(100))
    url = Column(String(3000))
    html_content = Column(Text)
    http_status_code = Column(Integer)
    accessed_time = Column(TIMESTAMP)
    reservation_id = Column(Integer)
    reserved = Column(TIMESTAMP)

    def __repr__(self):
        return '<Page {0} {1}: {2}>'.format(self.page_type_code,
                                            self.url,
                                            self.html_content)
