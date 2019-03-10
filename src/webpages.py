# everything related to getting the html code and parsing it
from src import webdriver


def visit_url(url):

    # mark url as visited/processed in db

    content = get_url_content(url)

    return content


def get_url_content(url):

    webdriver.browser.get(url)

    content = webdriver.browser.page_source
    print("page content")
    print(content)

    return content


