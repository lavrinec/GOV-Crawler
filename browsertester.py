from src import webdriver
from src.webpages import visit_url, get_links_from_content, get_img_urls_from_content, get_binary_data
from bs4 import BeautifulSoup


def main():
    webdriver.init()
    # cnt = await visit_url("http://evem.gov.si/robots.txt")
    response_obj = visit_url("http://evem.gov.si/")
    # response_obj = visit_url("https://www.ajpes.si/Registri/Poslovni_register/Splosno")
    print("res", response_obj["status"], response_obj["actual_url"])

    actual_url = response_obj["actual_url"]

    links = get_links_from_content(actual_url, response_obj["content"])
    print("links", links)

    img_urls = get_img_urls_from_content(actual_url, response_obj["content"])
    print("img urls", img_urls)

    for img_url in img_urls:
        bin_data = get_binary_data(img_url)
        print("data", bin_data)

    webdriver.close()


if __name__ == "__main__":
    main()
