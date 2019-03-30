from src import webdriver
from src.webpages import visit_url, get_links_from_content, get_img_urls_from_content
from bs4 import BeautifulSoup


def main():
    webdriver.init()
    # cnt = await visit_url("http://evem.gov.si/robots.txt")
    # response_obj = visit_url("http://evem.gov.si/")
    response_obj = visit_url("https://www.plus2net.com/html_tutorial/button-linking.php")
    print("res", response_obj["status"], response_obj["actual_url"])

    actual_url = response_obj["actual_url"]

    links = get_links_from_content(actual_url, response_obj["content"])

    webdriver.close()


if __name__ == "__main__":
    main()
