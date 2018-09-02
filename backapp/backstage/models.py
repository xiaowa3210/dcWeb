# # -*- coding: utf-8 -*-
#
# from peewee import MySQLDatabase, Model, CharField, BooleanField, IntegerField
# import json
# from werkzeug.security import check_password_hash
# from flask_login import UserMixin
#
# from flask_login import LoginManager, current_user, login_user, login_required
# # from backstage import login_manager
#
# import os
# # import sys
# # sys.path.extend(r"D:\lucy\研一下\大创xinyu\dachuangwebsite\dcWeb_2_0\backapp")
#
#
# from dcWeb_2_0.backapp import backstage
# # from backstage import login_manager
# from backstage import config
#
# from dcWeb_2_0.backapp.backstage import login_manager
#
# cfg = config[os.getenv('FLASK_CONFIG') or 'default']
#
# db = MySQLDatabase(host=cfg.DB_HOST, user=cfg.DB_USER, passwd=cfg.DB_PASSWD, database=cfg.DB_DATABASE)
#
#
# class BaseModel(Model):
#     class Meta:
#         database = db
#
#     def __str__(self):
#         r = {}
#         for k in self._data.keys():
#             try:
#                 r[k] = str(getattr(self, k))
#             except:
#                 r[k] = json.dumps(getattr(self, k))
#         # return str(r)
#         return json.dumps(r, ensure_ascii=False)
#
#
# # 管理员工号
# class Admin(UserMixin, BaseModel):
#     username = CharField()  # 用户名
#     password = CharField()  # 密码
#     fullname = CharField()  # 真实性名
#     email = CharField()  # 邮箱
#     phone = CharField()  # 电话
#     status = BooleanField(default=True)  # 生效失效标识
#
#     def verify_password(self, raw_password):
#         return check_password_hash(self.password, raw_password)
#
#
# # 通知人配置
# class CfgNotify(BaseModel):
#     check_order = IntegerField()  # 排序
#     notify_type = CharField()  # 通知类型：MAIL/SMS
#     notify_name = CharField()  # 通知人姓名
#     notify_number = CharField()  # 通知号码
#     status = BooleanField(default=True)  # 生效失效标识
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     return Admin.get(Admin.id == int(user_id))
#
#
# # 建表
# def create_table():
#     db.connect()
#     db.create_tables([CfgNotify, Admin])
#
#
# if __name__ == '__main__':
#     create_table()
