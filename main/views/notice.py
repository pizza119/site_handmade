from flask import Blueprint, render_template

bp = Blueprint('notice', __name__, url_prefix='/notice')

@bp.route("/")
def notice_main():

    return render_template("/notice/notice.html")
