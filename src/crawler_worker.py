# crawler worker - 1 crawler

from src.webpages import visit_url

### main function for one process
def crawler_worker():
    print("crawler worker")

    visit_url('https://google.com')

    return True
