# getters for site, page, ...

from src import db_manager
from src.page import Page
from src.site import Site
from sqlalchemy import and_, func, update
from random import randint
from datetime import datetime


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


def get_not_reserved_site():
    return get_not_reserved(Site, Site.reservation_id == None, Site.sitemap_content == None,
                            Site.robots_content == None)


def get_not_reserved_page():
    page = get_not_reserved(Page, Page.reservation_id == None, Page.page_type_code == "FRONTIER")
    if page is None:
        site = get_new_site()
        if site is not None:
            return get_not_reserved_page()
    return page


def get_site_robots(site):
    pass


def get_site_sitemap(site):
    pass


def get_site_data(site):
    get_site_robots(site)
    get_site_sitemap(site)


def cancel_reservation(input):
    input.reservation_id = None
    input.reserved = None
    db_manager.session.commit()


def get_new_site():
    site = get_not_reserved_site()
    if site is None:
        return None
    print("New site ", site.domain)
    get_site_data(site)
    cancel_reservation(site)
    return site


def get_not_reserved(param, *restrictions):
    rand = randint(-9999999, 9999999)
    timestamp = datetime.now()

    # Generate restriction
    sq = db_manager.session.query(param.id).filter(
        and_(*restrictions)).order_by(
        func.random()).limit(
        1).with_for_update()

    # Generate update
    q = update(param) \
        .values({param.reservation_id: rand, param.reserved: timestamp}) \
        .where(param.id == sq.as_scalar())

    # Execute update
    db_manager.session.execute(q)
    db_manager.session.commit()

    # return result
    try:
        return db_manager.session.query(param).filter(param.reservation_id == rand).one()
    except:
        return None


def finish_page(page):
    # TODO set page new page_type_code

    cancel_reservation(page)
