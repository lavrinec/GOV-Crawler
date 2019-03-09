# main file that contains main function

from src.crawler_worker import crawler_worker
import sys


if __name__ == "__main__":
    num_of_workers = sys.argv[1]
    # to be added: start num_of_workers crawlers in own processes
    crawler_worker()
