# getters for site, page, ...

from src import db_manager
from src.page import Page
from src.site import Site


def get_frontier_from_db():
    return True


def get_site_from_db():
    return True


def get_page_from_db():
    return True


def get_all_sites():
    for u in db_manager.session.query(Site).order_by(Site.id):
        print(u)


def get_all_pages():
    for u in db_manager.session.query(Page).order_by(Page.id):
        print(u)
