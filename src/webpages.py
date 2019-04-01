# everything related to getting the html code and parsing it
from src import webdriver
from bs4 import BeautifulSoup
import json
import re
import requests
from io import BytesIO
from PIL import Image

def visit_url(url):
    print("visit url", url)

    # mark url as visited/processed in db

    response = get_url_content(url)

    # TODO: check for redirects

    return response


def get_url_content(url):
    print("get content for", url)

    webdriver.browser.get(url)

    try:
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

        print("content returned ", status_code)

        redirected_from = None
        if url is not webdriver.browser.current_url:
            redirected_from = url

        return {
            "status": status_code,
            "content": parsed_content,
            "content_type": content_type,
            "actual_url": webdriver.browser.current_url,
            "redirected_from": redirected_from
        }

    except IndexError:
        return None


def check_a_url(a_tag, base_url, domain):
    url = a_tag.get("href")

    if not url:
        # just to prevent errors
        return None

    return check_any_url(url, base_url, domain)


def check_any_url(url, base_url, domain):
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

    if url.startswith('../'):
        # if url is relative path and aims to parent folders
        split_url = url.split("/")
        num_of_slashes_to_root = split_url.count("..") + 1
        split_base_url = base_url.split("/")
        tmp_base_url_root = "/".join(split_base_url[:-num_of_slashes_to_root])
        if not tmp_base_url_root.endswith('/'):
            tmp_base_url_root += '/'
        return tmp_base_url_root + "/".join(split_url[split_url.count(".."):])

    # otherwise, url is absolute address
    # if absolute path, add base url
    if not base_url.endswith('/'):
        base_url += '/'
    return base_url + url


def check_onclick_url(onclick_tag, base_url, domain):
    onclick_code = onclick_tag.get("onclick").replace(" ", "").replace("\'", "\"")

    if 'location.href=' in onclick_code:
        re_match = re.search("location\.href=\".*\"", onclick_code)
        # get the url from match
        url = re_match.group().replace("location.href=", "").replace("\"", "")
        return check_any_url(url, base_url, domain)

    if 'location=' in onclick_code:
        re_match = re.search("location=\".*\"", onclick_code)
        # get the url from match
        url = re_match.group().replace("location=", "").replace("\"", "")
        return check_any_url(url, base_url, domain)

    # TODO:
    #  'location.replace(' in line
    #  'location.assign(' in line
    #  'window.open(' in line
    #  'parent.open(' in line
    return None


def check_img_url(img_tag, base_url, domain):
    url = img_tag.get("src")

    if not url or url.startswith("data:"):
        # just to prevent errors
        return None

    return check_any_url(url, base_url, domain)


def get_links_from_content(base_url, parsed_content):
    print("get links from content")

    base_tag = parsed_content.find('base')
    if base_tag:
        base_url = base_tag.get("href")

    base_url_split = base_url.split("/")
    domain = "/".join(base_url_split[:3])

    a_tags = parsed_content.find_all('a', href=True)
    a_urls = list(map(lambda a_tag: check_a_url(a_tag, base_url, domain), a_tags))

    # case sensitive - onclick !== onClick, but we don't check onClick as it's not a standard
    tags_onclick = parsed_content.find_all(onclick=True)
    onclick_urls = list(map(lambda onclick_tag: check_onclick_url(onclick_tag, base_url, domain), tags_onclick))

    all_urls = a_urls + onclick_urls
    all_urls = list(filter(None, all_urls))

    return all_urls


def get_img_urls_from_content(base_url, parsed_content):
    print("get img urls from content")

    base_tag = parsed_content.find('base')
    if base_tag:
        base_url = base_tag.get("href")

    base_url_split = base_url.split("/")
    domain = "/".join(base_url_split[:3])

    img_tags = parsed_content.find_all('img', src=True)
    img_urls = list(map(lambda img_tag: check_img_url(img_tag, base_url, domain), img_tags))  # array of urls
    img_urls = list(filter(None, img_urls))

    return img_urls


def get_binary_data(url):
    r = requests.get(url, stream=True)

    split_url = url.split("/")
    name = split_url[-1]
    content_type = r.headers['Content-Type']

    # test which works
    # raw = r.raw  # ne dela
    content = r.content
    # kvazi_bin = BytesIO(r.content) # se ni testiran
    # i = Image.open(BytesIO(r.content)) # se ni testiran

    # or use shutils somehow
    # https://stackoverflow.com/a/13137873

    return {"name": name, "content_type": content_type, "data": content}