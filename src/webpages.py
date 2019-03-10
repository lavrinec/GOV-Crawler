# everything related to getting the html code and parsing it
from src import webdriver
from bs4 import BeautifulSoup


def visit_url(url):
    print("visit url", url)

    # mark url as visited/processed in db

    content = get_url_content("https://google.com")
    # print(content)

    parsed_content = BeautifulSoup(content, 'html.parser')
    # print(parsed_content)

    # TODO: check for redirects
    # TODO-in-TODO: find out if better from original content or parsed content

    return parsed_content


def get_url_content(url):
    print("get content for", url)

    webdriver.browser.get(url)
    content = webdriver.browser.page_source
    return content


def get_links_from_content(parsed_content):
    print("get links from content")

    a_links = parsed_content.find_all('a')

    links = list(map(lambda link: link.get("href"), a_links ))  # array of urls
    print(links)

    return links


