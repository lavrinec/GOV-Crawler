# crawler worker - 1 crawler

from src.webpages import visit_url
from src.getters import get_all_pages, get_all_sites
from src import db_manager


### main function for one process
def crawler_worker():
    print("crawler worker")

    db_manager.init()
    print("session", db_manager.session)

    get_all_sites()
    get_all_pages()

    # visit_url('https://google.com')

    return True
