# crawler worker - 1 crawler

from src.webpages import visit_url, get_links_from_content
from src.getters import get_not_reserved_page, finish_page
from src import db_manager
from src import webdriver


# main function for one process
def crawler_worker():
    print("crawler worker")

    db_manager.init()
    print("session", db_manager.session)

    webdriver.init()

    page = get_not_reserved_page()
    while page is not None:
        parsed_content = visit_url(page.url)

        # TODO get links [semi-done] and images and documents

        links = get_links_from_content(parsed_content, page.url)  # array of arrays [from_url, to_url]
        # TODO save links to DB

        # update page type and reservation
        finish_page(page)

        page = get_not_reserved_page()

    # this must be at the end when worker finishes
    webdriver.close()

    return True
