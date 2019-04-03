# main file that contains main function

from src.crawler_worker import crawler_worker
import sys
import time
from multiprocessing import Process

if __name__ == "__main__":

    num_of_workers = 1

    if len(sys.argv) == 2:
        num_of_workers = int(sys.argv[1])
        print("using provided number of workers:", num_of_workers)
    else:
        print("using default number of workers:", num_of_workers)

    print("starting {} workers".format(num_of_workers))

    processes = [Process(target=crawler_worker) for _ in range(num_of_workers)]

    for p in processes:
        p.start()
        time.sleep(1)

    for p in processes:
        p.join()

    print("all workers ended")
