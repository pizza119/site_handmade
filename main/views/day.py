from flask import Blueprint, render_template, request
from datetime import datetime
from werkzeug.utils import redirect

from main.models import EnableDay

bp = Blueprint('day', __name__, url_prefix='/day')


# 달력 화면 코드
@bp.route('/')
def day():
    year = request.args.get('year', datetime.now().year, int)
    month = request.args.get('month', datetime.now().month, int)
    today_list = [datetime.now().year, datetime.now().month, datetime.now().day]
    e_d = EnableDay.query.order_by()
    if request.args.get('dates', '', str) != '':
        give_str = request.args.get('dates', "기본값 입력", str)
        return redirect('/date?dates=%s' %give_str)
    else:
        return render_template('/day/test2.html', year = year, month = month, t_list=today_list, e_d = e_d)


# 이거 test2에 꺼녛을 방법 생각해봐
'''
        {% for i in e_d %}
        {% elif (i.year == year) and (i.month == month) and (i.day == (a|int)) %}
            <td onClick="location.href='/date?dates={{year}}-{{month}}-{{a}}'" class="blinking table-danger"> <!-- class="table-danger table-active"-->
                {{a | safe}}
            </td>
        {% endfor %}
'''
