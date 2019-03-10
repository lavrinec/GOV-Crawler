# everything related to getting the html code and parsing it
from src import webdriver
from bs4 import BeautifulSoup
import json


def visit_url(url):
    print("visit url", url)

    # mark url as visited/processed in db

    content = get_url_content(url)

    parsed_content = BeautifulSoup(content, 'html.parser')

    # TODO: check for redirects
    # TODO-in-TODO: find out if better from original content or parsed content

    return parsed_content


def get_url_content(url):
    print("get content for", url)

    webdriver.browser.get(url)
    har = json.loads(webdriver.browser.get_log('har')[0]['message'])

    # prints status code and text
    print(har['log']['entries'][0]['response']['status'])
    print(har['log']['entries'][0]['response']['statusText'])

    content = webdriver.browser.page_source
    return content


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
