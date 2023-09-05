from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo

class UserCreateForm(FlaskForm):
    name = StringField("사용자이름", validators=[DataRequired('이름은 필수 입력 항목입니다.')])
    nickname = StringField("아이디", validators=[DataRequired('아이디는 필수 입력 항목입니다.'), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired('비밀번호는 필수 입력 항목입니다.'), EqualTo('password2', '비밀번호가 일치하지 않습니다.')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired('비밀번호 확인은 필수 입력 항목입니다.')])

class UserLoginForm(FlaskForm):
    nickname = StringField("아이디", validators=[DataRequired('아이디는 필수 입력 항목입니다.'), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired('비밀번호는 필수 입력 항목입니다.')])

class Day_Comment(FlaskForm):
    Title = StringField("제목", validators=[DataRequired('제목은 필수 입력 항목입니다.')])
    content = StringField("내용", validators=[DataRequired('내용은 필수 입력 항목입니다.')])

class SnackForm(FlaskForm):
    snack_content = StringField("과자", validators=[DataRequired('과자를 입력해 주세요.')])
    