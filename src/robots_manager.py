# functions for robots.txt management

from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse

from src.getters import get_site_robots_from_db


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
        add_rp(result, robots)
    print(result)
    return rps[result].can_fetch("*", url)


def add_rp(url, content):
    rp = RobotFileParser()
    rps[url] = rp.parse(content)
