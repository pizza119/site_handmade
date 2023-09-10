from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from main.models import EnableDay, ComeMenber, EnableDay_comment, User, Each_snack
from main.forms import Day_Comment, SnackForm
from .auth import login_required
from main import db

bp = Blueprint('date', __name__, url_prefix='/date')

@bp.route('/')
def date():
    form = Day_Comment()
    year, month, day = request.args.get('dates', "2023-9-18", str).split('-')
    date = year + ',' + month + ',' + day
    # 오는사람 안오는사람 구분하기
    member = ComeMenber.query.filter_by(date=date).first()
    if not member:
        c_p_list, n_c_p_list = [''], ['']
    else:
        c_p_list, n_c_p_list = list((member.comeuser).split(',')), list((member.not_comeuser).split(','))
    # 그날의 내용 보여주기
    contents_list = EnableDay_comment.query.filter_by(date=date)
    name_list = []
    for i in contents_list:
        user = User.query.filter_by(id=i.id_user).first()
        name_list.append(user.username)
    # 그날 파인만 하는지 안하는지 알려주기
    e_d = EnableDay.query.filter_by(year=year, month=month, day = day).first()
    if e_d:
        enable_feynman = True
    else:
        enable_feynman = False
    return render_template('/day/date_detail.html', year = year, month = month, day = day, c_p_list = c_p_list, n_c_p_list = n_c_p_list,
                            form = form, contents_list = contents_list, name = name_list, enable_feynman = enable_feynman)


@bp.route("/EnableDay")
@login_required
def enableDay():
    year, month, day = request.args.get('dates', "2023-9-18", str).split('-')
    e_d = EnableDay.query.filter_by(year=year, month=month, day = day).first()
    days = EnableDay(year=year, month=month, day = day)
    if e_d:
        db.session.delete(e_d)
    else:
        db.session.add(days)
    db.session.commit()
    return redirect(url_for('main.index'))


@bp.route('/Record')
@login_required
def record():
    year, month, day = request.args.get('dates', "2023-9-18", str).split('-')
    come_notcome = request.args.get('come', "T", str)
    date = year + ',' + month + ',' + day
    come_people = ComeMenber.query.filter_by(date=date).first()
    if not come_people:
        # 데이터베이스에 날짜가 없을 때
        if come_notcome == 'T':    
            today_people = ComeMenber(date = date, comeuser = ','+g.user.name, not_comeuser = "")
        else:
            today_people = ComeMenber(date = date, comeuser = "", not_comeuser = ','+g.user.name)
        db.session.add(today_people)
        db.session.commit()
        return redirect( url_for('date.date')+"?dates=%s-%s-%s" %(year, month, day) )

    else:
        # 데이터베이스에 날짜가 있을 때
        c_p_list, n_c_p_list = list((come_people.comeuser).split(',')), list((come_people.not_comeuser).split(','))

        #이름이 포함되있을 경우
        if g.user.name in c_p_list:
            #온다에 들어있을 때
            c_p_list.remove(g.user.name)
        elif g.user.name in n_c_p_list:
            #오지 않는다에 들어있을 때
            n_c_p_list.remove(g.user.name)
        
        #이름이 아무곳에도 포함 안되있을 경우
        if come_notcome == 'T':    
            c_p_list.append(g.user.name)
        else:
            n_c_p_list.append(g.user.name)

        c_p_input, c_n_p_input = ",".join(c_p_list), ",".join(n_c_p_list)
        all_input = ComeMenber(date = date, comeuser = c_p_input, not_comeuser = c_n_p_input)
        db.session.delete(come_people)
        db.session.commit()
        db.session.add(all_input)
        db.session.commit()
        return redirect( url_for('date.date')+"?dates=%s-%s-%s" %(year, month, day) )


@bp.route('/Comment/<string:year>/<string:month>/<string:day>', methods = ("GET","POST"))
@login_required
def comment(year, month, day):
    date_list = [year, month, day]
    date_input = ','.join(date_list)
    form = Day_Comment()
    if request.method == 'POST' and form.validate_on_submit():    
        user = User.query.filter_by(username=g.user.username).first()
        text = EnableDay_comment(a_user = user, Title = form.Title.data , content = form.content.data, date = date_input)
        db.session.add(text)
        db.session.commit()
    elif (not form.Title.data) and (not form.content.data):    
        flash("제목과 내용은 반드시 기입해야 합니다.")
    elif not form.Title.data:
        flash("제목은 반드시 기입해야 합니다.")
    elif not form.content.data:
        flash("내용은 반드시 기입해야 합니다.")
    return redirect( url_for('date.date')+"?dates=%s-%s-%s" %(year, month, day) )


@bp.route('/Snack', methods = ("GET","POST"))
@login_required
def snack():
    year, month, day = request.args.get('dates', "2023-9-18", str).split('-')
    date = year + ',' + month + ',' + day
    come_people = ComeMenber.query.filter_by(date=date).first()
    if come_people:
        if (come_people.comeuser != ""):
            come_people_name_list = list(come_people.comeuser.split(','))
            come_people_name_list.remove('')
            # 이름을 아이디로 바꾸기
            sub1 = []
            for name in come_people_name_list:
                each_user = User.query.filter_by(name=name).first()
                sub1.append(each_user.username)
                come_people_name_list = sub1
            #이름을 아이디로 바꾸기 끝
        else:
            come_people_name_list = False
    else:
        come_people_name_list = False
    
    form = SnackForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=g.user.username).first()
        text = Each_snack(date = date, content = form.snack_content.data, a_user = user)
        db.session.add(text)
        db.session.commit()
    
    snack_all_data = Each_snack.query.filter_by(date=date)
    return render_template('/day/snack.html', come_people_name_list = come_people_name_list,  form = form, snack_all_data = snack_all_data, 
                           year = year, month = month, day = day)


@bp.route('/Delete_snack/<int:snack_id>', methods = ("GET","POST"))
@login_required
def delete_snack_function(snack_id):
    year, month, day = request.args.get('dates', "2023-9-18", str).split('-')
    delete_snack = Each_snack.query.filter_by(id=snack_id).first()
    db.session.delete(delete_snack)
    db.session.commit()
    return redirect( url_for('date.snack')+"?dates=%s-%s-%s" %(year, month, day) )


@bp.route('/Delete_comment/<int:comment_id>', methods = ("GET","POST"))
@login_required
def delete_comment_function(comment_id):
    year, month, day = request.args.get('dates', "2023-9-18", str).split('-')
    delete_comment = EnableDay_comment.query.filter_by(id=comment_id).first()
    db.session.delete(delete_comment)
    db.session.commit()
    return redirect( url_for('date.date')+"?dates=%s-%s-%s" %(year, month, day) )