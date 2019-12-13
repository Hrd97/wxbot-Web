from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, Regexp, EqualTo
from models import Groupmsg, Users

class RegisterForm(FlaskForm):
    phonenumber = StringField('手机号', validators=[ DataRequired(), Length(11)])
    password = PasswordField('密码', validators=[DataRequired(), EqualTo('password2', message='两次输入的密码必须一致')])
    password2 = PasswordField('确认密码',validators=[DataRequired()])
    submit = SubmitField('注册')

    # def __init__(self, *args, **kwargs):
    #     super(RegisterForm, self).__init__(*args, **kwargs)
    #     self.role.choices = [(role.id, role.name)
    #         for role in UserGroup.query.order_by(UserGroup.name).all()] #还要再改

    def validate(self, field):
        if Users.query.filter_by(idcard=field.data).first():
            raise ValidationError('该用户身份证已经被注册。')

class LoginForm(FlaskForm):
    phonenumber = StringField('手机号', validators=[ DataRequired(), Length(11)])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')