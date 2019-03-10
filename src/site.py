from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Site(Base):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True)
    domain = Column(String(100))
    robots_content = Column(String(100))
    sitemap_content = Column(String(32))
    reservation_id = Column(Integer)

    def __repr__(self):
        return '<Site {0} {1}: {2} {3}>'.format(self.domain,
                                                self.robots_content,
                                                self.sitemap_content,
                                                self.reservation_id)
