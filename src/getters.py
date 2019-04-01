# getters for site, page, ...
from bs4 import BeautifulSoup

from src import db_manager
from src.image import Image
from src.link import Link
from src.page import Page
from src.page_image import PageImage
from src.savers import save_page_to_db, save_link_to_db, save_site_to_db, save_page_image_to_db, save_image_to_db
from src.site import Site
from sqlalchemy import and_, func, update, exc
from random import randint
from datetime import datetime
import requests
from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse
import re


def get_frontier_from_db():
    return True


def get_page_from_db():
    return True


def get_all_sites():
    for u in db_manager.session.query(Site).order_by(Site.id):
        #print(u)
        pass


def get_all_pages():
    for u in db_manager.session.query(Page).order_by(Page.id):
        #print(u)
        pass


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


def set_site_id(base, id):
    site_ids[base] = id
    return id


def get_site_id_for_url(url):
    base = get_base_url(url)
    site_id = site_ids.get(base, None)
    if site_id is None:
        site = get_site_from_db(base)
        return set_site_id(base, site.id)
    else:
        return site_id


def add_frontier_url(url):
    #print("Adding to frontier ", url)
    site_id = get_site_id_for_url(url)
    frontier = Page(url=url, site_id=site_id, page_type_code='FRONTIER')
    save_page_to_db(frontier)


def add_frontier(url):
    if can_fetch(url):
        add_frontier_url(url)
    else:
        #print("URL not allowed: ", url)
    pass


def get_site_robots(site):
    r = requests.get(site.domain + "robots.txt")
    status = r.status_code
    if status is not None and 200 <= status < 300:
        content = r.text
    else:
        content = "Allow: /"
    #print(content)
    site.robots_content = content
    base = get_base_url(site.domain)
    add_rp(base, content)
    x = re.findall("^Sitemap:(.*)", content, re.MULTILINE)

    if x:
        #print("YES! We have a sitemap match!", x)
        for val in x:
            get_site_sitemap(val.strip(), site)
    else:
        #print("No sitemap match")
        site.sitemap_content = "None"


def process_sitemap(xml):
    soup = BeautifulSoup(xml)
    sitemap_tags = soup.find_all("sitemap")
    url_tags = soup.find_all("url")
    xml_dict = []

    #print("The number of sitemaps are {0} and {1}".format(len(sitemap_tags), len(url_tags)))

    for sitemap in sitemap_tags:
        xml_dict.append(sitemap.findNext("loc").text)

    for sitemap in url_tags:
        xml_dict.append(sitemap.findNext("loc").text)

    for page in xml_dict:
        add_frontier(page)


def get_site_sitemap(url, site):
    #print("Sitemap za ", url)
    r = requests.get(url)
    status = r.status_code
    if status is not None and 200 <= status < 300:
        content = r.text
    else:
        content = "None"

    site.sitemap_content = content
    cancel_reservation(site)
    process_sitemap(content)


def get_site_data(site):
    get_site_robots(site)
    # get_site_sitemap(site)


def cancel_reservation(input):
    try:
        input.reservation_id = None
        input.reserved = None
        db_manager.session.commit()
    except exc.SQLAlchemyError as e:
        print('exception for reservation ', str(e))


def get_new_site():
    site = get_not_reserved_site()
    if site is None:
        return None
    #print("New site ", site.domain)
    set_site_id(get_base_url(site.domain), site.id)
    get_site_data(site)
    cancel_reservation(site)
    add_frontier(site.domain)
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

    # return result
    try:
        # Execute update
        db_manager.session.execute(q)
        db_manager.session.commit()
        return db_manager.session.query(param).filter(param.reservation_id == rand).one()
    except exc.SQLAlchemyError as e:
        db_manager.handel_exception(e, True, 'get not reserved', rand)
        return None


def finish_page(page, page_type='HTML'):
    #print("finish page")
    # TODO set page new page_type_code
    page.page_type_code = page_type
    cancel_reservation(page)


# last resort if something goes wrong (you stop a program at the wrong time)
# call these functions to reset all reservations of pages, sites

def cancel_all_sites_reservations():
    for site in db_manager.session.query(Site).order_by(Site.id):
        cancel_reservation(site)


def cancel_all_pages_reservations():
    for page in db_manager.session.query(Page).order_by(Page.id):
        cancel_reservation(page)


def get_site_from_db(site):
    try:
        return db_manager.session.query(Site).filter(Site.domain.like("%" + site + "%")).one()
    except exc.SQLAlchemyError as e:
        db_manager.handel_exception(e, True, 'get site robots', site)
        return None


def init():
    global rps
    global site_ids
    rps = {}
    site_ids = {}


def get_base_url(url):
    parsed_uri = urlparse(url)
    return '//{uri.netloc}/'.format(uri=parsed_uri)


def get_full_base_url(url):
    parsed_uri = urlparse(url)
    return '{uri.scheme}//{uri.netloc}/'.format(uri=parsed_uri)


def add_site(url, base):
    #print("Adding to sites ", url)
    site = Site(domain=url)
    save_site_to_db(site)
    return get_site_from_db(base)


def process_fetch_result(result, url, first_time):
    robots_check = rps.get(result, None)
    if robots_check is None:
        site = get_site_from_db(result)
        if site is None:
            #print("Currently skipping site ", result)
            # TODO uncoment when needing all sites from .gov.si
            # site = add_site(get_full_base_url(url), result)
            return False
        else:
            set_site_id(result, site.id)
        robots = site.robots_content
        if robots == "":
            #print("first time robots for domain ", result)
            if first_time:
                get_site_data(site)
                return process_fetch_result(result, url, False)
            else:
                return False
        #print("Saving inner robots", robots)
        robots_check = add_rp(result, robots)
    if robots_check is None:
        #print("find out why is None")
        return False
    else:
        can = robots_check.can_fetch("*", url)
        #print("results for site ", result, url, can)
        return can


def can_fetch(url) -> bool:
    result = get_base_url(url)
    if ".gov.si" not in result:
        #print("ni v gov.si", result)
        return False
    return process_fetch_result(result, url, True)


def add_rp(url, content):
    rp = RobotFileParser()
    rp.parse(content.splitlines())
    rps[url] = rp
    return rp


def get_page_from_db_by_url(link):
    try:
        return db_manager.session.query(Page).filter(Page.url == link).one()
    except exc.SQLAlchemyError as e:
        db_manager.handel_exception(e, True, 'get page by url', link)
        return None


def get_image_from_db_by_url(link):
    try:
        return db_manager.session.query(Image.id).filter(Image.url == link).one()
    except exc.SQLAlchemyError as e:
        db_manager.handel_exception(e, True, 'get image by url', link)
        return None


def get_page_from_url(link):
    add_frontier_url(link)
    return get_page_from_db_by_url(link)


def add_link_to_page(link, page):
    #print(link)
    if can_fetch(link):

	# removes hashes (anchors)
	split_by_hash = link.split("#")
	link = split_by_hash[0]

	# sort query params by abc
        split_by_query = link.split("?")
        if len(split_by_query) == 2:
            query_params = split_by_query[-1].split("&")
            query_params.sort()
            sorted_params = "&".join(query_params)
            link = split_by_query[0] + sorted_params

        connected = get_page_from_url(link)
        link = Link(from_page=page.id, to_page=connected.id)
        save_link_to_db(link)


def add_page_image(image_id, page_id):
    page_image = PageImage(page_id=page_id, image_id=image_id)
    save_page_image_to_db(page_image)


def connect_image_with_page(page_id, image_url, get_binary_data):
    if ".gov.si" not in image_url:
        #print("image is not inside gov.si", image_url)
        return False
    image_id = get_image_from_db_by_url(image_url)
    if image_id is None:
        image_data = get_binary_data(image_url)
        # image_data = {name, data, content_type}

        # TODO check if data is saved properly
        # Image object should be
        #   filename = image_data["name"]
        #   content_type = image_data["content_type"]
        #   data = image_data["data"]
        time = datetime.now()
        img = Image(url=image_url, filename=image_data["name"], content_type=image_data["content_type"],
                    data=image_data["data"], accessed_time=time)
        save_image_to_db(img)
        image_id = get_image_from_db_by_url(image_url)
    add_page_image(image_id, page_id)
