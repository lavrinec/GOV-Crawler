from sqlalchemy import Column, Integer, String, TIMESTAMP, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Site(Base):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True)
    domain = Column(String(150))
    robots_content = Column(Text)
    sitemap_content = Column(Text)
    reservation_id = Column(Integer)
    reserved = Column(TIMESTAMP)

    def __repr__(self):
        return '<Site {0} {1}: {2} {3}>'.format(self.domain,
                                                self.robots_content,
                                                self.sitemap_content,
                                                self.reservation_id)
