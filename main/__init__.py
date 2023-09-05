from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

import config

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

app = Flask(__name__)
app.config.from_object(config)

#ORM
db.init_app(app)
if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
    migrate.init_app(app, db, render_as_batch=True)
else:
    migrate.init_app(app, db)
from . import models

'''
@app.route('/')
def first():
    return redirect(url_for('day.day'))
'''

#블루프린트
from .views import dates, day, main_views, auth
app.register_blueprint(dates.bp)
app.register_blueprint(day.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(main_views.bp)


#필터
import main.filter
#app.jinja_env.filters["sdt"] = sdt


# -> 앞으로 할일
# 계시물 올린거 삭제, 수정할 수 있도록 하기
# 파일 올릴 수 있도록 하기
# 파인만 하는 날 누르면 그날에 올 사람 그거 data 없에자.
# db 너무 많은 값이 저장될 것을 방지해서 시간 지나면 데이터 사라지게 하기 -> 파인만 올 날짜 아니면 올사람 안올사람 삭제하기
# sqlalchemy 함 봐보기


# 그냥 해보기
# 아래는 onclick 함수 안에 url_for 함수대신 넣기 위해 싸운 흔적이다.
#onclick="location.href = '/date/EnableDay?dates={{year}}-{{month}}-{{day}}'"