# everything related to getting the html code and parsing it

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
# chrome_options.add_argument("--headless")

def visit_url(url):

    content = get_url_content(url)

    return content


def get_url_content(url):
    driver = webdriver.Chrome(executable_path='./webdrivers/chromedriver-2-46', chrome_options=chrome_options)

    for i in range(2):
        driver.get(url)

    driver.close()

    return True


