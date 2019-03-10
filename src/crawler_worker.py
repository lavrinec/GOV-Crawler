# crawler worker - 1 crawler

from src.webpages import visit_url
from src.getters import get_not_reserved_page
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
        visit_url(page.url)
        page = get_not_reserved_page()

        # TODO get links and images

        # TODO update page type and reservation

    # this must be at the end when worker finishes
    webdriver.close()

    return True
