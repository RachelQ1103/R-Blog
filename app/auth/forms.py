from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

class RegistrationForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1,64), Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1,64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能包含字母,数字,点号或下划线.')
    ])
    password = PasswordField('密码', validators=[
        Required(), EqualTo('password2', message='密码必须一致')
    ])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱已注册.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('该用户名已存在.')

class ChangePasswordForm(Form):
    old_password = PasswordField('旧密码', validators=[Required()])
    password = PasswordField('密码', validators=[
        Required(), EqualTo('password2', message='密码必须一致')
    ])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('更新密码')

class PasswordResetRequestForm(Form):
    email = StringField('请输入您的邮箱', validators=[Required(), Length(1,64), Email()])
    submit = SubmitField('重设密码')

class PasswordResetForm(Form):
    email = StringField('邮箱', validators=[Required(), Length(1,64), Email()])
    password = PasswordField('密码', validators=[
        Required(), EqualTo('password2', message='密码必须一致')
    ])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('重设密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('邮箱不存在.')

class ChangeEmailForm(Form):
    email = StringField('新邮箱',validators=[Required(), Length(1,64), Email()])
    password = PasswordField('密码', validators=[Required()])
    submit = SubmitField('重设邮箱')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已存在.')