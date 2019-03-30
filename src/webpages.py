# everything related to getting the html code and parsing it
from src import webdriver
from bs4 import BeautifulSoup
import json
import re

def visit_url(url):
    print("visit url", url)

    # mark url as visited/processed in db

    response = get_url_content(url)

    # TODO: check for redirects
    # TODO-in-TODO: find out if better from original content or parsed content

    return response


def get_url_content(url):
    print("get content for", url)

    webdriver.browser.get(url)

    har = json.loads(webdriver.browser.get_log('har')[0]['message'])
    response = har['log']['entries'][0]['response']

    status_code = response['status']

    if not status_code:  # if status_code == None
        if "not found" in response['statusText'].lower():
            status_code = 404
        # other, e.q. 401, 402, 403, ...

    content_type = list(filter(lambda x: x["name"] == "Content-Type", response['headers']))[0]["value"]

    content = webdriver.browser.page_source
    parsed_content = BeautifulSoup(content, 'html.parser')

    return {
        "status": status_code,
        "content": parsed_content,
        "content_type": content_type,
        "actual_url": webdriver.browser.current_url
    }


# podatki.gov.si
# <a class="view_mode view_lower active" view_mode="view_upper">Male</a>

def check_a_url(a_tag, base_url, domain):
    url = a_tag.get("href")
    print('url', url)

    if not url:
        # just to prevent errors
        return None

    if url.startswith('https://') or url.startswith('http://') or url.startswith('ftp://'):
        # url is absolute path
        return url

    if url.startswith('/'):
        # path is relative to domain
        if domain.endswith('/'):
            domain = domain[:-1]
        return domain + url

    if url.startswith('file:/'):
        # SKIP ... complicated check if / or // or /// and if absolute or relative path
        return None

    if url.startswith('mailto:') or url.startswith('javascript:'):
        # mailto: or javascript: => skip
        return None

    # otherwise, url is absolute address
    # if absolute path, add base url
    if not base_url.endswith('/'):
        base_url += '/'
    return base_url + url


def check_onclick_url(onclick_tag, base_url, domain):
    onclick_code = onclick_tag.get("onclick")
    print("code", onclick_code)

    if 'location.href=' in onclick_code or 'location=' in onclick_code:
        re_match = re.search("location\.href\s*=\s*(\'|\").*(\'|\")", onclick_code)
        if not re_match:
            re_match = re.search("location\s*=\s*(\'|\").*(\'|\")", onclick_code)

        substr = re_match.group()
        # get the url from substr
        return "test"

    #  'location.replace(' in line
    #  'location.assign(' in line
    #  'window.open(' in line
    #  'parent.open(' in line
    return None


def get_links_from_content(base_url, parsed_content):
    # TODO check if correct link
    print("get links from content")

    base_tag = parsed_content.find('base')
    if base_tag:
        base_url = base_tag.get("href")

    base_url_split = base_url.split("/")
    domain = "/".join(base_url_split[:3])
    print("dom", domain, base_url_split)

    a_tags = parsed_content.find_all('a', href=True)  # array of <a> tags
    a_urls = list(map(lambda a_tag: check_a_url(a_tag, base_url, domain), a_tags))  # array of urls from <a> tags
    print("a_urls", a_urls)

    # case sensitive - onclick !== onClick, but we don't check onClick as it's not a standard
    tags_onclick = parsed_content.find_all(onclick=True)
    onclick_urls = list(map(lambda onclick_tag: check_onclick_url(onclick_tag, base_url, domain), tags_onclick))
    print("onclick_urls", onclick_urls)

    return None


def get_img_urls_from_content(parsed_content):
    print("get img urls from content")

    img_tags = parsed_content.find_all('img')

    img_urls = list(map(lambda link: link.get("src"), img_tags ))  # array of urls
    print("img_urls", img_urls)

    return img_urls
