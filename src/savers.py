# savers
from sqlalchemy import exc

from src import db_manager


def save_site_to_db():
    return True


def save_page_to_db(page):
    try:
        db_manager.session.add(page)
        db_manager.session.commit()
    except exc.SQLAlchemyError as e:
        db_manager.handel_exception(e, True, 'save_page', page.url)
    return True


### saving documents

def save_documents_to_db(doc_array, page_id):
    for doc in doc_array:
        save_document_to_db(doc, page_id)

    return True


def save_document_to_db(url, page_id):
    return True


### saving images

def save_images_to_db(img_array, page_id):
    for img in img_array:
        save_document_to_db(img, page_id)

    return True


def save_image_to_db(url, page_id):
    return True

