# functions for db management

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# connect to db
def connect_to_db():
    file = open("connection.txt", "r")
    dbschema = 'crawldb'  # Searches left-to-right
    engine = create_engine(file.read(),
                           connect_args={'options': '-csearch_path={}'.format(dbschema)})
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


def work_with_db(sql_statement):
    return True
