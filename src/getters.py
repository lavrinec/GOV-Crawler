# getters for site, page, ...

from src.db_manager import connect_to_db
from src.page import Page
from src.site import Site

def get_frontier_from_db():
    return True


def get_site_from_db():
    return True


def get_page_from_db():
    return True

def get_all_sites():
    session = connect_to_db()
    for u in session.query(Site).order_by(Site.id):
        print(u)


def get_all_pages():
    session = connect_to_db()
    for u in session.query(Page).order_by(Page.id):
        print(u)