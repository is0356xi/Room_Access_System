from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError



def length_check(form, field):
    if len(field.data) < 6:
        raise ValidationError('6文字以上じゃないと受け付けないよ〜')

def id_check(form, field):
    if not len(field.data) == 11:
        raise ValidationError('11桁じゃなかった？')
    elif not field.data.isdecimal():
        raise ValidationError('全部数字じゃなかった？')

def uname_check(form, field):
    if len(field.data) > 10:
        raise ValidationError('ちょっと長いね')
    elif not field.data.isalpha():
        raise ValidationError('ローマ字だよ？')

def line_check(form, field):
    # LINEトークンを使ってメッセージを送れるかどうか検証
    # レスポンスが200になるはず
    pass


def maddr_check(form, field):
    # xx:xx:xx:xx:xx:xxの形式かチェックする
    pass
    
        


class LoginForm(FlaskForm):
    student_id = StringField('Student id(ハイフンなし)', validators=[DataRequired(), id_check])
    user_name = StringField('User Name(ローマ字)', validators=[DataRequired(), uname_check])
    full_name = StringField('Full Name(漢字)', validators=[DataRequired()])
    token = StringField('LINE Notify Token', validators=[DataRequired(), line_check])
    mac_addr = StringField('MAC Adress', validators=[DataRequired(), maddr_check])
    submit = SubmitField('登録')