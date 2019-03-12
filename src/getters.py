# getters for site, page, ...

from src import db_manager
from src.page import Page
from src.site import Site
from sqlalchemy import and_, func, update
from random import randint
from datetime import datetime
import requests
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse


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
    r = requests.get(site.domain + "robots.txt")
    status = r.status_code
    if status is not None and 200 <= status < 300:
        content = r.text
    else:
        content = "Allow: /"
    print(content)
    site.robots_content = content
    base = get_base_url(site.domain)
    add_rp(base, content)


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
    print("finish page")
    # TODO set page new page_type_code

    cancel_reservation(page)


# last resort if something goes wrong (you stop a program at the wrong time)
# call these functions to reset all reservations of pages, sites

def cancel_all_sites_reservations():
    for site in db_manager.session.query(Site).order_by(Site.id):
        cancel_reservation(site)


def cancel_all_pages_reservations():
    for page in db_manager.session.query(Page).order_by(Page.id):
        cancel_reservation(page)


def get_site_robots_from_db(site):
    return db_manager.session.query(Site.robots_content).filter(Site.domain.like("%" + site + "%")).one()


def init():
    global rps
    rps = {}


def get_base_url(url):
    parsed_uri = urlparse(url)
    return '//{uri.netloc}/'.format(uri=parsed_uri)


def can_fetch(url) -> bool:
    result = get_base_url(url)
    if rps[result] is None:
        robots = get_site_robots_from_db(result)
        print(robots)
        add_rp(result, robots)
    print(result)
    return rps[result].can_fetch("*", url)


def add_rp(url, content):
    rp = RobotFileParser()
    rps[url] = rp.parse(content)
