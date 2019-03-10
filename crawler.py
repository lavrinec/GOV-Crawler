# main file that contains main function
from src import db_manager
from src.crawler_worker import crawler_worker
import sys
from src.getters import get_all_pages, get_all_sites

if __name__ == "__main__":
    db_manager.init()
    get_all_sites()
    get_all_pages()
    num_of_workers = sys.argv[1]
    # to be added: start num_of_workers crawlers in own processes
    crawler_worker()
