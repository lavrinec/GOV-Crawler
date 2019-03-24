# functions for db management

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# connect to db
def connect_to_db():
    file = open("connection.txt", "r")
    read = file.read()
    # print(read)
    dbschema = 'crawldb'  # Searches left-to-right
    engine = create_engine(read,
                           connect_args={'options': '-csearch_path={}'.format(dbschema)})
    Session = sessionmaker(bind=engine)
    return Session()


def init():
    global session
    session = connect_to_db()


def handel_exception(e, rollback, where, second=None):
    print('exception for ', where, second, str(e))
    if rollback:
        session.rollback()
