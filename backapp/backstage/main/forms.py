from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from tensorboard.backend.event_processing.event_accumulator import IMAGES
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from flask_uploads import UploadSet, IMAGES
from flask_uploads import configure_uploads, patch_request_class

photos = UploadSet('photos', IMAGES)
class CfgNotifyForm(FlaskForm):
    check_order = StringField('排序', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    notify_type = SelectField('通知类型', choices=[('MAIL', '邮件通知'), ('SMS', '短信通知')],
                              validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    notify_name = StringField('通知人姓名', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    notify_number = StringField('通知号码', validators=[DataRequired(message='不能为空'), Length(0, 64, message='长度不正确')])
    status = BooleanField('生效标识', default=True)
    submit = SubmitField('提交')

class AddinfoForm(FlaskForm):
    title = StringField('文章标题', validators=[DataRequired(), Length(1, 64), ])
    content = TextAreaField('文章内容', validators=[DataRequired() ])
    attachment = FileField('文件',validators=[FileRequired(message='未选择文件')])
    submit = SubmitField('提交')


class AddDocumentForm(FlaskForm):
    title = StringField('政策标题', validators=[DataRequired(), Length(1, 64), ])
    attachment =  FileField('文件',validators=[FileRequired(message='未选择文件')])
    submit = SubmitField('提交')

class AddProjectForm(FlaskForm):
    name = StringField('项目名称', validators=[DataRequired(), Length(1, 64), ])
    team_info = StringField('团队信息', validators=[DataRequired(), Length(1, 1024), ])
    introduction = TextAreaField('项目简介', validators=[DataRequired(), Length(1, 8*1024), ])
    photo = FileField(validators=[FileRequired(message='未选择文件'),
                                  FileAllowed(photos, message='只能上传图片')])
    video = FileField(validators=[FileRequired(message='未选择文件')])
    submit = SubmitField('提交')

class AddAdminForm(FlaskForm):
    name = StringField('用户名', validators=[DataRequired(), Length(1, 64), ])
    password =  StringField('用户密码', validators=[DataRequired(), Length(1, 64), ])
    rep_password =  StringField('请确认用户密码', validators=[DataRequired(), Length(1, 64), ])
    submit = SubmitField('提交')





