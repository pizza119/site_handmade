'''
from main.models import EnableDay
from main import db


a = EnableDay.query.get()
db.session.delete(a)
db.session.commit()
'''