from src import webdriver
from src.webpages import visit_url, get_links_from_content, get_img_urls_from_content
from bs4 import BeautifulSoup


def main():
    webdriver.init()
    # cnt = await visit_url("http://evem.gov.si/robots.txt")
    cnt = visit_url("https://www.google.si")
    print("cnt", cnt)
    webdriver.close()


if __name__ == "__main__":
    main()
