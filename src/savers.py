# savers
from sqlalchemy import exc

from src import db_manager


def save_page_to_db(page):
    try:
        db_manager.session.add(page)
        db_manager.session.commit()
    except exc.SQLAlchemyError as e:
        db_manager.handel_exception(e, True, 'save_page', page.url)
    return True


def save_site_to_db(site):
    try:
        db_manager.session.add(site)
        db_manager.session.commit()
    except exc.SQLAlchemyError as e:
        db_manager.handel_exception(e, True, 'save_site', site.domain)
    return True


def save_link_to_db(link):
    try:
        db_manager.session.add(link)
        db_manager.session.commit()
    except exc.SQLAlchemyError as e:
        db_manager.handel_exception(e, True, 'save_link', link.to_page)
    return True


def save_image_to_db(image):
    try:
        db_manager.session.add(image)
        db_manager.session.commit()
    except exc.SQLAlchemyError as e:
        db_manager.handel_exception(e, True, 'save_image', image.url)
    return True


def save_page_image_to_db(page_image):
    try:
        db_manager.session.add(page_image)
        db_manager.session.commit()
    except exc.SQLAlchemyError as e:
        db_manager.handel_exception(e, True, 'save_page_image', page_image.image_id)
    return True


def save_page_data_to_db(page_data):
    try:
        db_manager.session.add(page_data)
        db_manager.session.commit()
    except exc.SQLAlchemyError as e:
        db_manager.handel_exception(e, True, 'save_page_data', page_image.image_id)
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
