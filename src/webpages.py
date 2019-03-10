# everything related to getting the html code and parsing it
from src import webdriver

def visit_url(url):

    content = get_url_content(url)

    return content


def get_url_content(url):

    for i in range(2):
        webdriver.driver.get(url)

    return True


