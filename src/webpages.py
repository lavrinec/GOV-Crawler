# everything related to getting the html code and parsing it
from src import webdriver
from bs4 import BeautifulSoup
import json


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


def get_links_from_content(parsed_content):
    print("get links from content")

    a_tags = parsed_content.find_all('a')

    a_urls = list(map(lambda link: link.get("href"), a_tags ))  # array of urls
    print(a_urls)

    return a_urls


def get_img_urls_from_content(parsed_content):
    print("get img urls from content")

    img_tags = parsed_content.find_all('img')

    img_urls = list(map(lambda link: link.get("src"), img_tags ))  # array of urls
    print(img_urls)

    return img_urls
