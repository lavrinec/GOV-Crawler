# main file that contains main function

from src.crawler_worker import crawler_worker
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.page import Page
from src.site import Site

if __name__ == "__main__":
    file = open("connection.txt", "r")

    dbschema = 'crawldb'  # Searches left-to-right
    engine = create_engine(file.read(),
                           connect_args={'options': '-csearch_path={}'.format(dbschema)})
    Session = sessionmaker(bind=engine)
    session = Session()
    for u in session.query(Page).order_by(Page.id):
        print(u)
    for u in session.query(Site).order_by(Site.id):
        print(u)
    num_of_workers = sys.argv[1]
    # to be added: start num_of_workers crawlers in own processes
    crawler_worker()
