# crawler worker - 1 crawler

from src.webpages import visit_url, get_links_from_content, get_img_urls_from_content, get_binary_data
from src.getters import get_not_reserved_page, finish_page, cancel_all_sites_reservations, \
    cancel_all_pages_reservations, add_link_to_page, connect_image_with_page
from src import getters
from src import db_manager
from src import webdriver


# main function for one process
def crawler_worker():
    print("crawler worker")

    db_manager.init()
    print("session", db_manager.session)

    webdriver.init()
    getters.init()

    page = get_not_reserved_page()
    while page is not None:
        split_url = page.url.split("/")
        page_name = split_url[-1]
        split_page_name = page_name.split(".")

        allowed_binary_docs = ["pdf", "doc", "docx", "ppt", "pptx"]

        if len(split_page_name) >= 2 and split_page_name[-1] in allowed_binary_docs:
            # if the ending is pdf, doc, ...

            response = get_binary_data(page.url)
            # response = {name, data, content_type}
            # TODO: save to DB

            # update page type and reservation
            finish_page(page, page_type="BINARY")

        else:
            response = visit_url(page.url)

            links = get_links_from_content(response["actual_url"], response["content"])  # array of urls
            for link in links:
                add_link_to_page(link, page)

            images_urls = get_img_urls_from_content(response["actual_url"], response["content"])
            # TODO: get imgs and save imgs to db
            # for loop through image_url and call bin_data = get_binary_data(img_url)
            # the result for each is {name, data, content_type}
            for img_url in images_urls:
                connect_image_with_page(page.id, img_url, get_binary_data)



            connect_image_with_page

            # update page type and reservation
            finish_page(page, page_type="HTML")

        page = get_not_reserved_page()

    # this must be at the end when worker finishes
    webdriver.close()

    return True
