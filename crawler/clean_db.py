from sqlalchemy import update, and_

from src import db_manager
from src.page import Page

print("Start")
last = 150000
db_manager.init()
print("Naprej")
while last < 1191843:
    q = db_manager.session.query(Page).filter(
        and_(Page.id > last, Page.duplicated_with == None, Page.html_content != None)).order_by(Page.id.asc())
    # print(str(q))
    result = q.first()
    # print("Dobil")
    print(result.id)
    last = result.id
    q = update(Page) \
        .values({Page.html_content: None, Page.page_type_code: 'DUPLICATE', Page.duplicated_with: last}) \
        .where(and_(Page.id > last, Page.html_content == result.html_content))
    db_manager.session.execute(q)
    db_manager.session.commit()
