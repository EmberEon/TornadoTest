from wtforms import StringField
from wtforms.fields.simple import HiddenField
from wtforms import Form
from wtforms.validators import DataRequired, Length


class UserForm(Form):
    id = HiddenField()
    email = StringField('邮箱', validators=[DataRequired(message='请填写邮箱')])
    nick_name = StringField('昵称', validators=[Length(max=10, min=2, message='请输入3-1g长度的昵称')])
    password = StringField('密码')
    gender = StringField('性别')
    signatrue = StringField('签名')
    pic = StringField('头像')

