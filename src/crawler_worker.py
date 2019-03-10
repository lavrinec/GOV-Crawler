# crawler worker - 1 crawler

from src.webpages import visit_url
from src.getters import get_all_pages, get_all_sites, get_not_reserved_site
from src import db_manager
from src import webdriver


### main function for one process
def crawler_worker():
    print("crawler worker")

    db_manager.init()
    print("session", db_manager.session)

    # get_all_sites() and # get_all_pages() should be removed
    # here should come while ... getting pages from db, visiting them, etc.

    site = get_not_reserved_site()
    print(site)
    # get_all_sites()
    # get_all_sites()
    get_all_pages()

    webdriver.init()
    visit_url('https://google.com')

    # this must be at the end when worker finishes
    webdriver.close()

    return True
